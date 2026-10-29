# 第 14 課｜在 Raspberry Pi 5 安裝 OpenCV

[原始文章](https://liusming.pixnet.net/blog/posts/14222877021) · 更新日期：2026-10-29

## 學習目標

確認目前 Python 執行環境載入的 OpenCV 版本與實際模組位置。

## 事前準備

使用 RP5 已存在的系統 Python 與 OpenCV。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第14課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第14課.py)。

```python
import cv2
print("opencv", cv2.__version__)
print("path", cv2.__file__)
```

在該檔案所在的目錄執行 `python3 第14課.py`。

## 本機實際輸出

```text
opencv 4.10.0-dev
path /usr/lib/python3/dist-packages/cv2/__init__.py
```

路徑顯示此 Python 實際載入的套件；不同系統會不同。此機套件管理器的版本紀錄與 Python 匯入版本不同，不可只憑其中一個數字判斷。

## 與原文章的差異

- 原文包含多種安裝方式；本版先驗證既有安裝，避免同時安裝多個 OpenCV 變體。若缺少套件，另參考共用安裝紀錄。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 尚未補拍操作畫面；圖檔（若有）是程式產生的結果，不冒充螢幕截圖。
