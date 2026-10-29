import time
import cv2
import numpy as np
from picamera2 import Picamera2

# 本次相機位置的測試圖四角；不同位置或尺寸須重新量測。
source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [599, 0], [599, 337], [0, 337]])
matrix = cv2.getPerspectiveTransform(source, target)
camera = Picamera2()
writer = None
panels = []
written = 0
try:
    camera.configure(camera.create_still_configuration(main={'size': (1920, 1080), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    writer = cv2.VideoWriter('lesson16-camera.avi', cv2.VideoWriter_fourcc(*'MJPG'), 5, (600, 338))
    if not writer.isOpened():
        raise RuntimeError('無法建立 MJPG 影片')
    for index in range(12):
        frame = camera.capture_array()
        board = cv2.warpPerspective(frame, matrix, (600, 338))
        gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.putText(processed, f'frame {index+1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        writer.write(processed)
        written += 1
        if index in (0, 5, 11):
            panels.append(processed)
        time.sleep(0.2)
finally:
    if writer is not None:
        writer.release()
    camera.stop()
    camera.close()

video = cv2.VideoCapture('lesson16-camera.avi')
read_count = 0
first_shape = None
try:
    while True:
        ok, image = video.read()
        if not ok:
            break
        if first_shape is None:
            first_shape = image.shape
        read_count += 1
finally:
    video.release()
if not cv2.imwrite('lesson16-frames.png', cv2.hconcat(panels)):
    raise RuntimeError('無法儲存結果圖')
print('frames written:', written)
print('frames read:', read_count)
print('first video frame:', first_shape)
print('saved: lesson16-camera.avi, lesson16-frames.png')
