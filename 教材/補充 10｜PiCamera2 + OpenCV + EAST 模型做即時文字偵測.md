# 補充 10｜PiCamera2 + OpenCV + EAST 模型做即時文字偵測

[原始文章](https://liusming.pixnet.net/blog/posts/14223038343) · 更新日期：2026-10-29

## 學習目標

把一張 Pi 相機影格送入 EAST 模型，檢查輸出維度。

## 事前準備

需要 PiCamera2、相機、OpenCV、NumPy 與 EAST 模型。

在練習目錄下載本次測試模型（約 97 MB）：

```bash
curl -fL https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb -o frozen_east_text_detection.pb
```

## 程式與執行

將以下程式存為 `補充10.py`，或使用[已測試的範例程式](./範例程式/補充10.py)。在檔案所在目錄執行 `python3 補充10.py`。

```python
import cv2
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
net = cv2.dnn.readNet('frozen_east_text_detection.pb')
blob = cv2.dnn.blobFromImage(frame, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
scores, geometry = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])
print('camera frame', frame.shape)
print('scores shape', scores.shape)
print('geometry shape', geometry.shape)
```

## 本機實際輸出

```text
camera frame (240, 320, 3)
scores shape (1, 1, 80, 80)
geometry shape (1, 5, 80, 80)
```

此測試處理單張影格；未解析文字框、測即時預覽或準確率。

## 與原文章的差異

- 原文是即時文字框顯示；本版先測相機與 EAST 的單張推論，完整後處理仍待實作。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
