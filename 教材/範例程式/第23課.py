import cv2
import numpy as np
images = [np.full((100, 100), 40, dtype=np.uint8), np.full((100, 100), 200, dtype=np.uint8)]
labels = np.array([0, 1], dtype=np.int32)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, labels)
label, confidence = recognizer.predict(images[0])
print('LBPH trained', True)
print('predicted label', label)
