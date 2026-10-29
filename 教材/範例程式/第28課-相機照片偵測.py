import cv2
import numpy as np

# 先使用 rpicam-still 拍攝 lesson28-camera.jpg，再依實際畫面調整 ROI。
image = cv2.imread('lesson28-camera.jpg')
if image is None:
    raise RuntimeError('找不到 lesson28-camera.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 130, 100), (10, 255, 255)) | cv2.inRange(hsv, (170, 130, 100), (179, 255, 255))
# 本次相機為 1920×1080；這個 ROI 是此次拍攝螢幕的範圍。
mask[:200, :] = 0
mask[600:, :] = 0
mask[:, :700] = 0
mask[:, 1500:] = 0
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = [c for c in contours if cv2.contourArea(c) >= 1000]
if not contours:
    raise RuntimeError('沒有找到夠大的紅色區域；請調整 ROI 與 HSV 範圍')
contour = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(contour)
margin = 30
x0, y0 = max(0, x - margin), max(0, y - margin)
x1, y1 = min(image.shape[1], x + w + margin), min(image.shape[0], y + h + margin)
sample = image[y0:y1, x0:x1].copy()
cv2.rectangle(sample, (x-x0, y-y0), (x-x0+w-1, y-y0+h-1), (0, 255, 0), 2)
panel = np.hstack((sample, cv2.cvtColor(mask[y0:y1, x0:x1], cv2.COLOR_GRAY2BGR)))
if not cv2.imwrite('lesson28-camera-mask.png', panel):
    raise RuntimeError('無法儲存結果圖片')
print('input camera image:', image.shape)
print('large red regions:', len(contours))
print('largest red box (x, y, w, h):', x, y, w, h)
print('largest red contour area:', round(cv2.contourArea(contour), 1))
print('result: lesson28-camera-mask.png')
