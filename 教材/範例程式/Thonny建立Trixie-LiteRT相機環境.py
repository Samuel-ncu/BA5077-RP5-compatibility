from pathlib import Path
import subprocess
import sys

target = Path.home() / 'ba5077-litert-camera-course-env'
if target.exists():
    raise RuntimeError(f'目標已存在：{target}，請修改 target 選擇新資料夾')
print('Creating:', target, flush=True)
subprocess.run([sys.executable, '-m', 'venv', '--system-site-packages', str(target)], check=True)
python = target / 'bin' / 'python'
subprocess.run([str(python), '-m', 'pip', 'install',
                'numpy==2.2.4', 'opencv-python==4.12.0.88',
                'ai-edge-litert==2.3.0'], check=True)
subprocess.run([str(python), '-c',
                'import cv2,numpy; from picamera2 import Picamera2; '
                'from ai_edge_litert.interpreter import Interpreter; '
                'from importlib.metadata import version; '
                'print("Picamera2 OK; OpenCV",cv2.__version__,"NumPy",numpy.__version__,'
                '"LiteRT",version("ai-edge-litert"))'], check=True)
print('Environment ready:', python, flush=True)
