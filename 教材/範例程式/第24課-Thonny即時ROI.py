import time
import cv2
from picamera2 import Picamera2

camera = Picamera2()
count = 0
try:
    camera.configure(camera.create_preview_configuration(main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    start = time.monotonic()
    while time.monotonic() - start < 120:
        frame = camera.capture_array()
        roi = frame[120:360, 160:480].copy()
        cv2.rectangle(frame, (160, 120), (479, 359), (0, 255, 0), 2)
        cv2.imshow('Live camera with ROI', frame)
        cv2.imshow('Live ROI', roi)
        count += 1
        if count == 1:
            print('frame:', frame.shape, 'ROI:', roi.shape, flush=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()
    print('frames:', count, flush=True)
