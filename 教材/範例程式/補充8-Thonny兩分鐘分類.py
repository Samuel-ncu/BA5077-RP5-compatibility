import time
import cv2
import numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter

with open('labels.txt', encoding='utf-8') as f:
    labels = [line.strip() for line in f]
interpreter = Interpreter(model_path='mobilenet.tflite')
interpreter.allocate_tensors()
inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]
if tuple(inp['shape']) != (1, 224, 224, 3) or inp['dtype'] != np.uint8:
    raise RuntimeError('需要 uint8 224x224 RGB 的 MobileNetV1 模型')
scale, zero = out['quantization']
if scale <= 0:
    raise RuntimeError('模型輸出量化參數無效')

camera = Picamera2()
count = 0
next_report = 30
stop_reason = 'time limit'
try:
    camera.configure(camera.create_preview_configuration(
        main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    start = time.perf_counter()
    while time.perf_counter() - start < 120:
        frame = camera.capture_array()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (224, 224))
        interpreter.set_tensor(inp['index'], np.expand_dims(rgb, 0))
        interpreter.invoke()
        raw = interpreter.get_tensor(out['index'])[0]
        scores = (raw.astype(np.float32) - zero) * scale
        if len(labels) != len(scores):
            raise RuntimeError('標籤數與模型輸出數不一致')
        i = int(np.argmax(scores))
        count += 1
        cv2.putText(frame, f'{labels[i]} {scores[i]:.3f}', (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('TFLite camera - Q to stop', frame)
        elapsed = time.perf_counter() - start
        if elapsed >= next_report:
            print(f'after {next_report}s: frames={count}, '
                  f'top={labels[i]}, score={scores[i]:.4f}', flush=True)
            next_report += 30
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_reason = 'q key'
            break
    elapsed = time.perf_counter() - start
    print('stop reason:', stop_reason)
    print('frames:', count)
    print('elapsed seconds:', round(elapsed, 2))
    print('average FPS:', round(count / elapsed, 2))
finally:
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()
    print('camera released')
