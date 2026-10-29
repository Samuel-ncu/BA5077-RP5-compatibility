import cv2
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
net = cv2.dnn.readNet('frozen_east_text_detection.pb')
blob = cv2.dnn.blobFromImage(frame, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
scores, geometry = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])
print('camera frame', frame.shape)
print('scores shape', scores.shape)
print('geometry shape', geometry.shape)
