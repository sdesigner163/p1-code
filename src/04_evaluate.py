import pandas as pd, numpy as np, os, yaml
from utils import annual_sharpe, max_drawdown

cfg = yaml.safe_load(open('config.yaml'))
res = pd.read_csv(f"{cfg['result_dir']}/roll_results.csv")
print('Mean AUC :', res['auc'].mean())
print('Mean ACC :', res['acc'].mean())
print('Mean MCC :', res['mcc'].mean())

# 经济评估
dfs = [pd.read_parquet(f"{cfg['result_dir']}/{f}")
       for f in os.listdir(cfg['result_dir']) if f.startswith('pred_')]
df = pd.concat(dfs)
df['pos'] = np.where(df['pred']==1, 1, -1)
df['ret'] = df['y'] * df['pos'] - cfg['cost'] * np.abs(df['pos'].diff()).fillna(0)
ann_ret = df['ret'].mean() * 252
sharpe  = annual_sharpe(df['ret'])
mdd     = max_drawdown(df['ret'])
print('Ann. return :', f"{ann_ret:.1%}")
print('Sharpe      :', f"{sharpe:.2f}")
print('MDD         :', f"{mdd:.1%}")

# 保存经济结果
eco = pd.DataFrame([{'ann_ret':ann_ret, 'sharpe':sharpe, 'mdd':mdd}])
eco.to_csv(f"{cfg['result_dir']}/economic.csv", index=False)