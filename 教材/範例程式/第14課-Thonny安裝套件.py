import subprocess
import sys

print('Python:', sys.executable, flush=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', 'numpy==1.26.4', 'opencv-python==4.10.0.84'], check=True)
print('Installation completed. Restart Thonny interpreter before testing.', flush=True)
