# 第 27 課｜使用背景減法與 MOG 進行運動物體檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886498) · 更新日期：2026-10-29

## 學習目標

認識背景模型並確認本機 GMG 物件可以處理影格。

## 事前準備

本機 OpenCV 需包含 `cv2.bgsegm` 擴充模組。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第27課.py`，或使用[已測試的範例程式](./範例程式/第27課.py)。

```python
import cv2
import numpy as np
subtractor = cv2.bgsegm.createBackgroundSubtractorGMG()
frame = np.zeros((40, 40, 3), dtype=np.uint8)
mask = subtractor.apply(frame)
print('GMG created', True)
print('mask shape', mask.shape)
```

在該檔案所在目錄執行 `python3 第27課.py`。

## 本機實際輸出

```text
GMG created True
mask shape (40, 40)
```

輸出遮罩尺寸與輸入相同；第一張影格不能代表背景模型已完成學習。

## 與原文章的差異

- 原文以相機持續更新背景；本版先驗證建立 GMG 和處理單張圖，不宣稱完成動態偵測。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
