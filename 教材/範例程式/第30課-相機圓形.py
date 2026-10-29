import cv2
import numpy as np

# shapes-board.png 由第 29 課的相機範例產生，是經透視校正的相機影像。
image = cv2.imread('shapes-board.png')
if image is None:
    raise RuntimeError('找不到 shapes-board.png，請先執行第 29 課相機輪廓範例')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 2)
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=150,
                           param1=100, param2=35, minRadius=80, maxRadius=160)
result = image.copy()
found = [] if circles is None else np.round(circles[0]).astype(int).tolist()
for x, y, radius in found:
    cv2.circle(result, (x, y), radius, (0, 255, 0), 4)
    cv2.circle(result, (x, y), 4, (0, 255, 0), -1)
if not cv2.imwrite('shapes-circles.png', result):
    raise RuntimeError('無法儲存影像')
print('input shape:', image.shape)
print('circles found:', len(found))
print('circles (x, y, radius):', found)
print('saved: shapes-circles.png')
