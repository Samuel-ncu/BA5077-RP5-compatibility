# 第 39 課｜YOLOv8 與 COCO 資料集完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222888508) · 更新日期：2026-10-29

## 學習目標

載入 YOLOv8n，查看模型的類別數及第一個類別。

## 事前準備

需要已驗證的 YOLO CPU 虛擬環境和模型檔。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#7-yolo-與-pytorch)建立並啟用 YOLO CPU 環境，再於練習目錄下載模型：

```bash
curl -fL https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt -o yolov8n.pt
```

不要使用原文的 CUDA 11.8 索引。

## 程式與執行

將下列已在 RP5 執行的程式存為 `第39課.py`，或使用[範例程式](./範例程式/第39課.py)。先確認目前目錄及檔案，避免覆蓋已有資料。

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
print('class count', len(model.names))
print('class 0', model.names[0])
```

執行 `python3 第39課.py`。

## 本機實際輸出

```text
class count 80
class 0 person
```

此模型包含 80 個類別，編號 0 是 person。這不等於資料集訓練或物件辨識精度已驗證。

## 與原文章的差異

- 原文涵蓋 COCO 資料集與模型推論；本版先驗證模型類別資訊，未測試資料集下載及訓練。
- 真實場景的準確率、速度和操作畫面尚未完整驗證。
- 尚未保存操作畫面截圖。
