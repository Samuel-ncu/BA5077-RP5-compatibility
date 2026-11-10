from pathlib import Path
import subprocess

target = Path('/home/pi/ba5077-camera-contrib-trixie-20261110')
if target.exists():
    raise RuntimeError('Choose a new environment folder')
subprocess.run(['/usr/bin/python3', '-m', 'venv', '--system-site-packages', str(target)], check=True)
subprocess.run([str(target / 'bin/python3'), '-m', 'pip', 'install', 'numpy==2.2.4', 'opencv-contrib-python==4.12.0.88'], check=True)
print('Environment ready:', target, flush=True)
