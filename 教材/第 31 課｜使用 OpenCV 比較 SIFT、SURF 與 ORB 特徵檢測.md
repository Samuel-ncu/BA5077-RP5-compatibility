# 第 31 課｜使用 OpenCV 比較 SIFT、SURF 與 ORB 特徵檢測

[原始文章](https://liusming.pixnet.net/blog/posts/14222886546) · 更新日期：2026-10-29

## 學習目標

認識 SIFT、SURF、ORB 並確認本機能建立三種偵測器。

## 事前準備

需要相容的 OpenCV；SURF 依賴有啟用 nonfree 的建置。

本教學程式使用合成資料，沒有把私人相機影像上傳公開 repo；請在自己的練習目錄操作。

## 程式與執行

將下列程式存為 `第31課.py`，或使用[已測試的範例程式](./範例程式/第31課.py)。

```python
import cv2
sift = cv2.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create()
print('SIFT created', bool(sift))
print('SURF created', bool(surf))
print('ORB created', bool(orb))
```

在該檔案所在目錄執行 `python3 第31課.py`。

## 本機實際輸出

```text
SIFT created True
SURF created True
ORB created True
```

本機三種物件均可建立；不代表所有 Raspberry Pi OS 的 OpenCV 都包含 SURF，也未測試原文圖片的特徵數。

## 與原文章的差異

- 新版 SIFT 改用 `cv2.SIFT_create()`；本次環境的 SURF 實測可建立，其他環境需自行確認。
- 以上是本機實際合成資料輸出；不同版本可能產生不同數值。
- 尚未保存操作畫面截圖。
