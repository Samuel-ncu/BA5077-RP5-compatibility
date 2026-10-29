from pathlib import Path
from urllib.request import urlopen
import shutil

files = {
    'yolov4-tiny.cfg': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg',
    'yolov4-tiny.weights': 'https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4-tiny.weights',
    'coco.names': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names',
}
for name, url in files.items():
    path = Path(name)
    if path.exists():
        raise RuntimeError(f'檔案已存在，請改用新的練習資料夾：{path}')
    print('Downloading:', name, flush=True)
    with urlopen(url, timeout=120) as response, path.open('xb') as target:
        shutil.copyfileobj(response, target)
    print('Saved:', name, 'bytes:', path.stat().st_size, flush=True)
print('Download complete.', flush=True)
