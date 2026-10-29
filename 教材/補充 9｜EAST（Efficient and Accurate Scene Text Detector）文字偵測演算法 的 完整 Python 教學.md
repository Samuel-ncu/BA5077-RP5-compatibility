# 補充 9｜EAST（Efficient and Accurate Scene Text Detector）文字偵測演算法 的 完整 Python 教學

[原始文章](https://liusming.pixnet.net/blog/posts/14223038337) · 更新日期：2026-10-29

## 學習目標

載入 EAST 模型，對合成英文影像偵測文字框、執行 NMS 並保存結果。

## 事前準備

需要 OpenCV、NumPy、EAST frozen graph 及 east_helpers.py。

先將[文字框處理程式 east_helpers.py](./範例程式/east_helpers.py)放在練習目錄，並下載本次測試模型（約 97 MB）：

```bash
curl -fL https://raw.githubusercontent.com/oyyd/frozen_east_text_detection.pb/master/frozen_east_text_detection.pb -o frozen_east_text_detection.pb
```

## 程式與執行

將以下程式存為 `補充9.py`，或使用[已測試的範例程式](./範例程式/補充9.py)。在檔案所在目錄執行 `python3 補充9.py`。

```python
import cv2
import numpy as np
from east_helpers import detect_text

net = cv2.dnn.readNet('frozen_east_text_detection.pb')
image = np.full((320, 320, 3), 255, dtype=np.uint8)
cv2.putText(image, 'HELLO 123', (15, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 2)
boxes = detect_text(net, image)
for x1, y1, x2, y2 in boxes:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
print('text boxes', len(boxes))
print('saved', cv2.imwrite('supplement9-east.png', image))
```

## 本機實際輸出

```text
text boxes 2
saved True
```

本例在合成英文上偵測到兩個框；不同圖片與模型版本的結果可能不同，未衡量真實場景準確率。

本機產生的結果圖（這是程式輸出，不是螢幕截圖）：

![EAST 文字框](./圖檔/supplement9-east.png)

## 背景與核心概念

### 文字偵測與文字辨識

EAST 偵測影像中可能有文字的區域；它本身不保證輸出文字內容。候選框可能重疊，非極大值抑制（NMS）可協助保留較適合的框。

### 思考、練習與後續應用

解釋文字區域偵測和 OCR 字元辨識的差別；合成英文圖成功是否代表中文、旋轉或模糊文字也成功？

文字偵測可用於文件擷取和標牌輔助閱讀，還需測試不同字體、角度、語言及隱私。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)。請以下方實測狀態為準；尚未實作或測試的情境不能視為已通過。

## 與原文章的差異

- 原文使用外部圖片並顯示視窗；本版使用可重現的合成圖片、保存結果並附上實測輸出。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
