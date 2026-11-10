from pathlib import Path
import cv2
import numpy as np

folder = Path('/tmp/ba5077-lesson23-FcArl6')
image = cv2.imread(str(folder / 'facehand-board.png'))
if image is None:
    raise RuntimeError('Cannot read image')
model = Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(str(model))
if cascade.empty():
    raise RuntimeError('Cannot load Haar model')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
print('face candidates:', len(faces))
if len(faces) != 1:
    raise RuntimeError('Expected one face in the practice image')
x, y, w, h = faces[0]
face = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train([face], np.array([0], dtype=np.int32))
label, distance = recognizer.predict(face)
print('training images:', 1)
print('predicted label:', label)
print('distance:', round(distance, 4))
cv2.imshow('Training face', face)
print('Window open', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
