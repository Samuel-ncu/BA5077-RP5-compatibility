import time
import cv2
import numpy as np
from picamera2 import Picamera2

# 此座標對應本次 1920×1080 相機畫面中的螢幕；移動設備後須重新量測。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [599, 0], [599, 337], [0, 337]])
matrix = cv2.getPerspectiveTransform(source, target)
camera = Picamera2()
panels, centers = [], []
try:
    camera.configure(camera.create_still_configuration(main={'size': (1920, 1080), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    for index in range(6):
        frame = camera.capture_array()
        board = cv2.warpPerspective(frame, matrix, (600, 338))
        hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 130, 100), (10, 255, 255))
        mask |= cv2.inRange(hsv, (170, 130, 100), (179, 255, 255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = [c for c in contours if cv2.contourArea(c) > 300]
        if candidates:
            x, y, w, h = cv2.boundingRect(max(candidates, key=cv2.contourArea))
            centers.append((x + w // 2, y + h // 2))
            cv2.rectangle(board, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            centers.append(None)
        cv2.putText(board, f'frame {index+1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        if index in (0, 2, 5):
            panels.append(board)
        time.sleep(0.5)
finally:
    camera.stop()
    camera.close()

if not cv2.imwrite('lesson28-motion.png', cv2.hconcat(panels)):
    raise RuntimeError('無法儲存結果圖')
print('frames captured:', len(centers))
print('red detections:', sum(point is not None for point in centers))
print('centers (x, y):', centers)
print('saved: lesson28-motion.png')
