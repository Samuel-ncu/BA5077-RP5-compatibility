import subprocess
import sys
import platform

print('Python:', sys.executable, flush=True)
print('Version:', sys.version.split()[0], flush=True)
print('Architecture:', platform.machine(), flush=True)
if sys.version_info[:2] != (3, 13) or platform.machine() != 'aarch64':
    raise RuntimeError('This installation path is verified for Python 3.13 on 64-bit Raspberry Pi OS Trixie.')
subprocess.run([sys.executable, '-m', 'pip', 'install', 'numpy==2.2.4', 'opencv-python==4.12.0.88'], check=True)
print('Installation completed. Restart Thonny interpreter before testing.', flush=True)
