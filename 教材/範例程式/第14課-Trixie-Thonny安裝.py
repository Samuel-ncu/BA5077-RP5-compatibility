"""第 14 課：在選定的 Thonny 虛擬環境安裝 OpenCV。"""
import subprocess
import sys

print("Python:", sys.executable, flush=True)
packages = ["setuptools==80.9.0", "numpy==2.2.6", "opencv-python==4.12.0.88"]
subprocess.run([sys.executable, "-m", "pip", "install", *packages], check=True)
print("Installation completed. Restart the Thonny interpreter.", flush=True)
