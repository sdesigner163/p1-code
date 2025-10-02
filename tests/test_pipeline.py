import subprocess, os, pandas as pd

def test_end2end():
    """CI 采样 3 只股票 30 天快速跑通"""
    os.environ['TEST_SAMPLE'] = '3'  # 在 01_download.py 中读取并截断
    subprocess.run(['bash', 'reproduce.sh'], check=True)
    assert os.path.exists('results/roll_results.csv')
    res = pd.read_csv('results/roll_results.csv')
    assert res['auc'].mean() > 0.55  #  sanity check

if __name__ == '__main__':
    test_end2end()