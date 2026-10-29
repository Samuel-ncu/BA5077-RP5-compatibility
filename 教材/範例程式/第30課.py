import cv2
import numpy as np
image = np.zeros((200, 200), dtype=np.uint8)
cv2.circle(image, (100, 100), 40, 255, 3)
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 30, param1=100, param2=20, minRadius=30, maxRadius=50)
print('circle detected', circles is not None)
