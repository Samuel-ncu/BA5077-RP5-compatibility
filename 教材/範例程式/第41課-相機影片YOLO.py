import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('lesson42-input.avi')
writer = None
counts, first_result = [], None
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        if writer is None:
            height, width = frame.shape[:2]
            writer = cv2.VideoWriter('lesson41-detected.avi', cv2.VideoWriter_fourcc(*'MJPG'), 3, (width, height))
            if not writer.isOpened():
                raise RuntimeError('無法建立輸出影片')
        result = model.predict(frame, imgsz=640, device='cpu', verbose=False)[0]
        annotated = result.plot()
        writer.write(annotated)
        counts.append(len(result.boxes))
        if first_result is None:
            first_result = annotated.copy()
finally:
    video.release()
    if writer is not None:
        writer.release()
if not counts or first_result is None:
    raise RuntimeError('輸入影片沒有讀取到影格')
if not cv2.imwrite('lesson41-detected-frame.png', first_result):
    raise RuntimeError('無法儲存結果圖')
print('frames processed:', len(counts))
print('detections per frame:', counts)
print('saved: lesson41-detected.avi, lesson41-detected-frame.png')
