# 補充 9｜EAST（Efficient and Accurate Scene Text Detector）文字偵測演算法 的 完整 Python 教學

[原始文章](https://liusming.pixnet.net/blog/posts/14223038337) · 更新日期：2026-10-29

## 學習目標

載入 EAST 模型並確認對合成空白圖的兩個輸出張量。

## 事前準備

需要 OpenCV、NumPy 與 EAST frozen graph 模型。

在練習目錄下載本次測試模型（約 97 MB）：

```bash
curl -fL https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb -o frozen_east_text_detection.pb
```

## 程式與執行

將以下程式存為 `補充9.py`，或使用[已測試的範例程式](./範例程式/補充9.py)。在檔案所在目錄執行 `python3 補充9.py`。

```python
import cv2
import numpy as np

net = cv2.dnn.readNet('frozen_east_text_detection.pb')
image = np.zeros((320, 320, 3), dtype=np.uint8)
blob = cv2.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
scores, geometry = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])
print('scores shape', scores.shape)
print('geometry shape', geometry.shape)
```

## 本機實際輸出

```text
scores shape (1, 1, 80, 80)
geometry shape (1, 5, 80, 80)
```

此測試只確認模型前向運算與輸出維度；沒有解析框、套用 NMS，也沒有實際文字偵測結果。

## 與原文章的差異

- 原文包含文字框解析與顯示；本版先驗證模型載入及輸出，完整偵測後處理尚待實測。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
