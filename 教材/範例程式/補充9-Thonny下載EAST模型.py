from pathlib import Path
from urllib.request import urlopen, Request
import hashlib

url = 'https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb'
target = Path('east-download-check.pb')
if target.exists():
    raise FileExistsError('east-download-check.pb 已存在，請使用新的練習資料夾')
h = hashlib.sha256()
size = 0
print('Downloading EAST model...', flush=True)
with urlopen(Request(url, headers={'User-Agent': 'BA5077-Thonny'}), timeout=120) as source:
    with target.open('xb') as dest:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            dest.write(chunk)
            h.update(chunk)
            size += len(chunk)
print('bytes:', size)
print('sha256:', h.hexdigest())
print('saved:', target)
