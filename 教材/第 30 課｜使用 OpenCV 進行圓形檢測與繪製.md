# 第 30 課｜使用 OpenCV 進行圓形檢測與繪製

[原始文章](https://liusming.pixnet.net/blog/posts/14222886537) · 更新日期：2026-10-29

## 學習目標

使用 HoughCircles 偵測合成圖中的圓。

## 事前準備

需要 OpenCV 與 NumPy；先在黑色背景畫一個圓。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第30課.py`，或使用[已測試的範例程式](./範例程式/第30課.py)。

```python
import cv2
import numpy as np
image = np.zeros((200, 200), dtype=np.uint8)
cv2.circle(image, (100, 100), 40, 255, 3)
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 30, param1=100, param2=20, minRadius=30, maxRadius=50)
print('circle detected', circles is not None)
```

在該檔案所在目錄執行 `python3 第30課.py`。

## 本機實際輸出

```text
circle detected True
```

參數對尺寸與影像品質敏感；本結果只證明合成例子成功，不能保證其他圖片使用相同參數也能偵測。

## 與原文章的差異

- 原文讀取外部杯子圖片；本版使用可重現的合成圓，未驗證原始圖片。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
