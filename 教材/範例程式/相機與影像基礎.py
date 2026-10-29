from pathlib import Path
import cv2
import numpy as np
from picamera2 import Picamera2

folder = Path('/tmp/ba5077-foundation-tests')
folder.mkdir(exist_ok=True)
print('opencv', cv2.__version__)
cam = Picamera2()
cam.configure(cam.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
cam.start()
frame = cam.capture_array()
cam.stop()
cam.close()
print('camera', frame.shape, str(frame.dtype))

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.line(image, (10, 20), (200, 20), (0, 255, 0), 3)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), 2)
cv2.circle(image, (240, 90), 40, (0, 0, 255), 3)
cv2.putText(image, 'OpenCV', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
print('synthetic image saved', cv2.imwrite(str(folder / 'shapes.png'), image))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print('grayscale', gray.shape, str(gray.dtype))
print('image reloaded', cv2.imread(str(folder / 'shapes.png')).shape)

video = folder / 'demo.avi'
writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*'MJPG'), 5.0, (320, 240))
if not writer.isOpened():
    raise RuntimeError('VideoWriter could not open')
for i in range(5):
    sample = image.copy()
    cv2.putText(sample, str(i), (250, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    writer.write(sample)
writer.release()
reader = cv2.VideoCapture(str(video))
count = 0
while True:
    ok, sample = reader.read()
    if not ok:
        break
    count += 1
reader.release()
print('video frames', count)
