# 第 19 課｜使用 OpenCV 繪製直線、圓形、橢圓與多邊形

[原始文章](https://liusming.pixnet.net/blog/posts/14222886411) · 更新日期：2026-10-29

> 本課基本繪圖程式已在 Thonny 重新執行；既有 Trixie 的 Thonny 繪圖、存檔與顯示視窗已有下方實測；原文其他情境依下文標示。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

## 學習目標

在合成畫布上繪製線條、矩形、圓形、橢圓與多邊形，並存成圖片。

## 事前準備

依[Thonny 環境指南](./Thonny環境與套件安裝.md)準備 OpenCV 與 NumPy，確認 Thonny 選擇安裝了這些套件的環境；程式會寫入 `lesson19-shapes.png`。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第19課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第19課.py)。

```python
import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.line(image, (10, 20), (200, 20), (0, 255, 0), 3)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), 2)
cv2.circle(image, (240, 90), 40, (0, 0, 255), 3)
cv2.ellipse(image, (160, 190), (50, 20), 0, 0, 360, (255, 255, 255), 2)
points = np.array([[20, 150], [65, 135], [105, 160], [55, 225]], dtype=np.int32)
cv2.polylines(image, [points], True, (0, 255, 255), 2)
print("saved", cv2.imwrite("lesson19-shapes.png", image))
```

在 Thonny 選擇 **File → Open** 開啟 `第19課.py`，確認右下角為準備好的環境，再點綠色執行按鈕。程式會在工作目錄寫入圖片；先確認不會覆寫自己的檔案。

## Thonny 實測輸出

```text
saved True
```

圖片可用來比較不同圖形的座標、顏色與線寬；OpenCV 的顏色參數一般使用 BGR 順序。

![RP5 上 Thonny 執行第 19 課程式及 Shell 輸出](./圖檔/lesson19-thonny.png)

本次 Thonny 使用 OpenCV 4.10.0 在 RP5 產生的圖檔：

![本次程式輸出](./圖檔/lesson19-thonny-result.png)

## 背景與核心概念

### 程式如何在影像上畫圖？

OpenCV 將圖片視為像素陣列，繪製函式會改變指定位置的像素。通常左上角是原點，x 向右、y 向下；顏色常以 BGR 順序指定。

### 思考、練習與後續應用

說出線條起點、終點、顏色和粗細分別影響什麼；畫在影像外的位置會有什麼問題？

繪圖可用來標示偵測框和測量結果，但標註不代表模型判斷一定正確。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 逐步看懂繪圖座標與參數

畫布的陣列形狀是 `(240, 320, 3)`，表示高 240、寬 320、三個色彩通道；左上角為 `(0, 0)`，x 向右增加、y 向下增加。`line` 使用起點和終點；`rectangle` 使用兩個角；`circle` 使用圓心和半徑；`ellipse` 還需要長短半軸及角度。

`points` 是依序排列的多邊形頂點。`polylines` 的 `True` 代表連回起點，形成封閉輪廓。OpenCV 常用 BGR 色彩順序，本次 `(0, 255, 255)` 是黃色；線寬 2 表示以兩像素左右的粗細畫線。修改後請重新觀察圖形，畫面超出邊界可能被裁切。

### 練習

修改多邊形的一個頂點並保存新圖；比較修改前後的形狀。再嘗試將 `True` 改為 `False`，觀察起點與終點是否連接。這些變化請學生自行操作並記錄。

## 先前測試：RP5 圖形桌面顯示結果

先前以終端機和系統 OpenCV 開啟同一類結果圖，保留視窗截圖作為歷史紀錄；**這張圖不是 Thonny 執行截圖**。此歷史紀錄當時尚未完成 Thonny 視窗流程；現有 Trixie 的新實測見下節。可先在[第 14 課](./Thonny環境與套件安裝.md)練習經 Thonny 開啟基本 OpenCV 視窗。

![先前終端機測試的 OpenCV 結果視窗](./圖檔/lesson19-opencv-window.png)

## 2026-11-10：現有 Trixie 的 Thonny 繪圖與視窗

本次使用既有 Trixie、Thonny 所選 `/home/pi/opencv-course-env/bin/python3`、Python 3.13.5 與 OpenCV 4.12.0；這不是新重灌系統。下列[完整範例](./範例程式/第19課-繪圖與視窗-trixie.py)每次建立新的暫存資料夾以避免覆寫，並將位置印在 Shell。`/tmp` 可能被系統清除，需保留的作品請另存。

在 Thonny 開啟或輸入程式，選擇含 OpenCV 和 NumPy 的解譯器，按 F5 執行。看到視窗後點選它並按任意鍵；未按鍵時最多等 60 秒。

```python
from pathlib import Path
from tempfile import mkdtemp
import cv2
import numpy as np

folder = Path(mkdtemp(prefix='ba5077-lesson19-'))
image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.line(image, (10, 20), (200, 20), (0, 255, 0), 3)
cv2.rectangle(image, (20, 40), (140, 120), (255, 0, 0), 2)
cv2.circle(image, (240, 90), 40, (0, 0, 255), 3)
cv2.ellipse(image, (160, 190), (50, 20), 0, 0, 360, (255, 255, 255), 2)
points = np.array([[20, 150], [65, 135], [105, 160], [55, 225]], dtype=np.int32)
cv2.polylines(image, [points], True, (0, 255, 255), 2)
print('saved:', cv2.imwrite(str(folder / 'shapes.png'), image))
print('folder:', folder)
cv2.imshow('Shapes', image)
print('Window open', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
```

本次輸出節錄如下；暫存資料夾名稱每次不同：

```text
saved: True
folder: /tmp/ba5077-lesson19-3azpk1h9
Window open
Window closed
```

Shell 另出現找不到 Qt `wayland` 平台外掛的訊息，本次圖形視窗仍正常顯示及關閉。若看不到視窗，需檢查桌面工作階段、所選環境與完整錯誤訊息。`saved: True` 表示本次寫檔成功；另以檔案工具確認產出為 320×240 PNG。

![Thonny 程式與 OpenCV 圖形視窗](./圖檔/lesson19-trixie-thonny-window-20261110.jpg)

*圖：本次 Thonny 與圖形視窗的實際畫面，圖形為程式生成。*

![關閉圖形視窗後的 Shell](./圖檔/lesson19-trixie-thonny-closed-20261110.jpg)

*圖：本次按鍵關閉後的實際輸出。*

## 與原文章的差異

- 新增在 Thonny 所選獨立環境執行繪圖並保存結果的截圖和輸出。

- 本版以合成畫布繪圖；既有 Trixie 已在 Thonny 測試存檔、圖形視窗與關閉，並非全新系統驗證。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 新增實際 OpenCV 圖形視窗的操作截圖；先前結果圖仍是程式存檔。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 重新執行後新增多邊形，讓實作涵蓋原文標題中的各種圖形。
