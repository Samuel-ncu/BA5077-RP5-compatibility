# 第 26 課｜使用 OpenCV 進行背景差分與運動物體檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886516) · 更新日期：2026-10-29

> 本課已在 Thonny 實測處理相機短影片的首末影格差分；其他既有情境仍依下文標示待重測。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

## 學習目標

用影像差分與閾值找出變動像素。

## 事前準備

需要 OpenCV 與 NumPy；本例在黑色背景建立 20 × 20 的白色區域。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。


### 用 Thonny 準備套件與教材檔案

1. 先依[擴充環境安裝步驟](./Thonny環境與套件安裝.md#第-2527-課在-thonny-建立-opencv-擴充環境)，在 Thonny 建立並選擇獨立環境；本次使用 Python 3.11、NumPy 1.26.4、opencv-contrib-python 4.11.0.86。
2. 在 RP5 瀏覽器開啟本儲存庫，按 **Code → Download ZIP** 並解壓；詳細步驟見[素材下載與使用說明](./練習素材/素材下載與使用.md)。下載教材不等於安裝套件。
3. 從解壓後的 `教材/範例程式` 把 `第26課-影片影格差分.py`，以及 `教材/練習素材` 的 `lesson16-camera.avi` 複製到**同一個新的練習資料夾**，影片檔名保持不變。此影片是 RP5 相機拍攝螢幕動畫後經處理的 12 張影格，不是生成的操作截圖。
4. 用 Thonny 開啟該程式，按綠色執行鈕。結果會寫入目前程式的練習資料夾；再次執行可能覆寫同名結果。若找不到影片，先確認影片名稱及程式和影片的位置。

## 程式與執行

將下列程式存為 `第26課.py`，或使用[先前以終端機測試的範例程式](./範例程式/第26課.py)。

```python
import cv2
import numpy as np
background = np.zeros((100, 100), dtype=np.uint8)
current = background.copy()
current[20:40, 30:50] = 255
diff = cv2.absdiff(background, current)
_, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
if not cv2.imwrite('lesson26-difference.png', np.hstack((background, current, mask))):
    raise RuntimeError('image save failed')
print('changed pixels', cv2.countNonZero(mask))
```

在 Thonny 選 **File → Open** 開啟練習資料夾中的 `第26課.py`，確認右下角解譯器後點綠色執行鈕。

## 先前終端機實測輸出（合成影格；Thonny 尚待重測）

```text
changed pixels 400
```

20 × 20 等於 400，輸出顯示這些像素被標記；真實場景還需處理光線、雜訊與相機移動。

## RP5 實際產生的結果圖

![第 26 課的實際程式輸出](./圖檔/lesson26-difference.png)

由左至右為背景、目前影格與差分遮罩。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 背景與核心概念

### 如何從兩張畫面看出變化？

背景差分先比較基準影格與目前影格，再用閾值把差異轉成遮罩。影像的亮度變動也會形成差異，因此偵測到變化不一定代表有物體移動。

### 閾值與遮罩怎麼解讀？

將兩張灰階影像的同一位置相減並取絕對值，就得到每個像素的亮度差。差值高於門檻時，二值化遮罩標為白色，其餘為黑色。例如第 26 課的 20 × 20 白色方塊含 400 個像素，因此在合成資料中可用 400 檢查計數；這個例子沒有雜訊，也不代表所有實景都會如此整齊。

門檻太低時，攝影雜訊或光線變化可能被誤判；太高時，小變化可能被忽略。看短影片的首末影格時，目標舊位置與新位置可能同時變白，因為兩處亮度都改變。若想評估固定鏡頭的門禁或設備狀態，可先保存不同光線下的資料，比較誤報與漏報，再決定是否使用。

### 思考、練習與後續應用

若白色方塊是 20 × 20 像素，遮罩白色像素可能是多少？改變光線或移動相機會對差分造成什麼影響？

背景差分適用固定鏡頭的入門偵測，部署時需測試陰影、光線、抖動與誤報。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 進階實測：處理 RP5 相機拍攝的短影片

### 實驗材料與步驟

1. 先依[第 16 課](./第%2016%20課｜Python%20結合%20OpenCV%20與%20Picamera2：影片錄製與即時影像處理.md)拍攝螢幕動畫，或下載[本次處理後的短影片](./練習素材/lesson16-camera.avi)，存為練習目錄中的 `lesson16-camera.avi`。本次使用的影片是 12 張經裁切、透視校正及灰階處理的 RP5 相機影格。
2. 將[本課範例程式](./範例程式/第26課-影片影格差分.py)放到相同目錄；執行前確認輸出檔不會覆蓋你的資料。本課差分範例不需要 `bgsegm` 擴充模組。

```python
import cv2

video = cv2.VideoCapture('lesson16-camera.avi')
frames = []
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        frames.append(frame)
finally:
    video.release()
if len(frames) < 2:
    raise RuntimeError('影片必須至少包含兩張影格，請先完成第 16 課')
first = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
last = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY)
diff = cv2.absdiff(first, last)
_, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
panels = cv2.hconcat([frames[0], frames[-1], cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
if not cv2.imwrite('lesson26-camera-diff.png', panels):
    raise RuntimeError('無法儲存結果圖')
print('frames read:', len(frames))
print('first and last changed pixels:', cv2.countNonZero(mask))
print('saved: lesson26-camera-diff.png')
```

在 Thonny 選 **File → Open** 開啟同一練習資料夾中的程式，檢查右下角解譯器，再按綠色執行鈕。

### 本次 Thonny 在 RP5 的實際輸出

```text
frames read: 12
first and last changed pixels: 10359
saved: lesson26-camera-diff.png
```

![第 26 課在 Thonny 的程式及 Shell 實際截圖](./圖檔/lesson26-thonny-clean.png)

截圖中的 `lesson26.py` 是儲存庫範例程式的測試副本，內容相同；右下角為本次獨立擴充環境。

![第 26 課相機短影片的實際處理結果](./圖檔/lesson26-camera-diff.png)

左圖是影片第一張影格，中圖是最後一張，右圖白色代表兩張灰階圖亮度差超過門檻的位置。可以看到圓形的原位置和新位置都出現白色，因為兩處像素都發生變化；左上角影格編號不同也造成白色文字，因此不能把每個白點都當成物體。 此圖是相機影片經程式處理的結果，不是操作截圖；原始相機全景沒有上傳。

### 學生練習與限制

找出圖中除了圓形以外被標成白色的區域，說明它為什麼可能改變。嘗試使用不同閾值或更多影格，記錄遮罩的變化；不要根據這段短影片就宣稱已完成真實場景或長時間的準確率評估。

## 與原文章的差異

- 本次改用 Thonny 與隔離的 OpenCV 擴充環境；逐項可重現範圍以上方截圖與文字為準。

- 原文使用影片或相機；本版的初步範例採可重現的合成影格，另增加相機短影片測試，沒有把測試結果視為實際監測效果。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 新增本次 Thonny 實際操作截圖；其餘情境仍按段落標示測試範圍。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 原文使用影片或相機；本版先做固定合成影格測試，新增由 RP5 相機實拍的短影片首末影格差分。
