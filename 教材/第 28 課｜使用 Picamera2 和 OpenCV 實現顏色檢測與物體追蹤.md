# 第 28 課｜使用 Picamera2 和 OpenCV 實現顏色檢測與物體追蹤

[原始文章](https://liusming.pixnet.net/blog/posts/14222886522) · 更新日期：2026-10-29

## 學習目標

利用 HSV 閾值建立顏色遮罩。

## 事前準備

需要 OpenCV 與 NumPy；合成圖中含 20 × 20 紅色區塊。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第28課.py`，或使用[已測試的範例程式](./範例程式/第28課.py)。

```python
import cv2
import numpy as np
image = np.zeros((100, 100, 3), dtype=np.uint8)
image[20:40, 30:50] = (0, 0, 255)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
print('red pixels', cv2.countNonZero(mask))
```

在該檔案所在目錄執行 `python3 第28課.py`。

## 本機實際輸出

```text
red pixels 400
```

此例僅使用紅色 HSV 的一段範圍；真實場景需要根據相機與照明調整，紅色也可能跨越色相邊界。

## 與原文章的差異

- 原文以相機追蹤顏色；本版先驗證固定合成圖的遮罩與像素數，未測即時追蹤。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
