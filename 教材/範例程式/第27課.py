import cv2
import numpy as np
subtractor = cv2.bgsegm.createBackgroundSubtractorGMG()
frame = np.zeros((40, 40, 3), dtype=np.uint8)
mask = subtractor.apply(frame)
print('GMG created', True)
print('mask shape', mask.shape)
