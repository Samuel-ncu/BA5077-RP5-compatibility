from pathlib import Path
import subprocess
import sys
import venv

target = Path.home() / 'ba5077-tflite-clean-20261029'
if target.exists():
    raise RuntimeError(f'目標已存在，請改用新的環境資料夾：{target}')
print('Creating:', target, flush=True)
venv.EnvBuilder(with_pip=True).create(target)
python = target / 'bin' / 'python3'
subprocess.run([str(python), '-m', 'pip', 'install',
                'numpy==1.26.4', 'opencv-python==4.10.0.84',
                'tflite-runtime==2.14.0'], check=True)
print('Installation completed:', python, flush=True)
print('Choose this interpreter in Thonny and restart the backend.', flush=True)
