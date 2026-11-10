from pathlib import Path
from importlib.metadata import version
import sys
import time

import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from picamera2 import Picamera2

# 不希望畫面顯示在桌面時設為 False；程式仍會記錄分類摘要。
SHOW_PREVIEW = True
MAX_FRAMES = 50
folder = Path(__file__).resolve().parent
labels = (folder / 'labels.txt').read_text(encoding='utf-8').splitlines()
model = Interpreter(model_path=str(folder / 'mobilenet.tflite'))
model.allocate_tensors()
inp = model.get_input_details()[0]
out = model.get_output_details()[0]
if tuple(inp['shape']) != (1, 224, 224, 3) or inp['dtype'] != np.uint8:
    raise RuntimeError('此範例需要 224x224 RGB uint8 MobileNetV1 模型')
print('Python:', sys.version.split()[0], 'LiteRT:', version('ai-edge-litert'),
      'OpenCV:', cv2.__version__, 'NumPy:', np.__version__, flush=True)
print('preview:', SHOW_PREVIEW, flush=True)
camera = Picamera2()
started = False
count = 0
try:
    camera.configure(camera.create_preview_configuration(
        main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    started = True
    time.sleep(1)
    begin = time.perf_counter()
    while count < MAX_FRAMES:
        frame = camera.capture_array()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (224, 224))
        model.set_tensor(inp['index'], np.expand_dims(rgb, 0))
        model.invoke()
        raw = model.get_tensor(out['index'])[0]
        scale, zero = out['quantization']
        scores = (raw.astype(np.float32) - zero) * scale
        if len(labels) != len(scores):
            raise RuntimeError('標籤數與模型輸出數不一致')
        i = int(np.argmax(scores))
        count += 1
        if count in (1, 10, 25, 50):
            print(f'frame {count}: {labels[i]} {scores[i]:.4f}', flush=True)
        if SHOW_PREVIEW:
            cv2.putText(frame, f'{labels[i]} {scores[i]:.3f}', (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('LiteRT camera - Q to stop', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    elapsed = time.perf_counter() - begin
    print('frames:', count, 'elapsed seconds:', round(elapsed, 2),
          'average FPS:', round(count / elapsed, 2) if elapsed else 0, flush=True)
finally:
    if started:
        camera.stop()
    camera.close()
    if SHOW_PREVIEW:
        cv2.destroyAllWindows()
    print('camera released', flush=True)
