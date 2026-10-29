from pathlib import Path
from urllib.request import urlopen
import shutil

files = {
    'opencv_face_detector.pbtxt': 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/opencv_face_detector.pbtxt',
    'opencv_face_detector_uint8.pb': 'https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180220_uint8/opencv_face_detector_uint8.pb',
}
for name, url in files.items():
    path = Path(name)
    if path.exists():
        raise RuntimeError(f'檔案已存在，請改用新的練習資料夾：{path}')
    print('Downloading:', name, flush=True)
    with urlopen(url, timeout=60) as response, path.open('xb') as target:
        shutil.copyfileobj(response, target)
    print('Saved:', name, 'bytes:', path.stat().st_size, flush=True)
print('Download complete.', flush=True)
