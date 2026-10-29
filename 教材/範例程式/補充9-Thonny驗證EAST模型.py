import cv2
from east_helpers import detect_text

image = cv2.imread('text-board.png')
if image is None:
    raise RuntimeError('找不到 text-board.png，請放在相同資料夾')
net = cv2.dnn.readNet('east-download-check.pb')
boxes = detect_text(net, image)
print('model loaded: east-download-check.pb')
print('image:', image.shape)
print('EAST boxes:', len(boxes))
