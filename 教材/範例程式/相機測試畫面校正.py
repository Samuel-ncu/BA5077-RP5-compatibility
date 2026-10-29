import cv2
import numpy as np

image = cv2.imread('facehand-camera.jpg')
if image is None:
    raise RuntimeError('找不到 facehand-camera.jpg')
if image.shape[:2] != (1080, 1920):
    raise RuntimeError('請使用 1920×1080 照片，或重新設定座標')
# 此四點對應本次相機位置，其他拍攝位置須自行量測。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [1199, 0], [1199, 674], [0, 674]])
board = cv2.warpPerspective(image, cv2.getPerspectiveTransform(source, target), (1200, 675))
if not cv2.imwrite('facehand-board.png', board):
    raise RuntimeError('無法儲存結果')
print('camera shape:', image.shape)
print('rectified board:', board.shape)
print('saved: facehand-board.png')
