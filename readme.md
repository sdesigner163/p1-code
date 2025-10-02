```markdown
# LightGBM-3F-Code  
可复现的「VPIN + LightGBM」A股隔夜跳空预测完整流水线（分钟 K 线）

---

## 1. 一键安装
```bash
pip install -r requirements.txt
```

---

## 2. 快速开始（仅需 3 行命令）

```bash
git clone <你的仓库> LightGBM-3F-Code
cd LightGBM-3F-Code
pip install -r requirements.txt
```

---

## 3. 配置账号（唯一需要修改）

打开 `config.yaml`，将 `jq_user` / `jq_pass` 改为你的聚宽手机号/密码。

---

## 4. 日常使用（人工交互）

```bash
python run.py
```

菜单中选择 `2-5` 即可；  
数据下载（1）已隐藏，如需使用请单独运行：

```bash
python src/01_download.py
```

---

## 5. CI / 无人值守

```bash
cd tests && python test_pipeline.py
```

（自动确认并跑完步骤 2-5，生成结果文件）

---

## 6. 输出结果

| 类型 | 文件路径 |
|------|----------|
| 指标 | `results/roll_results.csv` |
| 经济 | `results/economic.csv` |
| SHAP 图 | `results/fig2_shap_summary.pdf`<br>`results/fig3_shap_interaction.pdf` |

---

## 7. 文件说明（无需修改）

| 文件 | 说明 |
|------|------|
| `01_download.py` | 数据下载 |
| `02_feature_label.py` | 特征与标签生成 |
| `03_train.py` | 模型训练 |
| `04_evaluate.py` | 模型评估 |
| `05_shap.py` | SHAP 解释 |
| `utils.py` | 工具函数 |
| `config.yaml` | 配置文件 |
| `requirements.txt` | 依赖列表 |

---

## 8. 仓库地址

- **代码与数据流水线**：[https://github.com/yourrepo/LightGBM-3F-Code](https://github.com/yourrepo/LightGBM-3F-Code)

---

# LightGBM-3F-Paper

本仓库包含论文 **"Explainable and reproducible VPIN-driven tree ensemble for overnight jump in Chinese mid- and small-caps with public minute-bar data"**（Expert Systems With Applications, 2025）的 **LaTeX 源码** 与 **图表文件**。

> **最新 PDF**：[![Compile LaTeX](https://github.com/yourrepo/LightGBM-3F-Paper/actions/workflows/compile-latex.yml/badge.svg)](https://github.com/yourrepo/LightGBM-3F-Paper/actions)

---

## 仓库结构

```
LightGBM-3F-Paper/
├── main.tex                 # 主文件
├── figs/                    # 矢量 PDF 图表（5 张）
├── tables/                  # LaTeX 表格（3 张）
├── supplemental/            # 附录与伦理声明
└── .github/workflows/       # GitHub Action 自动编译
```

---

## 本地编译

```bash
git clone https://github.com/yourrepo/LightGBM-3F-Paper.git
cd LightGBM-3F-Paper
latexmk -xelatex main.tex   # 需安装 XeLaTeX + latexmk
```

---

## 许可证

MIT © 2025 Authors
```