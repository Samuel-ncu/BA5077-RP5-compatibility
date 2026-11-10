from pathlib import Path
import cv2
import numpy as np

folder = Path(__file__).resolve().parent
image = cv2.imread(str(folder / 'shapes-board.png'))
if image is None:
    raise RuntimeError('Put shapes-board.png beside this script')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 110, 80), (179, 255, 255))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large = sorted((c for c in contours if cv2.contourArea(c) > 4000),
               key=lambda c: cv2.boundingRect(c)[0])
annotated = image.copy()
for i, contour in enumerate(large, 1):
    cv2.drawContours(annotated, [contour], -1, (0, 0, 0), 3)
    x, y, w, h = cv2.boundingRect(contour)
    cv2.putText(annotated, str(i), (x, max(30, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
output = folder / 'lesson29-contours-result.png'
if not cv2.imwrite(str(output), annotated):
    raise RuntimeError('Cannot save result')
print('image shape:', image.shape)
print('large color contours:', len(large))
print('contour areas:', [round(cv2.contourArea(c), 1) for c in large])
print('saved:', output.name)
