from pathlib import Path
import cv2
import numpy as np

folder = Path(__file__).resolve().parent
centers = []
panels = []
for index in range(6):
    image = np.full((180, 320, 3), 235, dtype=np.uint8)
    left = 30 + index * 35
    cv2.rectangle(image, (left, 65), (left + 29, 94), (0, 0, 255), -1)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
    high = cv2.inRange(hsv, (170, 100, 100), (179, 255, 255))
    mask = cv2.bitwise_or(low, high)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = [c for c in contours if cv2.contourArea(c) >= 100]
    if not candidates:
        centers.append(None)
        continue
    x, y, w, h = cv2.boundingRect(max(candidates, key=cv2.contourArea))
    centers.append((x + w // 2, y + h // 2))
    cv2.rectangle(image, (x, y), (x + w - 1, y + h - 1), (0, 180, 0), 2)
    cv2.putText(image, f'frame {index + 1}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1)
    panels.append(image)
if len(panels) != 6:
    raise RuntimeError('Some generated frames did not contain a red region')
output = folder / 'lesson28-generated-motion.png'
if not cv2.imwrite(str(output), cv2.vconcat([cv2.hconcat(panels[:3]), cv2.hconcat(panels[3:])])):
    raise RuntimeError('Could not save result')
print('frames:', len(centers))
print('red detections:', sum(center is not None for center in centers))
print('centers:', centers)
print('saved:', output.name)
