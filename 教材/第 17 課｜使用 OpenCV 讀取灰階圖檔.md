# 第 17 課｜使用 OpenCV 讀取灰階圖檔

[原始文章](https://liusming.pixnet.net/blog/posts/14222886366) · 更新日期：2026-10-29

> 本課已在 Thonny 實測：合成彩色圖轉灰階並存檔。完整原文情境及其他舊案例仍須依下文標示重測。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

## 學習目標

建立合成彩色圖像，轉成灰階並儲存，以觀察彩色與灰階陣列的差異。

## 事前準備

系統 OpenCV 與 NumPy 已可匯入；程式在目前目錄寫入 `lesson17-gray.png`。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第17課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第17課.py)。

```python
import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), -1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("color", image.shape)
print("grayscale", gray.shape, str(gray.dtype))
print("saved", cv2.imwrite("lesson17-gray.png", gray))
```

在 Thonny 選 **File → Open** 開啟 `第17課.py`，確認右下角是包含所需套件的 Python 環境，再點綠色執行鈕。若程式會輸出檔案，先在新的練習目錄操作，避免覆寫。

## Thonny 實測輸出

```text
color (240, 320, 3)
grayscale (240, 320) uint8
saved True
```

![第 17 課在 Thonny 的程式與 Shell 實際畫面](./圖檔/lesson17-thonny2.png)

本次選用既有環境 `/home/pi/myenv/bin/python3`。本次基本範例先產生合成圖；下方另以 Thonny 讀取先前的相機實拍素材。此段的舊環境圖形視窗當時待重測；現有 Trixie 的 Thonny 結果見下方。 相機或影像相關套件的準備及可重現環境請參考[Thonny 環境指南](./Thonny環境與套件安裝.md)。

`saved True` 表示 OpenCV 成功寫入圖片。灰階圖片只有一個通道；若寫入失敗，檢查目前資料夾權限。

本次 RP5 程式實際產生的圖檔：

![本次程式輸出](./圖檔/lesson17-gray.png)

## 背景與核心概念

### 為什麼要讀取灰階圖片？

灰階影像以單一通道表示亮度，適合某些邊緣或形狀處理；彩色資訊會在轉換中消失。影像陣列的索引通常先是列（高度），再是欄（寬度）。

### 思考、練習與後續應用

比較彩色影像與灰階影像的通道數；解釋灰階可能讓哪些原本顏色不同的區域變得難以區分。

灰階可用於文件或輪廓的前處理；如果任務依賴顏色區分，應保留彩色資料。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## Thonny 進階實測：把相機實拍圖片讀成灰階

上面的初步範例建立合成圖片並轉換灰階；原文主題則是**讀取圖片檔**。本次另使用第 40 課由 RP5 拍攝螢幕測試素材、裁切並校正的[實拍影像](./圖檔/objects-board.png)。請下載該圖，存為 `objects-board.png`，放在下列[範例程式](./範例程式/第17課-讀取實拍灰階.py)的練習目錄。

```python
import cv2

# objects-board.png 是第 40 課的相機實拍測試圖，已裁切並透視校正。
image = cv2.imread('objects-board.png', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise RuntimeError('無法讀取 objects-board.png，請確認檔案與目錄')
print('gray shape', image.shape)
print('gray dtype', image.dtype)
print('saved', cv2.imwrite('lesson17-camera-gray.png', image))
```

在 Thonny 選擇 **File → Open** 開啟 `第17課-讀取實拍灰階.py`，確認素材和程式位於同一個練習目錄，再按綠色執行按鈕。

本次 RP5 實際輸出：

```text
gray shape (675, 1200)
gray dtype uint8
saved True
```

![相機實拍素材讀為灰階的結果](./圖檔/lesson17-camera-gray.png)

`cv2.IMREAD_GRAYSCALE` 在讀檔時取得單通道影像。圖中的物件原本由 AI 生成，先顯示於螢幕，再由 RP5 相機拍攝，最後裁切、校正和讀成灰階；它不是實拍真實水果，也不是操作截圖。`image is None` 用來檢查讀檔失敗，避免後續處理空資料。

### 練習

比較[彩色輸入](./圖檔/objects-board.png)與灰階輸出，說明哪些顏色資訊消失。將圖片檔名改成不存在的名稱，觀察程式如何提示，再改回正確名稱。

![Thonny 中讀取灰階圖片的程式與輸出](./圖檔/thonny2-lesson17-read.png)

## 舊實驗紀錄（終端機；待 Thonny 重測）：在桌面顯示合成灰階圖

先用本文範例產生 `lesson17-gray.png`，把[圖形視窗程式](./範例程式/OpenCV-圖形視窗.py)放在同一練習目錄，在 RP5 桌面執行：

