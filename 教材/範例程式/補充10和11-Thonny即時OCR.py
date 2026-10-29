from pathlib import Path
import subprocess
import time

import cv2
from picamera2 import Picamera2
from east_helpers import detect_text

# 與模型、east_helpers.py 放在同一個資料夾。這些座標是本次相機取景，請依自己的畫面調整。
model_path = Path('frozen_east_text_detection.pb')
if not model_path.exists():
    raise FileNotFoundError('找不到 EAST 模型')
net = cv2.dnn.readNet(str(model_path))
print('15 seconds to show the text board', flush=True)
time.sleep(15)
camera = Picamera2()
started = False
frames = 0
begin = None
try:
    camera.configure(camera.create_preview_configuration(
        main={'size': (1280, 960), 'format': 'RGB888'}))
    camera.start()
    started = True
    time.sleep(1)
    begin = time.monotonic()
    while time.monotonic() - begin < 25:
        full_frame = camera.capture_array()
        frame = full_frame[0:520, 400:1250].copy()
        boxes = sorted(detect_text(net, frame), key=lambda b: (b[1], b[0]))
        texts = []
        height, width = frame.shape[:2]
        for x1, y1, x2, y2 in boxes:
            crop = frame[max(0, y1-5):min(height, y2+5), max(0, x1-5):min(width, x2+5)]
            ok, png = cv2.imencode('.png', crop)
            if not ok:
                raise RuntimeError('圖片編碼失敗')
            result = subprocess.run(['tesseract', 'stdin', 'stdout', '-l', 'eng', '--psm', '7'],
                                    input=png.tobytes(), capture_output=True, check=True)
            text = result.stdout.decode('utf-8').strip().replace('\n', ' ')
            texts.append(text)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 220, 0), 2)
        frames += 1
        print(f'frame {frames}: {len(boxes)} boxes; {texts}', flush=True)
        cv2.imshow('EAST + Tesseract live', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('q pressed', flush=True)
            break
finally:
    if started:
        camera.stop()
    camera.close()
    cv2.destroyAllWindows()
    print('frames:', frames, flush=True)
    if begin is not None:
        print('elapsed seconds:', round(time.monotonic() - begin, 2), flush=True)
    print('camera released', flush=True)
