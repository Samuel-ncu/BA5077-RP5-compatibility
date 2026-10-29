import cv2
import numpy as np

image = cv2.imread('shapes-board.png')
if image is None:
    raise RuntimeError('找不到第 29 課產生的 shapes-board.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 110, 80), (179, 255, 255))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large = sorted((c for c in contours if cv2.contourArea(c) > 4000), key=lambda c: cv2.boundingRect(c)[0])
vertices = []
for contour in large:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    vertices.append(len(approx))
    cv2.polylines(image, [approx], True, (0, 0, 0), 4)
    for point in approx[:, 0]:
        cv2.circle(image, tuple(int(x) for x in point), 6, (0, 255, 255), -1)
if not cv2.imwrite('lesson34-camera-polygons.png', image):
    raise RuntimeError('無法儲存結果')
print('contours:', len(large))
print('polygon vertex counts:', vertices)
print('saved: lesson34-camera-polygons.png')
