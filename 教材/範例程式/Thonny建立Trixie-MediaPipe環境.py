"""在 Thonny 用系統 Python 3.13 執行：建立 MediaPipe 與 CVZone 環境。

Python 3.13 的 ARM64 只能安裝 MediaPipe 1.x（沒有 0.10.x 的輪子）。
--system-site-packages 讓相機程式也能匯入系統的 Picamera2。target 必須是新資料夾。
"""
from pathlib import Path
import subprocess
import sys

target = Path.home() / 'ba5077-mediapipe-trixie-20261112'
if target.exists():
    raise RuntimeError(f'目標已存在：{target}，請修改 target 選擇新資料夾')
print('Creating:', target, flush=True)
subprocess.run([sys.executable, '-m', 'venv', '--system-site-packages', str(target)], check=True)
python = str(target / 'bin' / 'python3')
subprocess.run([python, '-m', 'pip', 'install', 'mediapipe==1.2.2', 'cvzone==2.0.0'], check=True)
subprocess.run([python, '-c',
                'import cv2, mediapipe as mp; from picamera2 import Picamera2; '
                'print("Picamera2 OK; OpenCV", cv2.__version__, "MediaPipe", mp.__version__, '
                '"solutions:", hasattr(mp, "solutions"))'], check=True)
print('Environment ready:', python, flush=True)
