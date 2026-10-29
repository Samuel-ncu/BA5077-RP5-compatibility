import time
from pathlib import Path
import cv2
from ultralytics import YOLO

for name in ('repeat-120s-input.avi', 'repeat-120s-output.avi'):
    if Path(name).exists():
        raise FileExistsError(f'{name} 已存在，請先使用新的練習資料夾')

source = cv2.VideoCapture('lesson42-input.avi')
if not source.isOpened():
    raise RuntimeError('找不到 lesson42-input.avi')
frames = []
while True:
    ok, frame = source.read()
    if not ok:
        break
    frames.append(frame)
source.release()
if len(frames) != 4:
    raise RuntimeError('本練習預期 4 張來源影格')
height, width = frames[0].shape[:2]
fps = 3.0
writer = cv2.VideoWriter('repeat-120s-input.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
if not writer.isOpened():
    raise RuntimeError('無法建立輸入影片')
for i in range(360):
    writer.write(frames[i % len(frames)])
writer.release()
print('input: repeated four frames', flush=True)
print('input frames: 360', flush=True)
print('playback FPS: 3.0', flush=True)
print('input duration seconds: 120.0', flush=True)

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('repeat-120s-input.avi')
output = cv2.VideoWriter('repeat-120s-output.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
if not video.isOpened() or not output.isOpened():
    video.release()
    output.release()
    raise RuntimeError('無法讀取或建立影片')
count = 0
start = time.perf_counter()
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
        output.write(result.plot())
        count += 1
        if count % 90 == 0:
            print('processed:', count, flush=True)
finally:
    video.release()
    output.release()
elapsed = time.perf_counter() - start
check = cv2.VideoCapture('repeat-120s-output.avi')
readback = 0
while True:
    ok, _ = check.read()
    if not ok:
        break
    readback += 1
check.release()
print('processed frames:', count)
print('processing seconds:', round(elapsed, 2))
print('processing FPS:', round(count / elapsed, 2))
print('decoded output frames:', readback)
print('output playback seconds:', round(readback / fps, 2))
