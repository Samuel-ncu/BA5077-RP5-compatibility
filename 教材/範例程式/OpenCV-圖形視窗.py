import sys
import cv2

if len(sys.argv) != 2:
    raise SystemExit('用法：python3 OpenCV-圖形視窗.py 圖片檔名')
image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
if image is None:
    raise SystemExit('無法讀取圖片，請檢查路徑')
print('image shape:', image.shape, flush=True)
cv2.imshow('OpenCV image - press any key', image)
print('window opened; press any key or wait 60 seconds', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('window closed', flush=True)
