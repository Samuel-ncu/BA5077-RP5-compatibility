"""觀察目前的 Python 與常用套件；不安裝、移除套件或讀取相機。"""
from importlib.metadata import PackageNotFoundError, version
from importlib.util import find_spec
import platform
import sys

print('作業系統：', platform.system(), platform.release())
print('處理器：', platform.machine())
print('Python 版本：', platform.python_version())
print('Python 路徑：', sys.executable)
print('正在虛擬環境：', sys.prefix != sys.base_prefix)
for package in ('setuptools', 'numpy', 'opencv-python', 'opencv-contrib-python',
                'opencv-python-headless', 'opencv-contrib-python-headless',
                'picamera2', 'ultralytics', 'torch', 'mediapipe', 'cvzone',
                'tflite-runtime', 'ai-edge-litert', 'Flask', 'pytesseract'):
    try:
        print(package + '：', version(package))
    except PackageNotFoundError:
        print(package + '：沒有查到套件版本紀錄')
for module in ('cv2', 'picamera2', 'libcamera', 'pkg_resources'):
    spec = find_spec(module)
    print(module + ' 模組位置：', spec.origin if spec else '找不到')
print('這份觀察不代表相機或辨識功能已測試成功。')
