from pathlib import Path
import os
folder = Path(__file__).resolve().parent
os.environ['YOLO_CONFIG_DIR'] = str(folder / 'ultralytics-config')
from ultralytics import YOLO

weights = folder / 'runs/coco8-one-epoch/weights/best.pt'
image = folder / 'datasets/coco8/images/val/000000000036.jpg'
model = YOLO(str(weights))
results = model.predict(source=str(image), imgsz=320, device='cpu', verbose=False, save=False)
print('weights loaded:', weights.is_file())
print('images processed:', len(results))
print('image shape:', results[0].orig_shape)
print('detections:', len(results[0].boxes))
print('classes:', [results[0].names[int(c)] for c in results[0].boxes.cls])
