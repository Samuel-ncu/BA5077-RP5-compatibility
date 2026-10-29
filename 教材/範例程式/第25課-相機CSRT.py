import time
import cv2
import numpy as np
from picamera2 import Picamera2

# 以本次相機的 1920×1080 照片量測螢幕四角；不同位置須重新設定。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [599, 0], [599, 337], [0, 337]])
matrix = cv2.getPerspectiveTransform(source, target)
camera = Picamera2()
results, panels = [], []
try:
    camera.configure(camera.create_still_configuration(main={'size': (1920, 1080), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    tracker = cv2.TrackerCSRT_create()
    for index in range(8):
        frame = camera.capture_array()
        board = cv2.warpPerspective(frame, matrix, (600, 338))
        if index == 0:
            hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (0, 130, 100), (10, 255, 255)) | cv2.inRange(hsv, (170, 130, 100), (179, 255, 255))
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            candidates = [c for c in contours if cv2.contourArea(c) > 300]
            if not candidates:
                raise RuntimeError('第一張影格找不到紅色目標')
            box = cv2.boundingRect(max(candidates, key=cv2.contourArea))
            tracker.init(board, box)
            success = True
        else:
            success, box = tracker.update(board)
        results.append(bool(success))
        if success:
            x, y, w, h = (int(v) for v in box)
            cv2.rectangle(board, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(board, f'frame {index+1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        if index in (0, 3, 7):
            panels.append(board)
        time.sleep(0.2)
finally:
    camera.stop()
    camera.close()

if not cv2.imwrite('lesson25-csrt.png', cv2.hconcat(panels)):
    raise RuntimeError('無法儲存結果圖')
print('frames captured:', len(results))
print('initial target found:', results[0])
print('update results:', results[1:])
print('saved: lesson25-csrt.png')
