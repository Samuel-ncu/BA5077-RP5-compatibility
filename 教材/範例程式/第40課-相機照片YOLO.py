import cv2
import numpy as np
from ultralytics import YOLO

image = cv2.imread('objects-camera.jpg')
if image is None:
    raise RuntimeError('找不到 objects-camera.jpg，請先拍攝測試畫面')
if image.shape[:2] != (1080, 1920):
    raise RuntimeError('請使用 1920×1080 的照片，或依自己的照片重新設定座標')

# 下列座標只對應本次相機位置；換位置後必須在照片上重新量測。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [1199, 0], [1199, 674], [0, 674]])
board = cv2.warpPerspective(image, cv2.getPerspectiveTransform(source, target), (1200, 675))
model = YOLO('yolov8n.pt')
result = model.predict(board, imgsz=640, device='cpu', verbose=False)[0]
annotated = result.plot()
if not cv2.imwrite('objects-board.png', board) or not cv2.imwrite('objects-yolo.png', annotated):
    raise RuntimeError('無法儲存結果')
print('camera image:', image.shape)
print('rectified board:', board.shape)
print('detections:', len(result.boxes))
for box in result.boxes:
    cls = int(box.cls[0])
    print('class:', model.names[cls], 'confidence:', round(float(box.conf[0]), 3))
print('saved: objects-board.png, objects-yolo.png')
