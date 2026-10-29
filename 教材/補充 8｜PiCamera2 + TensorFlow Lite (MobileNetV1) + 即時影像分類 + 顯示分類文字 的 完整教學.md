# 補充 8｜PiCamera2 + TensorFlow Lite (MobileNetV1) + 即時影像分類 + 顯示分類文字 的 完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14223038310) · 更新日期：2026-10-29

## 學習目標

以 LiteRT 對一張 Pi 相機影格執行 MobileNetV1 推論。

## 事前準備

需要 Picamera2、相機、已驗證的 LiteRT 虛擬環境及 MobileNet 模型。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md)建立對應環境，再在練習目錄下載模型：

```bash
curl -fL https://raw.githubusercontent.com/nnsuite/testcases/master/DeepLearningModels/tensorflow-lite/Mobilenet_v1_1.0_224_quant/mobilenet_v1_1.0_224_quant.tflite -o mobilenet.tflite
```

## 程式與執行

將以下程式存為 `補充8.py`，或使用[已測試的範例程式](./範例程式/補充8.py)。在檔案所在目錄執行 `python3 補充8.py`。

```python
import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
interpreter = Interpreter(model_path='mobilenet.tflite')
interpreter.allocate_tensors()
input_info = interpreter.get_input_details()[0]
image = cv2.resize(frame, (224, 224)).astype(input_info['dtype'])
interpreter.set_tensor(input_info['index'], np.expand_dims(image, axis=0))
interpreter.invoke()
output = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
print('camera frame', frame.shape)
print('output shape', output.shape)
```

## 本機實際輸出

```text
camera frame (240, 320, 3)
output shape (1, 1001)
```

輸出維度成功，但程式沒有顯示標籤與信心度，也沒有測試即時畫面或分類正確率。

## 與原文章的差異

- 原文使用 tflite-runtime；本版採 LiteRT Interpreter，並以單張影格驗證推論；完整標籤與即時顯示仍待實作。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
