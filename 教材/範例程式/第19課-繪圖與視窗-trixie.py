from pathlib import Path
from tempfile import mkdtemp
import cv2
import numpy as np

folder = Path(mkdtemp(prefix='ba5077-lesson19-'))
image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.line(image, (10, 20), (200, 20), (0, 255, 0), 3)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), 2)
cv2.circle(image, (240, 90), 40, (0, 0, 255), 3)
cv2.ellipse(image, (160, 190), (50, 20), 0, 0, 360, (255, 255, 255), 2)
points = np.array([[20, 150], [65, 135], [105, 160], [55, 225]], dtype=np.int32)
cv2.polylines(image, [points], True, (0, 255, 255), 2)
print('saved:', cv2.imwrite(str(folder / 'shapes.png'), image))
print('folder:', folder)
cv2.imshow('Shapes', image)
print('Window open', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
