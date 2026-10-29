import cv2

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
net = cv2.dnn.readNetFromTensorflow('opencv_face_detector_uint8.pb', 'opencv_face_detector.pbtxt')
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104, 117, 123), swapRB=False, crop=False)
net.setInput(blob)
output = net.forward()
height, width = image.shape[:2]
scores = []
for detection in output[0, 0]:
    confidence = float(detection[2])
    if confidence < 0.5:
        continue
    x1, y1, x2, y2 = (detection[3:7] * [width, height, width, height]).astype(int)
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width-1, x2), min(height-1, y2)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    scores.append(round(confidence, 3))
if not cv2.imwrite('lesson37-camera-dnn.png', image):
    raise RuntimeError('無法儲存結果')
print('output shape:', output.shape)
print('faces above threshold:', len(scores))
print('confidence scores:', scores)
print('saved: lesson37-camera-dnn.png')
