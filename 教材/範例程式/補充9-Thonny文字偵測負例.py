import cv2
import numpy as np
from east_helpers import detect_text

net = cv2.dnn.readNet('east-download-check.pb')
for value, name in [(0, 'black'), (255, 'white')]:
    image = np.full((320, 320, 3), value, dtype=np.uint8)
    boxes = detect_text(net, image)
    print(f'{name} blank: {len(boxes)} boxes')
