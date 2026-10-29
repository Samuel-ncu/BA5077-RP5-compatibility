import cv2
import numpy as np
image = np.zeros((200, 200), dtype=np.uint8)
cv2.circle(image, (100, 100), 40, 255, 3)
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 30, param1=100, param2=20, minRadius=30, maxRadius=50)
result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
if circles is not None:
    for x, y, radius in np.round(circles[0]).astype(int):
        cv2.circle(result, (x, y), radius, (0, 0, 255), 2)
if not cv2.imwrite('lesson30-circle.png', result):
    raise RuntimeError('image save failed')
print('circle detected', circles is not None)
