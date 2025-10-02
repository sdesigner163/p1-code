import subprocess
import os
import pandas as pd

def test_end2end():
    """CI 采样 3 只股票 30 天快速跑通"""
    os.environ['TEST_SAMPLE'] = '3'

    # 自动答 y，顺序跑完 2~5
    subprocess.run(
        ['python', '../run.py'],   # 关键：相对路径上移一层
        input='y\n2\ny\n3\ny\n4\ny\n5\n',
        text=True,
        check=True
    )

    assert os.path.exists('../results/roll_results.csv')
    res = pd.read_csv('../results/roll_results.csv')
    assert res['auc'].mean() > 0.55

if __name__ == '__main__':
    test_end2end()