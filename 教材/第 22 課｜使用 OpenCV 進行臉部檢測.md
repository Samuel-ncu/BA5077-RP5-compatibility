# 第 22 課｜使用 OpenCV 進行臉部檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886426) · 更新日期：2026-10-29

> **Thonny 轉換待完成。** 本篇既有程式、安裝步驟與輸出仍須逐項改寫並在 Thonny 重新操作；現有終端機紀錄不代表已用 Thonny 測試。[逐篇進度](./Thonny逐篇實測狀態.md)

## 學習目標

載入 Haar Cascade 並檢查能否對圖像執行臉部偵測。

## 事前準備

需要 OpenCV 及本機 Haar XML，程式以全黑圖像測試。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第22課.py`，或使用[已測試的範例程式](./範例程式/第22課.py)。

```python
import cv2
import numpy as np
path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(path)
if cascade.empty():
    raise RuntimeError('cascade could not be loaded')
image = np.zeros((240, 320), dtype=np.uint8)
faces = cascade.detectMultiScale(image, 1.1, 3)
print('cascade loaded', not cascade.empty())
print('faces on blank image', len(faces))
```

在該檔案所在目錄執行 `python3 第22課.py`。

## 本機實際輸出

```text
cascade loaded True
faces on blank image 0
```

沒有臉的黑圖輸出 0 個臉部是測試預期；這不能證明真人偵測率。XML 路徑若不存在，須找出相容的模型檔。

## 背景與核心概念

### 臉部偵測和臉部辨識有何不同？

臉部偵測回答影像中可能有沒有臉、在哪裡；辨識則試圖判斷是哪個人。Haar Cascade 使用訓練好的特徵與級聯分類器，輸出會受到角度、光線和遮擋影響。

### 思考、練習與後續應用

解釋空白圖得到零張臉代表什麼、不能代表什麼；為何偵測到臉不等於知道身分？

應用可能涉及敏感生物特徵資料；任何真實資料使用都需確認授權、保存方式與公平性。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 概念流程圖

```mermaid
flowchart LR
    A["影像"]
    B["Haar Cascade 偵測"]
    C["候選臉部位置"]
    D["檢查偵測結果"]
    A --> B --> C --> D
```

此圖用於說明文章的概念或完整目標流程，**不是操作截圖，也不代表每個步驟都已實測**；本機實測範圍請看文章中的標示。

## 進階實測：相機拍攝 AI 生成的人臉與手部素材

### 準備與操作

本次素材是 AI 生成的虛構人物，先顯示在螢幕上，RP5 相機再拍攝；拍攝後另以程式裁切及透視校正。這不是實拍真人，也不是安裝操作截圖。完整拍攝與校正方法見[相機實拍與校正流程](./練習素材/相機實拍與校正流程.md)。

需要系統 Python、OpenCV 與可讀取的 Haar 模型 XML。 可將[本次校正影像](./圖檔/facehand-board.png)下載為 `facehand-board.png`，與[範例程式](./範例程式/第22課-相機人臉偵測.py)放在 RP5 的同一練習目錄，先確認輸出檔不會覆蓋現有資料。

```python
import cv2

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
cascade = cv2.CascadeClassifier(path)
if cascade.empty():
    raise RuntimeError('無法載入 Haar 模型，請確認 XML 路徑')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
if not cv2.imwrite('lesson22-camera-face.png', image):
    raise RuntimeError('無法儲存結果')
print('cascade loaded:', not cascade.empty())
print('faces found:', len(faces))
print('saved: lesson22-camera-face.png')
```

```bash
python3 第22課-相機人臉偵測.py
```

### 本次 RP5 實際輸出與結果

```text
cascade loaded: True
faces found: 1
saved: lesson22-camera-face.png
```

![RP5 相機拍攝生成素材的實測結果](./圖檔/lesson22-camera-face.png)

綠框由 Haar Cascade 程式畫出。這次找到一個候選人臉，只能說明這張素材的結果，不能證明真人或其他角度的表現。 原始相機全景含螢幕外環境，沒有公開。

### 讀懂原理與結果

本程式使用本機現有的 Haar XML 路徑；不同系統應找出模型路徑。Haar 使用灰階像素及尺度與鄰近候選框參數；調整 `scaleFactor`、`minNeighbors` 和最小尺寸可能改變輸出。臉部偵測回答位置，並不回答身分。

學生練習：先預測把測試圖縮小或轉動後可能發生什麼，再自行測試並記錄結果。如果找不到圖或模型，確認目前目錄、路徑及 Python 環境；如果找到零個目標，還應檢查畫面是否清楚。實際拍攝他人時須先取得適當授權，避免將私人照片上傳。

## 與原文章的差異

- 原文使用外部圖片與相對路徑的 XML；本版使用本機已驗證的絕對路徑與合成圖。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 加入教學流程示意；圖中的完整目標流程不代表已逐步實測。
- 本輪新增相機拍攝 AI 生成臉部素材後的 Haar 偵測；原文的真人相機即時視窗尚未完整測試。
