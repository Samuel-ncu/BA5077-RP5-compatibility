from pathlib import Path
import subprocess
import sys
import venv

target = Path('/home/pi/ba5077-contrib-20261029')
if target.exists():
    raise RuntimeError('目標資料夾已存在，請更換新資料夾名稱')
print('Creating isolated environment:', target, flush=True)
venv.create(target, with_pip=True)
python = target / 'bin' / 'python3'
subprocess.run([str(python), '-m', 'pip', 'install', 'numpy==1.26.4', 'opencv-contrib-python==4.11.0.86'], check=True)
print('Installation completed:', python, flush=True)
print('Select this interpreter in Thonny and restart the backend.', flush=True)
