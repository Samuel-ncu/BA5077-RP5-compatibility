"""在 Thonny 用系統 Python 3.13 執行：建立同時可用 Picamera2 與 YOLOv8 的環境。

--system-site-packages 讓新環境讀得到系統的 Picamera2；PyTorch 從官方 CPU 來源安裝，
避免 pip 去解析 CUDA 套件。target 必須是還不存在的新資料夾。
"""
from pathlib import Path
import subprocess
import sys

target = Path.home() / 'ba5077-yolo-camera-trixie-20261112'
if target.exists():
    raise RuntimeError(f'目標已存在：{target}，請修改 target 選擇新資料夾')
print('Creating:', target, flush=True)
subprocess.run([sys.executable, '-m', 'venv', '--system-site-packages', str(target)], check=True)
python = str(target / 'bin' / 'python3')
subprocess.run([python, '-m', 'pip', 'install',
                'torch==2.15.0+cpu', 'torchvision==0.29.2+cpu',
                '--index-url', 'https://download.pytorch.org/whl/cpu'], check=True)
subprocess.run([python, '-m', 'pip', 'install', 'ultralytics==8.4.208'], check=True)
subprocess.run([python, '-c',
                'import cv2, torch, ultralytics; from picamera2 import Picamera2; '
                'print("Picamera2 OK; OpenCV", cv2.__version__, "PyTorch", torch.__version__, '
                '"Ultralytics", ultralytics.__version__)'], check=True)
print('Environment ready:', python, flush=True)
