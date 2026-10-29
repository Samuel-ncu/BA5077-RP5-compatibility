import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--rectified', action='store_true', help='讀取已校正的測試圖')
args = parser.parse_args()
if args.rectified:
    board = cv2.imread('concave-board.png')
    if board is None:
        raise RuntimeError('找不到 concave-board.png')
else:
    image = cv2.imread('concave-camera.jpg')
    if image is None or image.shape[:2] != (1080, 1920):
        raise RuntimeError('請準備 1920×1080 的 concave-camera.jpg')
    # 以下四角只適用本次相機位置，其他照片須重新量測。
    source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
    target = np.float32([[0, 0], [799, 0], [799, 449], [0, 449]])
    board = cv2.warpPerspective(image, cv2.getPerspectiveTransform(source, target), (800, 450))
    if not cv2.imwrite('concave-board.png', board):
        raise RuntimeError('無法儲存校正圖片')
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
    raise RuntimeError('找不到輪廓，請檢查相機畫面、座標及閾值')
contour = max(contours, key=cv2.contourArea)
hull = cv2.convexHull(contour, returnPoints=False)
defects = cv2.convexityDefects(contour, hull)
deep = [] if defects is None else [d for d in defects if d[0][3] / 256.0 > 10]
cv2.drawContours(board, [cv2.convexHull(contour)], -1, (0, 255, 0), 3)
for defect in deep:
    far_index = defect[0][2]
    x, y = (int(v) for v in contour[far_index, 0])
    cv2.circle(board, (x, y), 8, (0, 0, 255), -1)
if not cv2.imwrite('lesson35-camera-hull.png', board):
    raise RuntimeError('無法儲存結果')
print('hull vertices:', len(hull))
print('defects deeper than 10 pixels:', len(deep))
print('saved: lesson35-camera-hull.png')
