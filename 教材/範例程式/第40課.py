from ultralytics import YOLO
import numpy as np

model = YOLO('yolov8n.pt')
image = np.zeros((320, 320, 3), dtype=np.uint8)
results = model.predict(image, imgsz=320, device='cpu', verbose=False)
print('results', len(results))
print('boxes', len(results[0].boxes))
