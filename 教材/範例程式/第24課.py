import numpy as np
image = np.zeros((240, 320, 3), dtype=np.uint8)
roi = image[30:110, 50:150]
print('image', image.shape)
print('ROI', roi.shape)
