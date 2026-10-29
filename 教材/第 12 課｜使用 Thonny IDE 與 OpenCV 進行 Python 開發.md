# 第 12 課｜使用 Thonny IDE 與 OpenCV 進行 Python 開發

[原始文章](https://liusming.pixnet.net/blog/posts/14222870088) · 更新日期：2026-10-29

## 學習目標

認識 Thonny 與 Python 的 OpenCV 模組，並先檢查本機程式是否存在。Thonny 的 Python 解譯器可能與終端機使用的解譯器不同；安裝模組後找不到時，先核對執行環境。

## 實測：查詢程式與版本

```bash
command -v thonny
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
```

本機實際輸出：

```text
/usr/bin/thonny
OpenCV: 4.10.0-dev
```

此結果證明終端機的系統 Python 可以匯入 OpenCV，不代表已驗證 Thonny 所選的解譯器或其圖形顯示。

## 後續練習

在 RP5 桌面啟動 Thonny，確認所選 Python 解譯器，建立自己的練習程式並檢查輸出。需要顯示圖片時，還要確認圖形桌面可用；經 SSH 執行不一定能開啟視窗。

Bookworm 不建議直接將 pip 套件裝入系統 Python，也不應同時安裝互相覆蓋的 OpenCV 變體；虛擬環境及實測紀錄見[安裝操作與實測紀錄](../安裝操作與實測紀錄.md)。

## 與原文章的差異

- 先檢查現有 Thonny 與 OpenCV，並區分終端機 Python 與 Thonny 解譯器。
- 原文同時安裝一般版及 headless OpenCV 的做法不作為新版建議。
- 尚未重新操作 Thonny 視窗與擷取畫面。
