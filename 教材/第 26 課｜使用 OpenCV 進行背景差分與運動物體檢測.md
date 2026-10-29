# 第 26 課｜使用 OpenCV 進行背景差分與運動物體檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886516) · 更新日期：2026-10-29

## 學習目標

用影像差分與閾值找出變動像素。

## 事前準備

需要 OpenCV 與 NumPy；本例在黑色背景建立 20 × 20 的白色區域。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第26課.py`，或使用[已測試的範例程式](./範例程式/第26課.py)。

```python
import cv2
import numpy as np
background = np.zeros((100, 100), dtype=np.uint8)
current = background.copy()
current[20:40, 30:50] = 255
diff = cv2.absdiff(background, current)
_, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
print('changed pixels', cv2.countNonZero(mask))
```

在該檔案所在目錄執行 `python3 第26課.py`。

## 本機實際輸出

```text
changed pixels 400
```

20 × 20 等於 400，輸出顯示這些像素被標記；真實場景還需處理光線、雜訊與相機移動。

## 與原文章的差異

- 原文使用影片或相機；本版採可重現的合成影格，沒有把合成結果視為實際監測效果。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
