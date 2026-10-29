# 第 2 課｜認識 Raspberry Pi 與 Raspberry Pi OS

[原始文章](https://liusming.pixnet.net/blog/posts/14222880459) · 更新日期：2026-10-29

## 學習目標

認識 Raspberry Pi 單板電腦和 Raspberry Pi OS，並能在自己的機器上確認型號、架構、核心數及 Python 版本。Raspberry Pi OS 是針對 Raspberry Pi 調整的 Linux 系統；本次機器使用的版本以 Debian 12 Bookworm 為基礎。

## 需要準備什麼

已啟動的 Raspberry Pi、終端機，以及可登入的帳號。可以在 RP5 接的螢幕操作，也可以使用已建立的 SSH 連線。

## 實作：查詢硬體與系統

在終端機執行：

```bash
printf 'model: '; tr -d '\000' < /proc/device-tree/model
printf '\narchitecture: '; uname -m
printf 'cores: '; getconf _NPROCESSORS_ONLN
python3 --version
```

本次實際輸出：

```text
model: Raspberry Pi 5 Model B Rev 1.0
architecture: aarch64
cores: 4
Python 3.11.2
```

`aarch64` 表示目前執行的是 64 位元 ARM 環境。四個核心和 Python 版本不代表所有軟體都自動相容：仍須檢查作業系統版本與 ARM64 套件。

記憶體可用 `free -h` 查看；這台機器的總記憶體曾顯示約 7.9 GiB，對應 8 GB 機型。可用量隨當時執行的程式而變。

## 檢查與排除

- 如果找不到 `/proc/device-tree/model`，先確認是否真的在 Raspberry Pi 上執行，而不是在 Windows PowerShell。
- `Python 3.11.2` 是本機結果；其他系統版本可能顯示不同數字。
- 系統可用記憶體略低於標示容量屬常見情況；記憶體不是 microSD 儲存容量。

## 與原文章的差異

- 補上這台 RP5 的實際命令與輸出；原文的機型與作業系統介紹仍適用作背景知識。
- 將硬體架構與軟體相容性分開說明，避免把 ARM64 視為所有套件均可安裝。
- 尚未補拍本課畫面。
