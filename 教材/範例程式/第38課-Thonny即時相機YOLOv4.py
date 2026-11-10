from pathlib import Path
import time

import cv2
import numpy as np
from picamera2 import Picamera2

folder = Path(__file__).resolve().parent
names = (folder / 'coco.names').read_text(encoding='utf-8').splitlines()
net = cv2.dnn.readNetFromDarknet(str(folder / 'yolov4-tiny.cfg'), str(folder / 'yolov4-tiny.weights'))
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
camera = Picamera2()
frames = 0
last_labels = []
started = time.monotonic()
try:
    camera.configure(camera.create_preview_configuration(main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    while time.monotonic() - started < 30:
        frame = camera.capture_array()
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())
        boxes, scores, classes = [], [], []
        for output in outputs:
            for row in output:
                class_id = int(np.argmax(row[5:]))
                score = float(row[5 + class_id])
                if score < 0.4:
                    continue
                center_x, center_y, w, h = row[:4] * [width, height, width, height]
                boxes.append([int(center_x - w / 2), int(center_y - h / 2), int(w), int(h)])
                scores.append(score)
                classes.append(class_id)
        indices = cv2.dnn.NMSBoxes(boxes, scores, 0.4, 0.45)
        selected = np.array(indices).reshape(-1).tolist() if len(indices) else []
        last_labels = [names[classes[i]] for i in selected]
        for i in selected:
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'{names[classes[i]]} {scores[i]:.2f}', (x, max(20, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        frames += 1
        cv2.putText(frame, f'frame {frames}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('YOLOv4-tiny live CPU', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()
print('frames processed:', frames)
print('last frame labels:', last_labels)
print('elapsed seconds:', round(time.monotonic() - started, 1))
