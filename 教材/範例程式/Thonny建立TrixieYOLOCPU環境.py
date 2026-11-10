from pathlib import Path
import subprocess

folder = Path('/home/pi/ba5077-yolov8-cpu-trixie-20261110')
if folder.exists():
    raise RuntimeError('Environment folder already exists; choose another')
subprocess.run(['/usr/bin/python3', '-m', 'venv', str(folder)], check=True)
python = str(folder / 'bin/python3')
subprocess.run([python, '-m', 'pip', 'install', 'torch==2.15.0+cpu', 'torchvision==0.29.2+cpu', '--index-url', 'https://download.pytorch.org/whl/cpu'], check=True)
subprocess.run([python, '-m', 'pip', 'install', 'ultralytics'], check=True)
print('Environment ready:', folder, flush=True)
