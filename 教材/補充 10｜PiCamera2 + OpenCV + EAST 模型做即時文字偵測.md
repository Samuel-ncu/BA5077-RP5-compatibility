# 補充 10｜PiCamera2 + OpenCV + EAST 模型做即時文字偵測

[原始文章](https://liusming.pixnet.net/blog/posts/14223038343) · 更新日期：2026-10-29

## 學習目標

把一張 Pi 相機影格送入 EAST 模型並解析文字框。

## 事前準備

需要 PiCamera2、相機、OpenCV、NumPy、EAST 模型及 east_helpers.py。

先將[文字框處理程式 east_helpers.py](./範例程式/east_helpers.py)放在練習目錄，並下載本次測試模型（約 97 MB）：

```bash
curl -fL https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb -o frozen_east_text_detection.pb
```

## 程式與執行

將以下程式存為 `補充10.py`，或使用[已測試的範例程式](./範例程式/補充10.py)。在檔案所在目錄執行 `python3 補充10.py`。

```python
import cv2
from picamera2 import Picamera2
from east_helpers import detect_text

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
net = cv2.dnn.readNet('frozen_east_text_detection.pb')
boxes = detect_text(net, frame)
print('camera frame', frame.shape)
print('frame processed', True)
```

## 本機實際輸出

```text
camera frame (240, 320, 3)
frame processed True
```

已對單張影格執行模型與文字框解析；未保存私人相機畫面，未測即時預覽或準確率。

## 與原文章的差異

- 原文使用連續攝影機及顯示視窗；本版先完成單張影格與後處理，不宣稱即時畫面已測。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
