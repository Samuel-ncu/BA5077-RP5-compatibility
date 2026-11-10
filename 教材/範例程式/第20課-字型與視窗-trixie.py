from pathlib import Path
from tempfile import mkdtemp
import cv2
import numpy as np

folder = Path(mkdtemp(prefix='ba5077-lesson20-'))
image = np.full((600, 700, 3), 255, dtype=np.uint8)
fonts = [
    ('SIMPLEX', cv2.FONT_HERSHEY_SIMPLEX),
    ('PLAIN', cv2.FONT_HERSHEY_PLAIN),
    ('DUPLEX', cv2.FONT_HERSHEY_DUPLEX),
    ('COMPLEX', cv2.FONT_HERSHEY_COMPLEX),
    ('TRIPLEX', cv2.FONT_HERSHEY_TRIPLEX),
    ('COMPLEX_SMALL', cv2.FONT_HERSHEY_COMPLEX_SMALL),
    ('SCRIPT_SIMPLEX', cv2.FONT_HERSHEY_SCRIPT_SIMPLEX),
    ('SCRIPT_COMPLEX', cv2.FONT_HERSHEY_SCRIPT_COMPLEX),
]
for index, (name, font) in enumerate(fonts):
    cv2.putText(image, f'{name}: OpenCV', (15, 60 + index * 70), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
print('fonts drawn:', len(fonts))
print('saved:', cv2.imwrite(str(folder / 'fonts.png'), image))
print('folder:', folder)
cv2.namedWindow('Fonts', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Fonts', 700, 450)
cv2.imshow('Fonts', image)
print('Window open', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
