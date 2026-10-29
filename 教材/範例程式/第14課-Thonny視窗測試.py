import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.circle(image, (160, 120), 60, (0, 255, 0), -1)
print('Opening image window', flush=True)
cv2.namedWindow('Thonny OpenCV test')
cv2.moveWindow('Thonny OpenCV test', 550, 360)
cv2.imshow('Thonny OpenCV test', image)
cv2.waitKey(30000)
cv2.destroyAllWindows()
print('Window closed', flush=True)
