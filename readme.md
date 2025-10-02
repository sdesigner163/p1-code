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