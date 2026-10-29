from pathlib import Path
from urllib.request import urlopen
import hashlib
import shutil
import tarfile
import tempfile

model = Path('mobilenet.tflite')
labels = Path('labels.txt')
if model.exists() or labels.exists():
    raise RuntimeError('模型或標籤已存在，請改用新的練習資料夾')
model_url = 'https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224_quant.tgz'
labels_url = 'https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/lite/java/demo/app/src/main/assets/labels_mobilenet_quant_v1_224.txt'
print('Downloading model archive...', flush=True)
with tempfile.TemporaryFile() as archive_file:
    with urlopen(model_url, timeout=120) as response:
        shutil.copyfileobj(response, archive_file)
    archive_file.seek(0)
    with tarfile.open(fileobj=archive_file, mode='r:gz') as archive:
        member = archive.getmember('./mobilenet_v1_1.0_224_quant.tflite')
        with archive.extractfile(member) as source, model.open('xb') as target:
            shutil.copyfileobj(source, target)
print('Downloading labels...', flush=True)
with urlopen(labels_url, timeout=120) as response, labels.open('xb') as target:
    shutil.copyfileobj(response, target)
for path in (model, labels):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(path.name, 'bytes:', path.stat().st_size, 'sha256:', digest, flush=True)
print('Download complete.')
