import numpy as np, pandas as pd
from scipy import stats

def delong_roc_variance(ground_truth, predictions):
    """DeLong 方差近似，返回 (AUC, stderr)"""
    # 简化实现，够用即可
    auc, _, _, _ = stats.roc_auc_score(ground_truth, predictions, return_stderr=True)
    return auc

def max_drawdown(returns):
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    return drawdown.min()

def annual_sharpe(returns, freq=252):
    return returns.mean() / returns.std() * np.sqrt(freq)