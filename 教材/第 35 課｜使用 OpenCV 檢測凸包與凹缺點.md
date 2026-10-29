# 第 35 課｜使用 OpenCV 檢測凸包與凹缺點

[原始文章](https://liusming.pixnet.net/blog/posts/14222886573) · 更新日期：2026-10-29

## 學習目標

建立凸包並計算輪廓的凸缺陷。

## 事前準備

需要 OpenCV、NumPy；本例建立五個頂點的合成凹多邊形。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第35課.py`，或使用[已測試的範例程式](./範例程式/第35課.py)。

```python
import cv2
import numpy as np
points = np.array([[10, 10], [80, 10], [80, 80], [50, 50], [10, 80]], dtype=np.int32).reshape(-1, 1, 2)
hull = cv2.convexHull(points, returnPoints=False)
defects = cv2.convexityDefects(points, hull)
image = np.zeros((100, 100, 3), dtype=np.uint8)
cv2.polylines(image, [points], True, (255, 255, 255), 1)
cv2.polylines(image, [cv2.convexHull(points)], True, (0, 255, 0), 1)
if defects is not None:
    for defect in defects:
        far = tuple(int(v) for v in points[defect[0][2], 0])
        cv2.circle(image, far, 3, (0, 0, 255), -1)
if not cv2.imwrite('lesson35-hull.png', image):
    raise RuntimeError('image save failed')
print('hull indices', len(hull))
print('defect count', 0 if defects is None else len(defects))
```

在該檔案所在目錄執行 `python3 第35課.py`。

## 本機實際輸出

```text
hull indices 4
defect count 1
```

凸包包住原輪廓；凹缺陷數會受點序與輸入形狀影響。

## RP5 實際產生的結果圖

![第 35 課的實際程式輸出](./圖檔/lesson35-hull.png)

白色為輪廓、綠色為凸包、紅色為凸缺陷位置。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 與原文章的差異

- 原文使用外部圖片；本版以固定多邊形驗證凸包和凹缺陷 API，未測試原圖。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
