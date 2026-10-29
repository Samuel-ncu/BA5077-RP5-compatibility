from pathlib import Path
import math
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
output = Path('two-hands-mirror-result.png')
if output.exists():
    raise FileExistsError('結果已存在，請先使用新練習資料夾')
# One AI-generated hand, cropped then mirrored: artificial test pair.
hand = image[100:650, 720:1100]
pair = np.hstack((cv2.flip(hand, 1), hand))
blank = np.full_like(pair, 255)
detector = HandDetector(staticMode=True, maxHands=2, detectionCon=0.5)
none, _ = detector.findHands(blank, draw=False, flipType=False)
print('blank hands:', len(none))
hands, annotated = detector.findHands(pair.copy(), draw=True, flipType=False)
print('synthetic pair hands:', len(hands))
for index, item in enumerate(hands):
    print('hand', index + 1, 'landmarks:', len(item['lmList']))
if len(hands) == 2:
    p1 = hands[0]['lmList'][8][:2]
    p2 = hands[1]['lmList'][8][:2]
    distance = math.dist(p1, p2)
    cv2.line(annotated, tuple(p1), tuple(p2), (255, 0, 255), 2)
    print('index fingertips:', p1, p2)
    print('distance pixels:', round(distance, 2))
    if not cv2.imwrite(str(output), annotated):
        raise RuntimeError('無法儲存結果圖片')
    print('saved:', output)
else:
    print('distance unavailable: need exactly two hands')
