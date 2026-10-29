from pathlib import Path
import subprocess

import cv2
from east_helpers import detect_text

# 相機拍攝後經校正的練習照片、EAST 模型和 east_helpers.py 要在同一資料夾。
image = cv2.imread('text-board.png')
if image is None:
    raise FileNotFoundError('找不到 text-board.png')
net = cv2.dnn.readNet('frozen_east_text_detection.pb')
boxes = sorted(detect_text(net, image), key=lambda box: (box[1], box[0]))
height, width = image.shape[:2]
result_image = image.copy()
print('EAST boxes:', len(boxes), flush=True)
for number, (x1, y1, x2, y2) in enumerate(boxes, 1):
    # 多保留 5 像素背景，避免裁到字的筆畫。
    left, top = max(0, x1 - 5), max(0, y1 - 5)
    right, bottom = min(width, x2 + 5), min(height, y2 + 5)
    crop = image[top:bottom, left:right]
    ok, png = cv2.imencode('.png', crop)
    if not ok:
        raise RuntimeError('無法編碼裁切影像')
    # -l eng 使用英文資料，--psm 7 將每個區域視為單行文字。
    process = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', 'eng', '--psm', '7'],
        input=png.tobytes(), capture_output=True, check=True,
    )
    text = process.stdout.decode('utf-8').strip().replace('\n', ' ')
    print(f'{number}: ({x1}, {y1}, {x2}, {y2}) {text!r}', flush=True)
    cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 180, 0), 2)
    cv2.putText(result_image, str(number), (x1, max(20, y1 - 5)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

output = Path('east-box-ocr-result.png')
if output.exists():
    raise FileExistsError('結果圖已存在，請移至其他資料夾後再執行')
if not cv2.imwrite(str(output), result_image):
    raise RuntimeError('無法儲存結果圖')
print('saved:', output)
