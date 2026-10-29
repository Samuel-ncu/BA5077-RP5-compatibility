# 第 17 課｜使用 OpenCV 讀取灰階圖檔

[原始文章](https://liusming.pixnet.net/blog/posts/14222886366) · 更新日期：2026-10-29

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

在該檔案所在的目錄執行 `python3 第17課.py`。

## 本機實際輸出

```text
color (240, 320, 3)
grayscale (240, 320) uint8
saved True
```

`saved True` 表示 OpenCV 成功寫入圖片。灰階圖片只有一個通道；若寫入失敗，檢查目前資料夾權限。

本次 RP5 程式實際產生的圖檔：

![本次程式輸出](./圖檔/lesson17-gray.png)

## 與原文章的差異

- 原文讀取外部 `demo.jpeg`；本版使用合成圖像，不依賴未提供的圖片。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 尚未補拍操作畫面；圖檔（若有）是程式產生的結果，不冒充螢幕截圖。
