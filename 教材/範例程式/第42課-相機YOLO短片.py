import time
import cv2
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO

source = np.float32([[755, 270], [1385, 65], [1484, 412], [856, 604]])
target = np.float32([[0, 0], [799, 0], [799, 449], [0, 449]])
matrix = cv2.getPerspectiveTransform(source, target)
model = YOLO('yolov8n.pt')
camera = Picamera2()
writer = None
source_writer = None
panels, detected = [], []
try:
    camera.configure(camera.create_still_configuration(main={'size': (1920, 1080), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    writer = cv2.VideoWriter('lesson42-yolo.avi', cv2.VideoWriter_fourcc(*'MJPG'), 3, (800, 450))
    source_writer = cv2.VideoWriter('lesson42-input.avi', cv2.VideoWriter_fourcc(*'MJPG'), 3, (800, 450))
    if not writer.isOpened() or not source_writer.isOpened():
        raise RuntimeError('無法建立 MJPG 影片')
    start = time.perf_counter()
    for index in range(4):
        frame = camera.capture_array()
        board = cv2.warpPerspective(frame, matrix, (800, 450))
        source_writer.write(board)
        result = model.predict(board, imgsz=640, device='cpu', verbose=False)[0]
        labels = [model.names[int(box.cls[0])] for box in result.boxes]
        detected.append(labels)
        annotated = result.plot()
        cv2.putText(annotated, f'frame {index+1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        writer.write(annotated)
        if index in (0, 3):
            panels.append(annotated)
    elapsed = time.perf_counter() - start
finally:
    if writer is not None:
        writer.release()
    if source_writer is not None:
        source_writer.release()
    camera.stop()
    camera.close()

video = cv2.VideoCapture('lesson42-yolo.avi')
read_count = 0
try:
    while True:
        ok, _ = video.read()
        if not ok:
            break
        read_count += 1
finally:
    video.release()
if not cv2.imwrite('lesson42-yolo-frames.png', cv2.hconcat(panels)):
    raise RuntimeError('無法儲存圖片')
print('frames processed:', len(detected))
print('detected classes per frame:', detected)
print('frames read from video:', read_count)
print('elapsed seconds:', round(elapsed, 2))
print('observed loop FPS:', round(len(detected) / elapsed, 2))
print('saved: lesson42-input.avi, lesson42-yolo.avi, lesson42-yolo-frames.png')
