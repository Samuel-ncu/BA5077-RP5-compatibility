import cv2

image = cv2.imread('objects-board.png')
if image is None:
    raise RuntimeError('找不到 objects-board.png')
# 固定座標只適用本次 1200 x 675 圖片，換圖時需重新選取。
x1, y1, x2, y2 = 150, 185, 390, 490
roi = image[y1:y2, x1:x2].copy()
if roi.size == 0:
    raise RuntimeError('ROI 為空，請檢查座標')
marked = image.copy()
cv2.rectangle(marked, (x1, y1), (x2-1, y2-1), (0, 255, 0), 3)
if not cv2.imwrite('lesson24-camera-roi.png', roi) or not cv2.imwrite('lesson24-camera-marked.png', marked):
    raise RuntimeError('圖片儲存失敗')
print('image shape:', image.shape)
print('ROI shape:', roi.shape)
print('saved: lesson24-camera-roi.png, lesson24-camera-marked.png')
