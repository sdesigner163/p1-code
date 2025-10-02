#!/usr/bin/env python3
"""
端到端流水线控制台（单文件、跨平台）
> python run.py
"""
import subprocess
import sys

TASKS = {
    2: ("2. 构造特征与标签", "python src/02_feature_label.py"),
    3: ("3. 滚动训练 + 调参", "python src/03_train.py"),
    4: ("4. 评估 & 经济指标", "python src/04_evaluate.py"),
    5: ("5. SHAP 解释性", "python src/05_shap.py"),
}

def run(cmd):
    print(f"\n>>>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def menu():
    while True:
        print("\n========== 主菜单 ==========")
        print("1. 下载 1-min OHLCV  （请单独执行 src/01_download.py）")
        for k, (name, _) in TASKS.items():
            print(f"{k}. {name}")
        print("0. 退出")
        choice = input("请选择要执行的序号: ").strip()
        if choice == "0":
            print("已退出，拜拜~")
            sys.exit(0)
        if choice == "1":
            print("\n提示：下载功能请手动运行  python src/01_download.py")
            continue
        if choice.isdigit() and int(choice) in TASKS:
            return int(choice)
        print("输入无效，请重试！")

def main():
    while True:
        choice = menu()
        name, cmd = TASKS[choice]

        ans = input("\n数据将被覆盖，是否继续？ [y/N] ").strip()
        if ans.lower() != "y":
            print("用户取消，返回主菜单。")
            continue

        print(f"\n==== {name} ====")
        run(cmd)
        print(f"==== {name} 完成 ====")

if __name__ == "__main__":
    main()