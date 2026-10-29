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

## 背景與核心概念

### 從特徵點到遊戲規則

手勢遊戲需要先取得手部影像，再推估關鍵點、判斷手指狀態，最後依規則計算勝負。用布林值測試規則只能驗證其中一段，不能證明相機辨識整個遊戲已完成。

### 思考、練習與後續應用

列出剪刀、石頭、布判斷規則可能忽略哪些手指或手部角度；哪些情況應回傳未知而非硬判？

可擴充為互動遊戲，還要驗證誤判、等待時間、平手及無法辨識時的提示。

進一步閱讀：[相關官方文件](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)。請以下方實測狀態為準；尚未實作或測試的情境不能視為已通過。

## 概念流程圖

```mermaid
flowchart LR
    A["相機影格"]
    B["手部特徵點"]
    C["手指狀態判斷"]
    D["剪刀石頭布規則"]
    A --> B --> C --> D
```

此圖用於說明文章的概念或完整目標流程，**不是操作截圖，也不代表每個步驟都已實測**；本機實測範圍請看文章中的標示。

## 與原文章的差異

- 原文包含相機手勢偵測；本版先把分類邏輯抽出並以固定資料測試，影像到手指狀態的整合仍待實作。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 加入教學流程示意；圖中的完整目標流程不代表已逐步實測。
