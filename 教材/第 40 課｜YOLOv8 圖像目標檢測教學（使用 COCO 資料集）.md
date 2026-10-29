# 第 40 課｜YOLOv8 圖像目標檢測教學（使用 COCO 資料集）

[原始文章](https://liusming.pixnet.net/blog/posts/14222899812) · 更新日期：2026-10-29

## 學習目標

使用 YOLOv8n 對合成圖片執行一次 CPU 推論。

## 事前準備

需要 YOLO CPU 虛擬環境與模型檔。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#7-yolo-與-pytorch)建立並啟用 YOLO CPU 環境，再於練習目錄下載模型：

```bash
curl -fL https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt -o yolov8n.pt
```

不要使用原文的 CUDA 11.8 索引。

## 程式與執行

將下列已在 RP5 執行的程式存為 `第40課.py`，或使用[範例程式](./範例程式/第40課.py)。先確認目前目錄及檔案，避免覆蓋已有資料。

```python
from ultralytics import YOLO
import numpy as np

model = YOLO('yolov8n.pt')
image = np.zeros((320, 320, 3), dtype=np.uint8)
results = model.predict(image, imgsz=320, device='cpu', verbose=False)
print('results', len(results))
print('boxes', len(results[0].boxes))
```

執行 `python3 第40課.py`。

## 本機實際輸出

```text
results 1
boxes 0
```

空白圖片得到 1 筆結果、0 個框；不能用它判斷真實圖片的偵測品質。

## 與原文章的差異

- 原文使用外部圖像；本版先使用合成空白圖驗證推論，不聲稱測過 COCO 圖片。
- 真實場景的準確率、速度和操作畫面尚未完整驗證。
- 尚未保存操作畫面截圖。
