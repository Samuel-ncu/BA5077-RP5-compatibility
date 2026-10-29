import cv2
import numpy as np

image = np.zeros((120, 160, 3), dtype=np.uint8)
cv2.circle(image, (80, 60), 30, (0, 255, 0), -1)
print('OpenCV version:', cv2.__version__)
print('Image shape:', image.shape)
print('Center BGR:', image[60, 80].tolist())
