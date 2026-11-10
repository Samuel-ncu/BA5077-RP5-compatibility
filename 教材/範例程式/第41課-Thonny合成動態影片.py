from pathlib import Path
import time

import cv2
import numpy as np
from ultralytics import YOLO

folder = Path(__file__).resolve().parent
source = cv2.imread(str(folder / 'objects-board.png'))
if source is None:
    raise RuntimeError('Put objects-board.png next to the script')
for name in ('lesson41-moving-input.avi', 'lesson41-moving-output.avi'):
    if (folder / name).exists():
        raise FileExistsError('Use a new folder; output exists: ' + name)
frame_size = (480, 270)
base = cv2.resize(source, frame_size)
fps = 2.0
writer = cv2.VideoWriter(str(folder / 'lesson41-moving-input.avi'), cv2.VideoWriter_fourcc(*'MJPG'), fps, frame_size)
if not writer.isOpened():
    raise RuntimeError('Cannot create input video')
try:
    for i in range(24):
        shift = -35 + 3 * i
        matrix = np.float32([[1, 0, shift], [0, 1, 0]])
        writer.write(cv2.warpAffine(base, matrix, frame_size, borderValue=(255, 255, 255)))
finally:
    writer.release()

model = YOLO(str(folder / 'yolov8n.pt'))
video = cv2.VideoCapture(str(folder / 'lesson41-moving-input.avi'))
output = cv2.VideoWriter(str(folder / 'lesson41-moving-output.avi'), cv2.VideoWriter_fourcc(*'MJPG'), fps, frame_size)
if not video.isOpened() or not output.isOpened():
    video.release()
    output.release()
    raise RuntimeError('Cannot open video input or output')
count = 0
counts = []
first = last = None
start = time.monotonic()
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
        annotated = result.plot()
        output.write(annotated)
        counts.append(len(result.boxes))
        count += 1
        if first is None:
            first = annotated.copy()
        last = annotated.copy()
finally:
    video.release()
    output.release()
elapsed = time.monotonic() - start
if count != 24 or first is None or last is None:
    raise RuntimeError(f'Expected 24 frames, got {count}')
if not cv2.imwrite(str(folder / 'lesson41-moving-first-last.png'), cv2.hconcat([first, last])):
    raise RuntimeError('Cannot save comparison image')
check = cv2.VideoCapture(str(folder / 'lesson41-moving-output.avi'))
readback = 0
try:
    while True:
        ok, _ = check.read()
        if not ok:
            break
        readback += 1
finally:
    check.release()
print('generated frames:', 24)
print('playback FPS:', fps)
print('processed frames:', count)
print('first and last detections:', counts[0], counts[-1])
print('decoded output frames:', readback)
print('elapsed seconds:', round(elapsed, 2))
print('saved: lesson41-moving-output.avi, lesson41-moving-first-last.png')
