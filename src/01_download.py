import akshare as ak, pandas as pd, os, yaml, tqdm, multiprocessing as mp

cfg = yaml.safe_load(open('config.yaml'))
os.makedirs(cfg['raw_dir'], exist_ok=True)

def download_sym(sym):
    try:
        df = ak.stock_zh_a_hist(sym, period='1', adjust='hfq',
                                start_date=cfg['start'].replace('-',''),
                                end_date=cfg['end'].replace('-',''))
        if df.empty: return
        df.columns = ['date','open','close','high','low','vol','amt','turn']
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date','open','high','low','close','vol','amt','turn']]
        df.to_parquet(f"{cfg['raw_dir']}/{sym}.parquet")
    except Exception as e:
        print(sym, e)

if __name__ == '__main__':
    univ = []
    for idx in cfg['univ']:
        df = ak.index_stock_cons(idx.lower())
        univ.extend(df['品种代码'].astype(str).str.zfill(6).tolist())
    univ = sorted(set(unv))
    print('total symbols:', len(unv))
    with mp.Pool(mp.cpu_count()) as p:
        list(tqdm.tqdm(p.imap(download_sym, univ), total=len(unv)))