# 第 22 課｜使用 OpenCV 進行臉部檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886426) · 更新日期：2026-10-29

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

## 與原文章的差異

- 原文使用外部圖片與相對路徑的 XML；本版使用本機已驗證的絕對路徑與合成圖。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
