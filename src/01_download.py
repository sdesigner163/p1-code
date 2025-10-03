# 01_download.py
from __future__ import annotations

import multiprocessing as mp
import os
from datetime import timedelta

import pandas as pd
import tqdm
import yaml
from jqdatasdk import auth, get_index_stocks, get_price

# ---------- 配置 ----------
CFG = yaml.safe_load(open("../config.yaml", encoding="utf-8"))
RAW_DIR = CFG["raw_dir"]
os.makedirs(RAW_DIR, exist_ok=True)
CPU_COUNT = mp.cpu_count()
FREQ = "1m"

# ---------- 登录 ----------
auth(CFG["jq_user"], CFG["jq_pass"])

# ---------- 日期区间 ----------
def calc_date_span() -> tuple[str, str]:
    """返回 (start, end) 字符串，试用版自动平移，正式版读配置"""
    if CFG["account_type"] == "trial":
        base_left  = pd.Timestamp("2024-06-23")
        base_right = pd.Timestamp("2025-06-30")
        base_today = pd.Timestamp("2025-10-01")
        delta = (pd.Timestamp.today().floor("D") - base_today).days
        return (
            (base_left  + timedelta(days=delta)).strftime("%Y-%m-%d"),
            (base_right + timedelta(days=delta)).strftime("%Y-%m-%d"),
        )
    else:
        return CFG["date_cfg"]["formal"]["start"], CFG["date_cfg"]["formal"]["end"]

START_DATE, END_DATE = calc_date_span()
print(f"{CFG['account_type']} 区间: {START_DATE} ~ {END_DATE}")

# ---------- 单标的下载 ----------
def download_sym(sym: str) -> None:
    try:
        code = f"{sym}.XSHG" if sym.startswith("6") else f"{sym}.XSHE"
        df = get_price(
            code,
            start_date=START_DATE,
            end_date=END_DATE,
            frequency=FREQ,
            fields=["open", "high", "low", "close", "volume", "money"],
            skip_paused=True,
        )
        if df.empty:
            return
        df = (
            df.rename(columns={"volume": "vol", "money": "amt"})
            .reset_index()
            .assign(date=lambda x: pd.to_datetime(x["index"]))
            .loc[:, ["date", "open", "high", "low", "close", "vol", "amt"]]
        )
        df.to_parquet(f"{RAW_DIR}/{sym}.parquet")
    except Exception as e:
        print(sym, e)

# ---------- 主入口 ----------
if __name__ == "__main__":
    universe: set[str] = set()
    for idx in CFG["univ"]:
        universe.update(get_index_stocks(idx, date=END_DATE))

    universe = sorted({s.split(".")[0] for s in universe})
    print(f"total symbols: {len(universe)}")

    with mp.Pool(CPU_COUNT) as pool:
        list(tqdm.tqdm(pool.imap(download_sym, universe), total=len(universe), ncols=88))