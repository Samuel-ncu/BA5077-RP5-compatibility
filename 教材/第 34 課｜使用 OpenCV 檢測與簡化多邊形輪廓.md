# 第 34 課｜使用 OpenCV 檢測與簡化多邊形輪廓

[原始文章](https://liusming.pixnet.net/blog/posts/14222886567) · 更新日期：2026-10-29

## 學習目標

用輪廓周長計算近似多邊形。

## 事前準備

需要 OpenCV、NumPy；本例建立矩形二值圖。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第34課.py`，或使用[已測試的範例程式](./範例程式/第34課.py)。

```python
import cv2
import numpy as np
image = np.zeros((100, 100), dtype=np.uint8)
cv2.rectangle(image, (20, 20), (70, 70), 255, -1)
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
approx = cv2.approxPolyDP(contours[0], 0.02 * cv2.arcLength(contours[0], True), True)
result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.polylines(result, [approx], True, (0, 0, 255), 2)
if not cv2.imwrite('lesson34-polygon.png', result):
    raise RuntimeError('image save failed')
print('polygon vertices', len(approx))
```

在該檔案所在目錄執行 `python3 第34課.py`。

## 本機實際輸出

```text
polygon vertices 4
```

矩形近似得到四個頂點；若變更 epsilon 或圖片形狀，頂點數可能改變。

## RP5 實際產生的結果圖

![第 34 課的實際程式輸出](./圖檔/lesson34-polygon.png)

合成矩形與近似多邊形。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 背景與核心概念

### 為什麼要簡化輪廓？

數位輪廓可能包含許多點；多邊形近似以允許的誤差 epsilon 保留較少頂點。誤差越大可能越簡化，也可能漏掉重要形狀細節。

### 思考、練習與後續應用

對同一輪廓使用不同 epsilon，觀察頂點數；說明四個頂點不一定就代表影像中的物體是完美矩形。

輪廓簡化可減少形狀分析的資料量，但參數應依物件尺寸與量測目的調整。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 與原文章的差異

- 原文使用外部圖片；本版使用合成矩形，並列出此機器的實際頂點數。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
