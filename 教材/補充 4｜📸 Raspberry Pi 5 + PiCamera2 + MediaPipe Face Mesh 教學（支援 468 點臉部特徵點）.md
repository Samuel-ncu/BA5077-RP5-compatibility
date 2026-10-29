# 補充 4｜📸 Raspberry Pi 5 + PiCamera2 + MediaPipe Face Mesh 教學（支援 468 點臉部特徵點）

[原始文章](https://liusming.pixnet.net/blog/posts/14223033921) · 更新日期：2026-10-29

## 學習目標

以 MediaPipe Face Mesh 處理一張 Pi 相機影格。

## 事前準備

需要 PiCamera2、相機及 MediaPipe 0.10.9 虛擬環境。

MediaPipe 的已測試安裝方式請看[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#5-mediapipe-手勢與-face-mesh)。不同專案請使用獨立環境。

## 程式與執行

將以下程式存為 `補充4.py`，或使用[已測試的範例程式](./範例程式/補充4.py)。在檔案所在目錄執行 `python3 補充4.py`。

```python
import cv2
import mediapipe as mp
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as mesh:
    result = mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
print('frame processed', result is not None)
```

## 本機實際輸出

```text
frame processed True
```

成功處理影格不代表一定偵測到臉部或 468 點；真人追蹤、顯示與精度未測。

## 與原文章的差異

- 原文即時臉部網格在本版先縮小成可驗證的單張流程，並不宣稱 GUI 與完整模型表現已通過。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
