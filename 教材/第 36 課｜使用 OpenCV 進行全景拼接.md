# 第 36 課｜使用 OpenCV 進行全景拼接

[原始文章](https://liusming.pixnet.net/blog/posts/14222886579) · 更新日期：2026-10-29

## 學習目標

驗證 OpenCV 拼接器能否處理兩張有重疊的影像。

## 事前準備

OpenCV、NumPy；程式使用同一合成場景裁出的兩張影像。

## 程式與執行

將下列已在 RP5 執行的程式存為 `第36課.py`，或使用[範例程式](./範例程式/第36課.py)。先確認目前目錄及檔案，避免覆蓋已有資料。

```python
import cv2
import numpy as np

rng = np.random.default_rng(42)
scene = rng.integers(0, 256, (400, 900, 3), dtype=np.uint8)
left = scene[:, :600].copy()
right = scene[:, 300:].copy()
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
status, panorama = stitcher.stitch([left, right])
if panorama is not None and not cv2.imwrite('lesson36-panorama.png', panorama):
    raise RuntimeError('image save failed')
print('stitch status', status)
print('panorama produced', panorama is not None)
```

執行 `python3 第36課.py`。

## 本機實際輸出

```text
stitch status 0
panorama produced True
```

狀態 0 表示這個合成案例成功。真實照片需要足夠重疊、紋理和合適拍攝角度；並未測試原文的照片。

## RP5 實際產生的結果圖

![第 36 課的實際程式輸出](./圖檔/lesson36-panorama.png)

合成隨機影像拼接後的結果；輸入不是相機照片。 圖片由本課程式在 RP5 執行時儲存，是程式輸出，不是操作畫面截圖。

## 背景與核心概念

### 全景影像如何拼接？

相鄰照片若有足夠重疊與可辨識特徵，可以先找出匹配點，再估計影像之間的幾何關係並合成。實際拍攝的視角、重疊比例、光線及移動物體都可能使拼接失敗。

### 思考、練習與後續應用

合成影像拼接成功能證明什麼？如果兩張照片沒有重疊或圖案重複，預期會遇到什麼困難？

全景可用於場景記錄；實際應用需要測試失敗狀況，並處理透視、接縫與個人資訊。

進一步閱讀：[相關官方文件](https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 與原文章的差異

- 原文以實際圖片檔進行拼接；本版先以重疊的合成影像驗證流程。
- 真實場景的準確率、速度和操作畫面尚未完整驗證。
- 尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
