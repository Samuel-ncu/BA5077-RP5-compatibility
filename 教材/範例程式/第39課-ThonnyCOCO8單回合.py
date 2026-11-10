from pathlib import Path
import os

folder = Path(__file__).resolve().parent
config = folder / 'ultralytics-config'
config.mkdir(exist_ok=True)
os.environ['YOLO_CONFIG_DIR'] = str(config)

from ultralytics import YOLO, settings
import torch
import ultralytics

settings.update({'datasets_dir': str(folder / 'datasets'), 'sync': False})
print('Ultralytics:', ultralytics.__version__, flush=True)
print('PyTorch:', torch.__version__, 'CUDA available:', torch.cuda.is_available(), flush=True)
model = YOLO(str(folder / 'yolov8n.pt'))
print('class count:', len(model.names), 'class 0:', model.names[0], flush=True)
results = model.train(data='coco8.yaml', epochs=1, imgsz=320, batch=1,
                      workers=0, device='cpu', amp=False, plots=False,
                      project=str(folder / 'runs'), name='coco8-one-epoch', exist_ok=False)
save_dir = Path(model.trainer.save_dir)
print('training directory:', save_dir, flush=True)
print('best weights exist:', (save_dir / 'weights' / 'best.pt').is_file(), flush=True)
print('last weights exist:', (save_dir / 'weights' / 'last.pt').is_file(), flush=True)

