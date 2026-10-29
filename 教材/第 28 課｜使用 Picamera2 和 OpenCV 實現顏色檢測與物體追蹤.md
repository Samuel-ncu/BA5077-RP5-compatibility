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
if not cv2.imwrite('lesson28-mask.png', np.hstack((image, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))):
    raise RuntimeError('image save failed')
print('red pixels', cv2.countNonZero(mask))
```

在該檔案所在目錄執行 `python3 第28課.py`。

## 本機實際輸出

```text
red pixels 400
```

此例僅使用紅色 HSV 的一段範圍；真實場景需要根據相機與照明調整，紅色也可能跨越色相邊界。

## RP5 實際產生的結果圖

![第 28 課的實際程式輸出](./圖檔/lesson28-mask.png)

左側為合成紅色區塊，右側為 HSV 遮罩。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 使用 RP5 相機拍攝螢幕色塊的實測

2026-10-29 使用本機 IMX708 廣角相機拍攝螢幕上的紅、綠、藍、黃色塊。以下是**單張照片**的紅色偵測，不是即時追蹤。照片中包含螢幕外的紅色物品，所以此例先限制偵測區域（ROI）。本次只公開裁切後的紅色目標與遮罩，未公開完整相機照片。

先在練習目錄拍攝照片；拍攝前需讓相機處於未被其他程式占用的狀態：

```bash
rpicam-still --nopreview --timeout 2000 --width 1920 --height 1080 --output lesson28-camera.jpg
```

將下列程式存為 `第28課-相機照片偵測.py`，也可使用[範例程式](./範例程式/第28課-相機照片偵測.py)。程式中的 ROI 僅對應這次 1920 × 1080 的拍攝位置；相機或螢幕移動後，請重新設定座標及 HSV 閾值。

```python
import cv2
import numpy as np

# 先使用 rpicam-still 拍攝 lesson28-camera.jpg，再依實際畫面調整 ROI。
image = cv2.imread('lesson28-camera.jpg')
if image is None:
    raise RuntimeError('找不到 lesson28-camera.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 130, 100), (10, 255, 255)) | cv2.inRange(hsv, (170, 130, 100), (179, 255, 255))
# 本次相機為 1920×1080；這個 ROI 是此次拍攝螢幕的範圍。
mask[:200, :] = 0
mask[600:, :] = 0
mask[:, :700] = 0
mask[:, 1500:] = 0
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = [c for c in contours if cv2.contourArea(c) >= 1000]
if not contours:
    raise RuntimeError('沒有找到夠大的紅色區域；請調整 ROI 與 HSV 範圍')
contour = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(contour)
margin = 30
x0, y0 = max(0, x - margin), max(0, y - margin)
x1, y1 = min(image.shape[1], x + w + margin), min(image.shape[0], y + h + margin)
sample = image[y0:y1, x0:x1].copy()
cv2.rectangle(sample, (x-x0, y-y0), (x-x0+w-1, y-y0+h-1), (0, 255, 0), 2)
panel = np.hstack((sample, cv2.cvtColor(mask[y0:y1, x0:x1], cv2.COLOR_GRAY2BGR)))
if not cv2.imwrite('lesson28-camera-mask.png', panel):
    raise RuntimeError('無法儲存結果圖片')
print('input camera image:', image.shape)
print('large red regions:', len(contours))
print('largest red box (x, y, w, h):', x, y, w, h)
print('largest red contour area:', round(cv2.contourArea(contour), 1))
print('result: lesson28-camera-mask.png')
```

在照片與程式所在目錄執行：

```bash
python3 第28課-相機照片偵測.py
```

本次在 RP5 上的實際輸出如下；座標和面積會隨拍攝位置、曝光與光線改變：

```text
input camera image: (1080, 1920, 3)
large red regions: 1
largest red box (x, y, w, h): 784 283 150 157
largest red contour area: 14982.0
result: lesson28-camera-mask.png
```

![RP5 相機拍攝色塊後的紅色偵測與遮罩](./圖檔/lesson28-camera-mask.png)

左圖是相機照片中目標周圍的裁切圖，綠框為偵測範圍；右圖是對應的二值遮罩。畫面經裁切以去除螢幕外的環境，紅色目標仍是相機實拍。

## 與原文章的差異

- 原文以相機追蹤顏色；本版先驗證固定合成圖的遮罩與像素數，未測即時追蹤。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
- 追加 RP5 實拍螢幕色塊的單張照片偵測；尚未完成原文的即時追蹤。
