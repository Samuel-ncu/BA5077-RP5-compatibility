from pathlib import Path
import cv2

folder = Path('/tmp/ba5077-lesson17-tPp3k0')
image = cv2.imread(str(folder / 'objects-board.png'), cv2.IMREAD_GRAYSCALE)
if image is None:
    raise RuntimeError('Cannot read image; check path')
print('gray shape:', image.shape)
print('gray dtype:', image.dtype)
print('saved:', cv2.imwrite(str(folder / 'gray-output.png'), image))
cv2.namedWindow('Gray image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Gray image', 800, 450)
cv2.imshow('Gray image', image)
print('Window open: press any key or wait 60 seconds', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
