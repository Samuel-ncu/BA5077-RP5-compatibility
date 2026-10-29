# 補充 1｜🎯 MediaPipe 介紹：Google 開源的跨平台視覺 AI 框架

[原始文章](https://liusming.pixnet.net/blog/posts/14223033861) · 更新日期：2026-10-29

## 學習目標

認識 MediaPipe 與 Solutions API，並檢查舊教材使用的介面是否能匯入。

## 事前準備

使用已驗證的 MediaPipe 0.10.9 虛擬環境。

MediaPipe 的已測試安裝方式請看[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#5-mediapipe-手勢與-face-mesh)。不同專案請使用獨立環境。

## 程式與執行

將以下程式存為 `補充1.py`，或使用[已測試的範例程式](./範例程式/補充1.py)。在檔案所在目錄執行 `python3 補充1.py`。

```python
import mediapipe as mp
print('MediaPipe', mp.__version__)
print('solutions available', hasattr(mp, 'solutions'))
```

## 本機實際輸出

```text
MediaPipe 0.10.9
solutions available True
```

此測試只檢查版本與介面存在；不等同所有模型均已測試。新版 Tasks API 可能與舊 Solutions 寫法不同。

## 與原文章的差異

- 原文介紹框架與應用；本版加入實際版本與 API 檢查。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
