import cv2

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(path)
if cascade.empty():
    raise RuntimeError('無法載入 Haar 模型，請確認 XML 路徑')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
if not cv2.imwrite('lesson22-camera-face.png', image):
    raise RuntimeError('無法儲存結果')
print('cascade loaded:', not cascade.empty())
print('faces found:', len(faces))
print('saved: lesson22-camera-face.png')
