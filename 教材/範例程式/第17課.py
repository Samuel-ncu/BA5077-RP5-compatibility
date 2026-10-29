import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), -1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("color", image.shape)
print("grayscale", gray.shape, str(gray.dtype))
print("saved", cv2.imwrite("lesson17-gray.png", gray))
