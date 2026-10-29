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
if not cv2.imwrite('lesson27-gmg-mask.png', mask):
    raise RuntimeError('image save failed')
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

## RP5 實際產生的結果圖

![第 27 課的實際程式輸出](./圖檔/lesson27-gmg-mask.png)

這是第一張影格產生的遮罩；背景模型尚未完成學習，不能作為移動物體偵測成果。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 背景與核心概念

### 背景模型為何需要時間？

背景減法不是只比較一張固定底圖；演算法可從多張影格建立或更新背景模型，再推測哪些像素屬於前景。MOG 系列與 GMG 是不同方法，參數和結果不能直接視為相同。

### 思考、練習與後續應用

第一張影格的遮罩為何不足以評估動態偵測？請指出本篇範例建立的是哪一種背景模型，是否等同原文的 MOG。

適合進一步研究固定相機場景，但需要連續影格、適應時間與多種光線的實測。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 與原文章的差異

- 原文以相機持續更新背景；本版先驗證建立 GMG 和處理單張圖，不宣稱完成動態偵測。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
