import cv2
import numpy as np
from east_helpers import detect_text

net = cv2.dnn.readNet('frozen_east_text_detection.pb')
image = np.full((320, 320, 3), 255, dtype=np.uint8)
cv2.putText(image, 'HELLO 123', (15, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 2)
boxes = detect_text(net, image)
for x1, y1, x2, y2 in boxes:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
print('text boxes', len(boxes))
print('saved', cv2.imwrite('supplement9-east.png', image))
