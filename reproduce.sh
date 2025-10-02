#!/usr/bin/env bash
set -e
echo "==== 1. 下载 1-min OHLCV ===="
python src/01_download.py
echo "==== 2. 构造特征与标签 ===="
python src/02_feature_label.py
echo "==== 3. 滚动训练 + 调参 ===="
python src/03_train.py
echo "==== 4. 评估 & 经济指标 ===="
python src/04_evaluate.py
echo "==== 5. SHAP 解释性 ===="
python src/05_shap.py
echo "==== 全部完成，输出见 results/ ===="