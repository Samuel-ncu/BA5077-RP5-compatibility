# 補充 5｜✊🤚✌️ Raspberry Pi 5 + PiCamera2 + MediaPipe 手勢辨識遊戲：「剪刀、石頭、布」

[原始文章](https://liusming.pixnet.net/blog/posts/14223033945) · 更新日期：2026-10-29

## 學習目標

先驗證剪刀、石頭、布的簡化判斷規則。

## 事前準備

需要 Python；輸入為四根手指的布林狀態。

MediaPipe 的已測試安裝方式請看[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#5-mediapipe-手勢與-face-mesh)。不同專案請使用獨立環境。

## 程式與執行

將以下程式存為 `補充5.py`，或使用[已測試的範例程式](./範例程式/補充5.py)。在檔案所在目錄執行 `python3 補充5.py`。

```python
def classify(index_up, middle_up, ring_up, little_up):
    if not any((index_up, middle_up, ring_up, little_up)):
        return 'rock'
    if index_up and middle_up and not ring_up and not little_up:
        return 'scissors'
    if all((index_up, middle_up, ring_up, little_up)):
        return 'paper'
    return 'unknown'

print('rock test', classify(False, False, False, False))
print('scissors test', classify(True, True, False, False))
print('paper test', classify(True, True, True, True))
```

## 本機實際輸出

```text
rock test rock
scissors test scissors
paper test paper
```

這只測試分類規則；程式沒有使用相機，也沒有從 MediaPipe 關鍵點判斷手指彎曲，不能視為完成互動遊戲。

## 與原文章的差異

- 原文包含相機手勢偵測；本版先把分類邏輯抽出並以固定資料測試，影像到手指狀態的整合仍待實作。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
