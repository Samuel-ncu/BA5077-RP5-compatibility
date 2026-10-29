import cv2
import numpy as np
from ultralytics import YOLO

path = 'lesson41-demo.avi'
writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), 5.0, (320, 240))
if not writer.isOpened():
    raise RuntimeError('VideoWriter could not open')
for _ in range(3):
    writer.write(np.zeros((240, 320, 3), dtype=np.uint8))
writer.release()
model = YOLO('yolov8n.pt')
results = list(model.predict(path, imgsz=320, device='cpu', stream=True, verbose=False))
print('frames processed', len(results))
