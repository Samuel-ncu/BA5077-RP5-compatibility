from pathlib import Path
import subprocess
import venv

folder = Path.home() / 'ba5077-tflite-camera-20261029'
if folder.exists():
    raise FileExistsError(f'{folder} 已存在，請更改資料夾名稱後重新執行')
print('creating:', folder, flush=True)
print('Inherit Raspberry Pi OS system packages for Picamera2 and OpenCV', flush=True)
venv.EnvBuilder(with_pip=True, system_site_packages=True).create(folder)
python = folder / 'bin' / 'python'
subprocess.run([str(python), '-m', 'pip', 'install',
                'numpy==1.26.4', 'tflite-runtime==2.14.0'], check=True)
print('Environment created:', python, flush=True)
