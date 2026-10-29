# 補充 6｜🧠 RP5 + CVZone + MediaPipe + PiCamera2 雙手偵測與距離計算教學

[原始文章](https://liusming.pixnet.net/blog/posts/14223033954) · 更新日期：2026-10-29

## 學習目標

確認 CVZone 的 HandDetector 在目前測試環境能否匯入。

## 事前準備

本次在 MediaPipe 測試環境以 --no-deps 安裝 CVZone 2.0.0。

MediaPipe 的已測試安裝方式請看[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#5-mediapipe-手勢與-face-mesh)。不同專案請使用獨立環境。

## 程式與執行

將以下程式存為 `補充6.py`，或使用[已測試的範例程式](./範例程式/補充6.py)。在檔案所在目錄執行 `python3 補充6.py`。

```python
from cvzone.HandTrackingModule import HandDetector
print('HandDetector import', HandDetector is not None)
```

## 本機實際輸出

```text
HandDetector import True
```

匯入成功不等於可用：pip check 回報缺少 opencv-python，因環境安裝的是 opencv-contrib-python。雙手追蹤與距離計算未測試。

## 與原文章的差異

- 原文直接安裝 CVZone；本次保留依賴衝突的真實結果，沒有宣稱可直接使用。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
