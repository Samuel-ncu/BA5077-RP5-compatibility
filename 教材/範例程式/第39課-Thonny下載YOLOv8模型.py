from pathlib import Path
from urllib.request import urlopen
import shutil

path = Path('yolov8n.pt')
url = 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt'
if path.exists():
    raise RuntimeError(f'檔案已存在，請改用新的練習資料夾：{path}')
print('Downloading:', path.name, flush=True)
with urlopen(url, timeout=120) as response, path.open('xb') as target:
    shutil.copyfileobj(response, target)
print('Saved:', path.name, 'bytes:', path.stat().st_size, flush=True)
print('Download complete.', flush=True)
