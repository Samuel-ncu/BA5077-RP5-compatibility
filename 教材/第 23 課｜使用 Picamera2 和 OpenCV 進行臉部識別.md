# 第 23 課｜使用 Picamera2 和 OpenCV 進行臉部識別

[原始文章](https://liusming.pixnet.net/blog/posts/14222876475) · 更新日期：2026-10-29

## 學習目標

了解 LBPH 臉部辨識器的訓練與預測流程。

## 事前準備

需要支援 `cv2.face` 的 OpenCV；本例使用兩張均勻合成圖。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第23課.py`，或使用[已測試的範例程式](./範例程式/第23課.py)。

```python
import cv2
import numpy as np
images = [np.full((100, 100), 40, dtype=np.uint8), np.full((100, 100), 200, dtype=np.uint8)]
labels = np.array([0, 1], dtype=np.int32)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, labels)
label, confidence = recognizer.predict(images[0])
print('LBPH trained', True)
print('predicted label', label)
```

在該檔案所在目錄執行 `python3 第23課.py`。

## 本機實際輸出

```text
LBPH trained True
predicted label 0
```

此測試只驗證 API 可以訓練並辨識訓練資料，不是真人臉部辨識，也沒有評估準確率或隱私資料。

## 與原文章的差異

- 原文使用人臉資料集與相機；本版先以合成資料驗證流程，不把合成結果當成真人辨識成果。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
