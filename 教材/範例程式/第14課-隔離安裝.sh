#!/bin/bash
set -euo pipefail
printf 'Create isolated Python environment\n'
python3 -m venv /tmp/ba5077-install-screen-test
source /tmp/ba5077-install-screen-test/bin/activate
printf 'Install verified package versions\n'
python -m pip install --disable-pip-version-check --progress-bar off 'numpy==1.26.4' 'opencv-python-headless==4.10.0.84'
printf '\nCheck dependencies and import\n'
python -m pip check
python -c "import cv2,numpy; print('OpenCV:',cv2.__version__); print('NumPy:',numpy.__version__); print('SIFT:',hasattr(cv2,'SIFT_create'))"
printf 'Installation test completed.\n'
sleep 90
