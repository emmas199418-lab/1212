#!/usr/bin/env python3
"""
暗影傳說 - 繁體中文文字 RPG 遊戲
執行方式：python main.py
需要 Python 3.7+
"""
import sys

def check_python_version():
    if sys.version_info < (3, 7):
        print("錯誤：本遊戲需要 Python 3.7 或更高版本。")
        print(f"目前版本：{sys.version}")
        sys.exit(1)

if __name__ == "__main__":
    check_python_version()
    try:
        from game import run_game
        run_game()
    except KeyboardInterrupt:
        print("\n\n  遊戲中斷。感謝遊玩！")
        sys.exit(0)
