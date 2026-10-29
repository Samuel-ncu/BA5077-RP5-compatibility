import cv2
import numpy as np

image = cv2.imread('shapes-camera.jpg')
if image is None:
    raise RuntimeError('找不到 shapes-camera.jpg；請先拍照')
if image.shape[:2] != (1080, 1920):
    raise RuntimeError('請使用 1920×1080 的照片，或依自己的影像重新設定座標')

# 此四點對應本次相機位置下白色測試畫面的內部；換位置後須重新量測。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [1199, 0], [1199, 674], [0, 674]])
matrix = cv2.getPerspectiveTransform(source, target)
board = cv2.warpPerspective(image, matrix, (1200, 675))
hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 110, 80), (179, 255, 255))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large = sorted((c for c in contours if cv2.contourArea(c) > 4000), key=lambda c: cv2.boundingRect(c)[0])
annotated = board.copy()
for i, contour in enumerate(large, 1):
    cv2.drawContours(annotated, [contour], -1, (0, 0, 0), 3)
    x, y, w, h = cv2.boundingRect(contour)
    cv2.putText(annotated, str(i), (x, max(30, y-10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
if not cv2.imwrite('shapes-board.png', board) or not cv2.imwrite('shapes-contours.png', annotated):
    raise RuntimeError('無法儲存影像')
print('camera image:', image.shape)
print('rectified board:', board.shape)
print('large color contours:', len(large))
print('contour areas:', [round(cv2.contourArea(c), 1) for c in large])
print('saved: shapes-board.png, shapes-contours.png')
