import cv2
import numpy as np
path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(path)
if cascade.empty():
    raise RuntimeError('cascade could not be loaded')
image = np.zeros((240, 320), dtype=np.uint8)
faces = cascade.detectMultiScale(image, 1.1, 3)
print('cascade loaded', not cascade.empty())
print('faces on blank image', len(faces))
