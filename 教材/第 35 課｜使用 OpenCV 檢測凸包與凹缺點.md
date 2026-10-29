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

## 背景與核心概念

### 凸包與凹缺陷是什麼？

凸包可想成用橡皮筋包住輪廓最外圍形成的凸形邊界；凸缺陷描述輪廓相對凸包向內凹陷的位置。影像雜訊與輪廓點的順序可能影響結果。

### 思考、練習與後續應用

解釋一個凹多邊形為什麼可能有凸缺陷；改變點的位置後，凸包和缺陷是否仍相同？

凸包與缺陷可輔助輪廓分析，例如檢查形狀，但不能直接推論手勢或真實物件的身分。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 與原文章的差異

- 原文使用外部圖片；本版以固定多邊形驗證凸包和凹缺陷 API，未測試原圖。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
