import pandas as pd, numpy as np, os, yaml, lightgbm as lgb, optuna
from sklearn.metrics import roc_auc_score, accuracy_score, matthews_corrcoef
from imblearn.metrics import geometric_mean_score

cfg = yaml.safe_load(open('config.yaml'))
os.makedirs(cfg['result_dir'], exist_ok=True)

def load_all():
    dfs = [pd.read_parquet(f"{cfg['feature_dir']}/{f}")
           for f in os.listdir(cfg['feature_dir']) if f.endswith('.parquet')]
    df = pd.concat(dfs).sort_values(['date','sym']).reset_index(drop=True)
    return df.dropna()

dates = load_all()['date'].unique()
T = len(dates)

def roll_split(start_idx):
    tr_e = start_idx + cfg['roll_train_days']
    va_e = tr_e + cfg['roll_valid_days']
    te_e = va_e + cfg['roll_test_days']
    if te_e > T: return None
    return dates[start_idx], dates[tr_e], dates[va_e], dates[te_e]

def objective(trial, X_tr, y_tr, X_va, y_va):
    param = {
        'objective': cfg['lgb_params']['objective'],
        'metric': cfg['lgb_params']['metric'],
        'verbosity': cfg['lgb_params']['verbosity'],
        'num_leaves': trial.suggest_int('num_leaves', 16, 64),
        'max_depth': trial.suggest_int('max_depth', 4, 12),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.5, 1.0),
        'n_estimators': trial.suggest_int('n_estimators', 200, 1000),
    }
    gbm = lgb.LGBMClassifier(**param)
    gbm.fit(X_tr, y_tr, eval_set=[(X_va, y_va)], early_stopping_rounds=50, verbose=False)
    return roc_auc_score(y_va, gbm.predict_proba(X_va)[:,1])

df = load_all()
dates = df['date'].unique()
res = []
idx = 0
while True:
    sp = roll_split(idx * cfg['roll_test_days'])
    if sp is None: break
    tr_s, tr_e, va_s, va_e, te_s, te_e = *sp, *(sp[2:4])
    train_df = df[(df['date']>=tr_s)&(df['date']<tr_e)]
    valid_df = df[(df['date']>=va_s)&(df['date']<va_e)]
    test_df  = df[(df['date']>=te_s)&(df['date']<te_e)]
    X_tr, y_tr = train_df[['rv','tr','vpin']], train_df['y']
    X_va, y_va = valid_df[['rv','tr','vpin']], valid_df['y']
    X_te, y_te = test_df[['rv','tr','vpin']],  test_df['y']

    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_tr, y_tr, X_va, y_va),
                   n_trials=cfg['optuna_trials'], n_jobs=1)
    best = study.best_params
    best_model = lgb.LGBMClassifier(**best)
    best_model.fit(X_tr, y_tr, eval_set=[(X_va, y_va)], verbose=False)

    prob = best_model.predict_proba(X_te)[:,1]
    pred = (prob > 0.5).astype(int)
    auc  = roc_auc_score(y_te, prob)
    acc  = accuracy_score(y_te, pred)
    mcc  = matthews_corrcoef(y_te, pred)
    res.append({'test_start':te_s, 'test_end':te_e, 'auc':auc, 'acc':acc, 'mcc':mcc})
    best_model.booster_.save_model(f"{cfg['result_dir']}/model_{idx}.txt")
    test_df.assign(prob=prob, pred=pred).to_parquet(f"{cfg['result_dir']}/pred_{idx}.parquet")
    idx += 1

pd.DataFrame(res).to_csv(f"{cfg['result_dir']}/roll_results.csv", index=False)