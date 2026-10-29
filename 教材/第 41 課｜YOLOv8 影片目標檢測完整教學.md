# 第 41 課｜YOLOv8 影片目標檢測完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222899833) · 更新日期：2026-10-29

> **部分實測**：已在 Thonny 測試四影格及由四影格重複製成的兩分鐘影片；真實動態長影片和乾淨環境安裝待驗證。[逐篇進度](./Thonny逐篇實測狀態.md)

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

## 延伸實驗：兩分鐘影片的逐格推論與讀回

### 素材和操作

此練習把上面的四張相機拍攝生成圖影格循環 90 次，建立 360 張影格、播放設定為 3 FPS 的兩分鐘影片。它能測試較多影格的讀寫和推論，但**不是兩分鐘不同的真實動態場景**，不能用它推論長時間實景準確率或長時間相機穩定性。

1. 在新練習資料夾放入 [lesson42-input.avi](./練習素材/lesson42-input.avi)、`yolov8n.pt` 和 [兩分鐘影片測試程式](./範例程式/第41課-Thonny兩分鐘影片測試.py)。模型取得方式見前節。若已有相同名稱的輸出影片，程式會停止，請改用新資料夾。
2. 在 Thonny 選擇前節已具備 YOLO 與 OpenCV 的直譯器，開啟程式並按綠色執行鈕。它先建立 `repeat-120s-input.avi`，再逐格推論、建立 `repeat-120s-output.avi`，最後重新讀取每一張輸出影格並計數。
3. 在同一資料夾下載並於 Thonny 執行[影片片段播放程式](./範例程式/第41課-Thonny播放影片片段.py)，它顯示前 12 張影格後結束。本次只目視播放前 12 張，整段 360 張由程式逐張解碼讀回，沒有目視播放全程。

兩分鐘測試完整程式：

```python
import time
from pathlib import Path
import cv2
from ultralytics import YOLO

for name in ('repeat-120s-input.avi', 'repeat-120s-output.avi'):
    if Path(name).exists():
        raise FileExistsError(f'{name} 已存在，請先使用新的練習資料夾')

source = cv2.VideoCapture('lesson42-input.avi')
if not source.isOpened():
    raise RuntimeError('找不到 lesson42-input.avi')
frames = []
while True:
    ok, frame = source.read()
    if not ok:
        break
    frames.append(frame)
source.release()
if len(frames) != 4:
    raise RuntimeError('本練習預期 4 張來源影格')
height, width = frames[0].shape[:2]
fps = 3.0
writer = cv2.VideoWriter('repeat-120s-input.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
if not writer.isOpened():
    raise RuntimeError('無法建立輸入影片')
for i in range(360):
    writer.write(frames[i % len(frames)])
writer.release()
print('input: repeated four frames', flush=True)
print('input frames: 360', flush=True)
print('playback FPS: 3.0', flush=True)
print('input duration seconds: 120.0', flush=True)

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('repeat-120s-input.avi')
output = cv2.VideoWriter('repeat-120s-output.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
if not video.isOpened() or not output.isOpened():
    video.release()
    output.release()
    raise RuntimeError('無法讀取或建立影片')
count = 0
start = time.perf_counter()
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
        output.write(result.plot())
        count += 1
        if count % 90 == 0:
            print('processed:', count, flush=True)
finally:
    video.release()
    output.release()
elapsed = time.perf_counter() - start
check = cv2.VideoCapture('repeat-120s-output.avi')
readback = 0
while True:
    ok, _ = check.read()
    if not ok:
        break
    readback += 1
check.release()
print('processed frames:', count)
print('processing seconds:', round(elapsed, 2))
print('processing FPS:', round(count / elapsed, 2))
print('decoded output frames:', readback)
print('output playback seconds:', round(readback / fps, 2))
```

播放片段完整程式：

```python
import cv2

video = cv2.VideoCapture('repeat-120s-output.avi')
if not video.isOpened():
    raise RuntimeError('無法開啟輸出影片')
count = 0
try:
    while count < 12:
        ok, frame = video.read()
        if not ok:
            break
        count += 1
        cv2.imshow('YOLO video playback sample', frame)
        cv2.waitKey(333)
finally:
    video.release()
    cv2.destroyAllWindows()
print('displayed frames:', count)
```

### 2026-10-29 RP5 的實際結果

```text
input: repeated four frames
input frames: 360
playback FPS: 3.0
input duration seconds: 120.0
processed: 90
processed: 180
processed: 270
processed: 360
processed frames: 360
processing seconds: 38.62
processing FPS: 9.32
decoded output frames: 360
output playback seconds: 120.0
```

![Thonny 顯示兩分鐘影片處理與讀回結果](./圖檔/lesson41-long-thonny.png)

播放片段的 Shell 輸出為 `displayed frames: 12`：

![Thonny 播放輸出影片片段的實際畫面](./圖檔/lesson41-playback-thonny.png)

這是**操作截圖與程式結果**；來源為相機拍攝 AI 生成物件圖片。`3.0 FPS` 決定影片每秒播放幾張；`9.32 FPS` 是本次從解碼、YOLO 推論到寫出 360 張的平均處理速度，與影片播放速度不同。首次模型載入和最後重新讀回時間不計入 38.62 秒；不同負載會影響結果。

Thonny 偵測器可能對 `cv2.VideoWriter_fourcc` 顯示靜態提示。本次程式實際建立並讀回 360 張，這個提示並非此次執行失敗；若你的 Shell 實際報錯，應先確認 OpenCV 版本與影片編碼器。

## 練習與應用

觀察四影格的框是否一致；再自行更換影片並記錄框數。為什麼四影格成功不能保證長影片效能？可延伸到物品計數，並比較漏檢、誤檢與每秒處理速度。

## 與原文章的差異

- 以 RP5 CPU 和 Thonny 執行，採可下載的四影格練習影片；並非原文所有影片及即時情境。
- 新增兩分鐘重複影格影片、實測處理時間、讀回和前 12 張播放截圖；真實動態長影片與乾淨安裝仍待驗證。
