# LightGBM-3F-Code
可复现的「VPIN + LightGBM」A股隔夜跳空预测完整流水线（分钟 K 线）

## 一键安装
```bash
pip install -r requirements.txt
0. 唯一需要改的
打开 config.yaml，把 jq_user / jq_pass 填成你的聚宽手机号/密码。
1. 日常人工交互
bash
复制
python run.py
菜单选 2-5 即可；下载（1）已隐藏，需单独：
bash
复制
python src/01_download.py
## 2. CI / 无人值守
```bash
cd tests && python test_pipeline.py
（会自动答 y 并跑完 2-5，生成 results/roll_results.csv）
3. 结果
指标：results/roll_results.csv
经济：results/economic.csv
SHAP 图：results/fig2_shap_summary.pdf / fig3_shap_interaction.pdf
复制

--------------------------------------------------
三、其余文件 **完全不用动**  
（01_download.py、02_feature_label.py、03_train.py、04_evaluate.py、05_shap.py、utils.py、config.yaml、requirements.txt 均已在上轮给出，无需任何修改）

--------------------------------------------------
四、快速开始（3 行命令）
```bash
git clone <你的仓库> LightGBM-3F-Code
cd LightGBM-3F-Code
pip install -r requirements.txt
# 改 config.yaml 账号
python test_pipeline.py   # CI 快速自检



# LightGBM-3F-Paper  
This repository contains the **camera-ready LaTeX source** and **figures/tables only** for:  
"Explainable and reproducible VPIN-driven tree ensemble for overnight jump in Chinese mid- and small-caps with public minute-bar data" (Expert Systems With Applications, 2025).  

> **Code & Data Pipeline**: https://github.com/yourrepo/LightGBM-3F-Code  
> **Latest PDF**: [![Compile LaTeX](https://github.com/yourrepo/LightGBM-3F-Paper/actions/workflows/compile-latex.yml/badge.svg)](https://github.com/yourrepo/LightGBM-3F-Paper/actions)

## Structure
LightGBM-3F-Paper/
├── main.tex               % 主文件
├── figs/                  % 矢量 PDF 图表（5 张）
├── tables/                % LaTeX 表格（3 张）
├── supplemental/          % 附录与伦理声明
└── .github/workflows/     % GitHub Action 自动编译
复制

## Quick Build
```bash
git clone https://github.com/yourrepo/LightGBM-3F-Paper.git
cd LightGBM-3F-Paper
latexmk -xelatex main.tex   % 本地需安装 XeLaTeX + latexmk
License
MIT © 2025 Authors