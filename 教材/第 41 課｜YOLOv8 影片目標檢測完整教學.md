# 第 41 課｜YOLOv8 影片目標檢測完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222899833) · 更新日期：2026-10-29

## 學習目標

建立合成短影片，再以 YOLOv8n 對影片逐幀執行 CPU 推論。

## 事前準備

需要 YOLO CPU 虛擬環境、模型與可用 MJPG 影片編碼器；會在目前目錄產生 lesson41-demo.avi。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#7-yolo-與-pytorch)建立並啟用 YOLO CPU 環境，再於練習目錄下載模型：

```bash
curl -fL https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt -o yolov8n.pt
```

不要使用原文的 CUDA 11.8 索引。

## 程式與執行

將下列已在 RP5 執行的程式存為 `第41課.py`，或使用[範例程式](./範例程式/第41課.py)。先確認目前目錄及檔案，避免覆蓋已有資料。

```python
import cv2
import numpy as np
from ultralytics import YOLO

path = 'lesson41-demo.avi'
writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), 5.0, (320, 240))
if not writer.isOpened():
    raise RuntimeError('VideoWriter could not open')
for _ in range(3):
    writer.write(np.zeros((240, 320, 3), dtype=np.uint8))
writer.release()
model = YOLO('yolov8n.pt')
results = list(model.predict(path, imgsz=320, device='cpu', stream=True, verbose=False))
print('frames processed', len(results))
```

執行 `python3 第41課.py`。

## 本機實際輸出

```text
frames processed 3
```

本機處理了 3 個合成影格；此測試未產生加框影片，也未評估長影片速度。

## 與原文章的差異

- 原文處理使用者影片；本版先用短合成影片驗證讀取與逐幀推論。
- 真實場景的準確率、速度和操作畫面尚未完整驗證。
- 尚未保存操作畫面截圖。
