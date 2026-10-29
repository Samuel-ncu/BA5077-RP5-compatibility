# 第 42 課｜YOLOv8 即時攝影機目標偵測教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222899842) · 更新日期：2026-10-29

> **部分實測**：已在 Thonny 連續擷取及推論四張相機影格；持續預覽、長時間效能、乾淨環境安裝與 Hailo 待驗證。[逐篇進度](./Thonny逐篇實測狀態.md)

## 學習目標與背景

CSI 相機由 Picamera2 擷取影格，YOLO 模型分析影格並回傳候選物件框。連續影格依序取像及推論，和先前拍好的影片不同；程式結束時釋放相機，其他程式才可使用它。原文標題的 PyCamera2 在此指 Python 套件 Picamera2。

本練習只列印偵測框數，沒有顯示相機預覽或保存相機畫面，因此四張影格測試不等於完整即時顯示。框數也不能證明辨識正確；相機內容和光線會改變結果。

## 準備

本次在這台 RP5 的既有 `/home/pi/myenv/bin/python3` 環境執行，含 Python 3.11.2、Ultralytics 8.3.50、PyTorch 2.5.1，以及 OpenCV。第 42、43 課另使用 Picamera2。這是本機既有混合環境；在全新虛擬環境透過 Thonny 安裝全部 YOLO 套件仍待實測，不能當成已驗證的乾淨安裝教學。

在瀏覽器下載並解壓本倉庫，依[素材下載與使用說明](./練習素材/素材下載與使用.md)建立新的練習資料夾；模型由[第 39 課](./第%2039%20課｜YOLOv8%20與%20COCO%20資料集完整教學.md)的 Thonny 下載程式取得，並放入同一資料夾。

將[共用相機範例](./範例程式/第42-43課-Thonny相機偵測.py)放在模型所在的練習資料夾。接妥 CSI 相機並確認未被其他程式占用。本範例直接取得當前相機畫面，無需下載圖片；可對準不含個人資訊的物品。相機內容不會被本程式保存。

## Thonny 操作

1. 在「工具 → 選項 → 直譯器」選擇已有 Picamera2 與 Ultralytics 的 Python，開啟共用相機範例。
2. 按綠色執行鈕，等待四張影格推論完成；Shell 列出尺寸、框數和這次平均迴圈速度。

```python
import time
from picamera2 import Picamera2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
camera = Picamera2()
counts = []
try:
    camera.configure(camera.create_preview_configuration(
        main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    start = time.perf_counter()
    for index in range(4):
        frame = camera.capture_array()
        result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
        counts.append(len(result.boxes))
        print('frame:', index + 1, 'shape:', frame.shape,
              'detections:', counts[-1], flush=True)
    elapsed = time.perf_counter() - start
finally:
    camera.stop()
    camera.close()
print('processed:', len(counts))
print('elapsed seconds:', round(elapsed, 2))
print('average FPS:', round(len(counts) / elapsed, 2))
```

## 本次實際輸出

```text
frame: 1 shape: (480, 640, 3) detections: 2
frame: 2 shape: (480, 640, 3) detections: 2
frame: 3 shape: (480, 640, 3) detections: 2
frame: 4 shape: (480, 640, 3) detections: 2
processed: 4
elapsed seconds: 1.41
average FPS: 2.84
```

![Thonny 執行相機與 YOLO 的實際畫面](./圖檔/lesson42-camera-thonny.png)

本次每張得到兩個候選框，並未人工核對框的正確性。時間涵蓋四次取像與推論、包含首次推論；不含模型載入和相機暖機。2.84 FPS 僅代表這次短暫的 CPU 測量，不能保證其他情況或長時間速度。

## 練習與延伸

比較 320 和 640 輸入尺寸時的偵測結果與耗時；分別記錄光線、畫面內容及執行次數。設計長時間測試時，還要考慮畫面顯示、停止方式、掉幀和資源釋放。

## 與原文章的差異

- 本版以 Picamera2 擷取 CSI 相機並在 RP5 CPU 上推論；不同於直接假設桌面電腦 CUDA 或攝影機介面。
- 本次以 Thonny 測試四張影格與實際輸出，尚未完成原文的持續預覽及長時間測試；需要 Hailo 的加速部分待有模組後驗證。
