from pathlib import Path
import cv2
import numpy as np

folder = Path('/tmp/ba5077-lesson22-SKocIi')
image = cv2.imread(str(folder / 'facehand-board.png'))
if image is None:
    raise RuntimeError('Cannot read image; check path')
model = Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(str(model))
if cascade.empty():
    raise RuntimeError('Cannot load Haar model')
blank = np.zeros((240, 320), dtype=np.uint8)
print('blank faces:', len(cascade.detectMultiScale(blank, 1.1, 5)))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
print('faces found:', len(faces))
print('saved:', cv2.imwrite(str(folder / 'face-result.png'), image))
cv2.namedWindow('Face detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Face detection', 700, 400)
cv2.imshow('Face detection', image)
print('Window open', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
