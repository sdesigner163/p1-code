# 01_download.py  ——  JQData 纯付费，自动区间
import os, yaml, tqdm, multiprocessing as mp
import pandas as pd
from jqdatasdk import auth, get_price

# ---------- 读取配置 ----------
cfg = yaml.safe_load(open('../config.yaml', encoding='utf-8'))
RAW_DIR = cfg['raw_dir']
os.makedirs(RAW_DIR, exist_ok=True)

# ---------- 登录 ----------
auth(cfg['jq_user'], cfg['jq_pass'])

# ---------- 自动选择日期 ----------
date_cfg = cfg['date_cfg'][cfg['account_type']]
START_DATE = date_cfg['start']
END_DATE   = date_cfg['end']
FREQ       = '1m'

def download_sym(sym: str):
    try:
        code = f"{sym}.XSHG" if sym.startswith('6') else f"{sym}.XSHE"
        df = get_price(code, start_date=START_DATE, end_date=END_DATE,
                       frequency=FREQ, fields=['open','high','low','close','volume','money'],
                       skip_paused=True)
        if df.empty:
            return
        df.reset_index(inplace=True)
        df.rename(columns={'index':'date','volume':'vol','money':'amt'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date','open','high','low','close','vol','amt']]
        df.to_parquet(f"{RAW_DIR}/{sym}.parquet")
    except Exception as e:
        print(sym, e)

if __name__ == '__main__':
    import akshare as ak
    univ = []
    for idx in cfg['univ']:
        univ.extend(ak.index_stock_cons(idx.lower())['品种代码'].astype(str).str.zfill(6).tolist())
    univ = sorted(set(univ))
    print('total symbols:', len(univ))
    with mp.Pool(mp.cpu_count()) as p:
        list(tqdm.tqdm(p.imap(download_sym, univ), total=len(univ)))