```bash
python3 OpenCV-圖形視窗.py lesson17-gray.png
```

```python
import sys
import cv2

if len(sys.argv) != 2:
    raise SystemExit('用法：python3 OpenCV-圖形視窗.py 圖片檔名')
image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
if image is None:
    raise SystemExit('無法讀取圖片，請檢查路徑')
print('image shape:', image.shape, flush=True)
cv2.imshow('OpenCV image - press any key', image)
print('window opened; press any key or wait 60 seconds', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('window closed', flush=True)
```

本次使用 RP5 系統 OpenCV 實際輸出節錄：

```text
image shape: (240, 320)
window opened; press any key or wait 60 seconds
window closed
```

![RP5 顯示灰階圖片的視窗截圖](./圖檔/lesson17-opencv-window.png)

這是遠端桌面擷取並裁切的操作截圖；圖中的灰色矩形是合成資料，滑鼠游標也出現在視窗中。顯示灰階圖需要圖形桌面與支援 GUI 的 OpenCV；本次沒有測試原文外部圖片。視窗程式在取得按鍵或等待 60 秒後結束。

## 2026-11-10：既有 Trixie 的 Thonny 灰階讀檔與視窗

本次在既有 Trixie、Thonny 選用 `/home/pi/opencv-course-env/bin/python3`（Python 3.13.5、OpenCV 4.12.0），讀取既有[相機測試素材](./圖檔/objects-board.png)。該素材原為生成圖，經顯示器呈現、RP5 相機拍攝並裁切校正；不代表拍攝了真實水果。這不是全新系統實測。

1. 建立自己的空練習資料夾，下載上述素材並命名為 `objects-board.png`；記下資料夾的完整路徑。執行會寫入 `gray-output.png`，若已有同名檔會覆寫，請先確認位置。
2. 在 Thonny 選擇已安裝 OpenCV 且支援圖形視窗的解譯器，開啟或輸入[本次範例](./範例程式/第17課-灰階讀圖顯示-trixie.py)。將 `folder` 改為自己練習資料夾的路徑；下方路徑只屬於本次測試，重開機後 `/tmp` 可能被清理。
3. 按 F5 執行。在出現的 `Gray image` 視窗點一下，再按任意鍵關閉；未按鍵時程式最多等 60 秒。觀察 Shell 並確認 `saved: True`。

```python
from pathlib import Path
import cv2

folder = Path('/tmp/ba5077-lesson17-tPp3k0')
image = cv2.imread(str(folder / 'objects-board.png'), cv2.IMREAD_GRAYSCALE)
if image is None:
    raise RuntimeError('Cannot read image; check path')
print('gray shape:', image.shape)
print('gray dtype:', image.dtype)
print('saved:', cv2.imwrite(str(folder / 'gray-output.png'), image))
cv2.namedWindow('Gray image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Gray image', 800, 450)
cv2.imshow('Gray image', image)
print('Window open: press any key or wait 60 seconds', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
```

本次 Thonny 的輸出（除程式文字外，另有下述 Qt 訊息）：

```text
gray shape: (675, 1200)
gray dtype: uint8
saved: True
Window open: press any key or wait 60 seconds
Window closed
```

![Thonny 顯示灰階圖像與輸出](./圖檔/lesson17-trixie-thonny-window-20261110.jpg)

*圖：本次 RP5 桌面分享中的 Thonny 與 OpenCV 實際視窗。*

![關閉灰階視窗後的程式與輸出](./圖檔/lesson17-trixie-thonny-closed-20261110.jpg)

*圖：按鍵關閉後的實際 Shell 輸出。* 此次出現 Qt 找不到 `wayland` 平台外掛的訊息，視窗仍正常出現並可關閉；其他系統若沒有視窗，應檢查圖形桌面、OpenCV 安裝變體與完整錯誤訊息，不要將此警告當作所有情況都可忽略。另以同一環境讀回產出的 PNG，確認形狀 `(675, 1200)`、型別 `uint8`。若 `saved` 為 `False`，檢查資料夾權限與路徑。

## 與原文章的差異

- 新增以 Thonny 操作的實測與截圖：合成彩色圖轉灰階並存檔。

- 原文讀取外部 `demo.jpeg`；本版使用合成圖像，不依賴未提供的圖片。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 新增合成灰階圖在 OpenCV 視窗中顯示的操作截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 新增使用 `cv2.imread(..., cv2.IMREAD_GRAYSCALE)` 讀取 RP5 實拍後校正影像的實測；本版另以合成圖片驗證圖形視窗；原文圖片未測。
