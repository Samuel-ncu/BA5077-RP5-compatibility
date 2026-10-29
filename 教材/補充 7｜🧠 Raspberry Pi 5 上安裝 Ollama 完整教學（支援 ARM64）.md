# 補充 7｜🧠 Raspberry Pi 5 上安裝 Ollama 完整教學（支援 ARM64）

[原始文章](https://liusming.pixnet.net/blog/posts/14223038205) · 更新日期：2026-10-29

## 學習目標

確認本機是否已有 Ollama，以及服務是否啟動。

## 事前準備

本次 RP5 已有 Ollama，以下使用系統現有安裝。

## 實際操作

```bash
command -v ollama
ollama --version
systemctl is-active ollama
```

## 本機實際輸出

```text
/usr/local/bin/ollama
ollama version is 0.9.0
active
```

本機已安裝 0.9.0 且服務 active；沒有在此步驟下載模型、更新版本或驗證聊天。模型的空間與記憶體需求因版本而異。

## 與原文章的差異

- 原文以安裝 Ollama 為主；本版先檢查已安裝版本，不重複執行安裝或宣稱已完成模型推論。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
