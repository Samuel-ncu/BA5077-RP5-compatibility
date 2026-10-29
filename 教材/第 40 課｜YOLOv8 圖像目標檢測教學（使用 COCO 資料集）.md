# 第 40 課｜YOLOv8 圖像目標檢測教學（使用 COCO 資料集）

[原始文章](https://liusming.pixnet.net/blog/posts/14222899812) · 更新日期：2026-10-29

> **部分實測。** 已用 Thonny 在 RP5 CPU 對一張相機照片推論；新建環境安裝 YOLO、拍攝流程及真實物件測試仍待補齊。[逐篇進度](./Thonny逐篇實測狀態.md) · [素材下載說明](./練習素材/素材下載與使用.md)

## 學習目標

了解偵測框、類別與信心值；在 Thonny 使用 YOLOv8n 辨識圖片，觀察並儲存結果。

## 背景與理論

影像辨識把像素送入模型，物件偵測進一步回傳候選物體的位置、類別和信心值。程式將候選框與類別畫回圖片，方便人類檢查。信心值反映模型對該候選類別的分數，**不等於保證正確的機率或整體準確率**；遮擋、光線和輸入影像皆會影響結果。

## 素材與環境

測試圖片的內容先由 AI 生成，再顯示在螢幕上，經 RP5 相機拍攝及透視校正；蘋果、香蕉與杯子是圖片中的生成物件，不是真實擺放的物品。[下載校正後的相機照片](./圖檔/objects-board.png)。原始全景照片含周圍環境，未公開。這是單張照片，不是即時影片。

本次使用第 39 課所述既有 `/home/pi/myenv/bin/python3`，已有 Ultralytics、PyTorch 和 OpenCV；全新環境的套件安裝仍未驗證。請在 Thonny 選擇已具備這些套件的 Python，並完成[第 39 課模型下載](./第%2039%20課｜YOLOv8%20與%20COCO%20資料集完整教學.md)。

## 在 Thonny 操作

1. 依[素材下載與使用說明](./練習素材/素材下載與使用.md)取得本倉庫並解壓，在新的練習資料夾放入[本課程式](./範例程式/第40課-Thonny校正圖YOLO.py)與 `objects-board.png`。圖片來源是本倉庫的 `教材/圖檔/objects-board.png`。
2. 在同一資料夾依第 39 課執行下載程式，取得 `yolov8n.pt`。模型檔、圖片和本課程式須放在一起。
3. 在 Thonny 選擇「檔案 → 開啟」開啟本課程式，按綠色執行鈕，觀察下方 Shell。結果圖 `lesson40-yolov8.png` 會寫入練習資料夾；先確認不會覆蓋既有同名結果。

本次執行的完整程式：

```python
import cv2
from ultralytics import YOLO

image = cv2.imread('objects-board.png')
if image is None:
    raise RuntimeError('找不到 objects-board.png，請將素材放在程式資料夾')
model = YOLO('yolov8n.pt')
result = model.predict(image, imgsz=640, device='cpu', verbose=False)[0]
if not cv2.imwrite('lesson40-yolov8.png', result.plot()):
    raise RuntimeError('無法儲存結果圖片')
print('image:', image.shape)
print('detections:', len(result.boxes))
for box in result.boxes:
    cls = int(box.cls[0])
    print('class:', model.names[cls], 'confidence:', round(float(box.conf[0]), 3))
print('saved: lesson40-yolov8.png')
```

## 本機實際輸出與截圖

```text
image: (675, 1200, 3)
detections: 3
class: cup confidence: 0.958
class: banana confidence: 0.93
class: apple confidence: 0.894
saved: lesson40-yolov8.png
```

![Thonny 執行 YOLOv8 圖像偵測及實際輸出](./圖檔/lesson40-thonny.png)

![RP5 相機照片的物件偵測結果](./圖檔/objects-yolo.png)

照片尺寸以「高、寬、色彩通道」表示；輸出三個框。上方結果圖來自先前對同一張校正後照片的 RP5 推論，本次 Thonny 再次對該照片推論並得到上述數值。不同模型或輸入條件可能產生不同結果。

## 練習與後續應用

- 把其中一個物品局部遮住，再觀察框與分數是否改變；記錄你自己的結果。
- 準備正例、沒有物品的負例，以及不同光線下的照片，比較人工標註與模型結果。單張示範不足以估算準確率。
- 可延伸為教室物品計數原型，但須測試誤檢、漏檢和速度後才能評估適用性。

參考：[Ultralytics 偵測文件](https://docs.ultralytics.com/tasks/detect/)。

## 與原文章的差異

- 本版以 RP5 CPU 和 Thonny 執行，素材為相機拍攝螢幕上的 AI 生成圖，並非原文外部圖像或完整 COCO 資料集。
- 新增可下載的校正照片、程式、操作截圖與實際輸出；新拍照片及校正步驟尚未在 Thonny 重測。
- 本次沿用既有 YOLO 環境，乾淨虛擬環境的套件安裝、真實物件及即時影片尚待驗證。
