import pandas as pd, numpy as np, os, yaml, tqdm, multiprocessing as mp

cfg = yaml.safe_load(open('config.yaml'))
os.makedirs(cfg['feature_dir'], exist_ok=True)

def vpin(buy_vol, sell_vol, bucket_size):
    df = pd.DataFrame({'bv':buy_vol, 'sv':sell_vol})
    df['bucket'] = np.arange(len(df)) // bucket_size
    agg = df.groupby('bucket')[['bv','sv']].sum()
    agg['vpin'] = np.abs(agg['bv'] - agg['sv']) / (agg['bv'] + agg['sv'] + 1e-8)
    return agg['vpin'].mean()

def make_features(sym):
    try:
        df = pd.read_parquet(f"{cfg['raw_dir']}/{sym}.parquet")
    except: return
    df = df.sort_values('date').reset_index(drop=True)
    df['ret'] = np.log(df['close']/df['close'].shift(1))
    # RV
    df['rv'] = df['ret'].rolling(cfg['rv_minutes']).apply(lambda x: (x**2).sum(), raw=True)
    # TR
    df['tr'] = df['vol'].rolling(cfg['tr_window']).sum() / df['amt'].rolling(cfg['tr_window']).sum()
    # VPIN
    df['sign'] = np.where(df['ret']>=0, 1, -1)
    df['buy_vol']  = np.where(df['sign']==1, df['vol'], 0)
    df['sell_vol'] = np.where(df['sign']==-1, df['vol'], 0)
    df['vpin'] = df[['buy_vol','sell_vol']].rolling(50*cfg['vpin_buckets']).apply(
        lambda x: vpin(x['buy_vol'], x['sell_vol'], cfg['vpin_buckets']), raw=False)
    # label
    df['jump'] = (df['open'].shift(-1) - df['close']) / df['close']
    df['y'] = np.where(df['jump'] > 0, 1, -1)
    df = df.dropna(subset=['y','rv','tr','vpin'])
    # z-score
    for col in ['rv','tr','vpin']:
        roll = df[col].rolling(cfg['zscore_window'])
        df[col] = (df[col] - roll.mean()) / roll.std()
    out = df[['date','y','rv','tr','vpin']]
    out['sym'] = sym
    out.to_parquet(f"{cfg['feature_dir']}/{sym}.parquet")

if __name__ == '__main__':
    syms = [f.replace('.parquet','') for f in os.listdir(cfg['raw_dir'])]
    with mp.Pool(mp.cpu_count()) as p:
        list(tqdm.tqdm(p.imap(make_features, syms), total=len(syms)))