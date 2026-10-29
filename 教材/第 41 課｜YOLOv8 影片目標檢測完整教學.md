# 第 41 課｜YOLOv8 影片目標檢測完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222899833) · 更新日期：2026-10-29

> **部分實測**：已在 Thonny 對四影格影片逐格推論並寫入影片；長影片、即時速度和乾淨環境安裝待驗證。[逐篇進度](./Thonny逐篇實測狀態.md)

## 學習目標與背景

影片是按順序排列的影格。物件偵測程式逐格解碼、推論、畫框再編碼；輸出影片的播放 FPS 是時間設定，與電腦實際每秒處理影格的速度不同。本課練習讀取影片、保存每格的框數，並產生新影片和結果圖片。

## 準備與素材

本次在這台 RP5 的既有 `/home/pi/myenv/bin/python3` 環境執行，含 Python 3.11.2、Ultralytics 8.3.50、PyTorch 2.5.1，以及 OpenCV。第 42、43 課另使用 Picamera2。這是本機既有混合環境；在全新虛擬環境透過 Thonny 安裝全部 YOLO 套件仍待實測，不能當成已驗證的乾淨安裝教學。

在瀏覽器下載並解壓本倉庫，依[素材下載與使用說明](./練習素材/素材下載與使用.md)建立新的練習資料夾；模型由[第 39 課](./第%2039%20課｜YOLOv8%20與%20COCO%20資料集完整教學.md)的 Thonny 下載程式取得，並放入同一資料夾。

將 [lesson42-input.avi](./練習素材/lesson42-input.avi) 和[本課程式](./範例程式/第41課-相機影片YOLO.py)複製到練習資料夾，與 `yolov8n.pt` 放在一起。影片由 RP5 相機拍攝螢幕上的 AI 生成物件圖，再裁切、校正並保存為四個影格；圖中的物件不是實體物品。執行會覆寫同名結果，請使用新的練習資料夾。

## 在 Thonny 操作

1. 「工具 → 選項 → 直譯器」選擇已有上述套件的 Python；選「檔案 → 開啟」開啟本課程式。
2. 按綠色執行鈕。觀察下方 Shell，並用檔案管理員開啟產生的 `lesson41-detected.avi` 與 `lesson41-detected-frame.png`。影片播放需適合的影片播放器。

完整程式：

```python
import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('lesson42-input.avi')
writer = None
counts, first_result = [], None
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        if writer is None:
            height, width = frame.shape[:2]
            writer = cv2.VideoWriter('lesson41-detected.avi', cv2.VideoWriter_fourcc(*'MJPG'), 3, (width, height))
            if not writer.isOpened():
                raise RuntimeError('無法建立輸出影片')
        result = model.predict(frame, imgsz=640, device='cpu', verbose=False)[0]
        annotated = result.plot()
        writer.write(annotated)
        counts.append(len(result.boxes))
        if first_result is None:
            first_result = annotated.copy()
finally:
    video.release()
    if writer is not None:
        writer.release()
if not counts or first_result is None:
    raise RuntimeError('輸入影片沒有讀取到影格')
if not cv2.imwrite('lesson41-detected-frame.png', first_result):
    raise RuntimeError('無法儲存結果圖')
print('frames processed:', len(counts))
print('detections per frame:', counts)
print('saved: lesson41-detected.avi, lesson41-detected-frame.png')
```

## 本次 Thonny 實際輸出

```text
frames processed: 4
detections per frame: [3, 3, 3, 3]
saved: lesson41-detected.avi, lesson41-detected-frame.png
```

![Thonny 處理影片及實際輸出](./圖檔/lesson41-thonny.png)

![影片第一個影格的偵測結果](./圖檔/lesson41-detected-frame.png)

四個影格各有三個框；結果圖為先前處理同一練習影片所保存的第一個影格。Thonny 右側靜態檢查曾提示 `VideoWriter_fourcc` 屬性，但本次程式實際成功執行與寫檔，應同時查看 Shell 和產生的檔案。

## 練習與應用

觀察四影格的框是否一致；再自行更換影片並記錄框數。為什麼四影格成功不能保證長影片效能？可延伸到物品計數，並比較漏檢、誤檢與每秒處理速度。

## 與原文章的差異

- 以 RP5 CPU 和 Thonny 執行，採可下載的四影格練習影片；並非原文所有影片及即時情境。
- 新增輸出影片、實測文字和 Thonny 截圖；長影片與乾淨安裝仍待驗證。
