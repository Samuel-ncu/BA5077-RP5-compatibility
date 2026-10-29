import cv2
import subprocess
from east_helpers import detect_text

# 讀取已裁切並校正的相機照片；EAST 尋找文字區域，Tesseract 嘗試辨認文字。
image = cv2.imread('text-board.png')
if image is None:
    raise RuntimeError('找不到 text-board.png')
net = cv2.dnn.readNet('frozen_east_text_detection.pb')
boxes = detect_text(net, image)
annotated = image.copy()
for x1, y1, x2, y2 in boxes:
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
if not cv2.imwrite('supplement9-camera-east.png', annotated):
    raise RuntimeError('無法儲存結果')
print('EAST boxes:', len(boxes))
print('saved: supplement9-camera-east.png')
result = subprocess.run(['tesseract', 'text-board.png', 'stdout', '-l', 'eng', '--psm', '6'],
                        check=True, capture_output=True, text=True)
print('Tesseract output:')
print(result.stdout.strip())
