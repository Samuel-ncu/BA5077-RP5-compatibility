import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
image = np.zeros((320, 320, 3), dtype=np.uint8)
still = model.predict(image, imgsz=320, device='cpu', verbose=False)
camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
camera_result = model.predict(frame, imgsz=320, device='cpu', verbose=False)
print('synthetic image results', len(still))
print('camera image results', len(camera_result))
