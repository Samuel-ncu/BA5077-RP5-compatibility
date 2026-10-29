# 第 7 課｜連接 Raspberry Pi 5 相機模組

[原始文章](https://liusming.pixnet.net/blog/posts/14222855742) · 更新日期：2026-10-29

## 學習目標

認識 Raspberry Pi 5 相機連接方式，並確認作業系統是否偵測相機。操作排線前，請先關機並拔掉電源；確認排線種類、方向及接頭鎖扣，避免強行插入。

## 查詢相機

開機後在 RP5 終端機執行：

```bash
rpicam-hello --list-cameras
```

本次實際輸出節錄：

```text
Available cameras
-----------------
0 : imx708_wide [4608x2592 10-bit RGGB]
```

其他可用影像模式會接在後面；型號及解析度依相機而異。若沒有列出相機，先關機斷電，檢查排線、接頭及相機相容性。

## 測試 Picamera2

本次使用 Picamera2 擷取一張 320 × 240 影格，得到以下實際結果：

```text
Picamera2 capture: (240, 320, 3) uint8
```

這代表已擷取一張三通道影像；它沒有驗證每種解析度、錄影或桌面預覽。

## 與原文章的差異

- Bookworm 的官方相機應用程式名稱改為 `rpicam-*`；使用 `rpicam-hello` 查詢相機。
- 加入本機實際相機與影格結果，不再要求先假定相機型號。
- 實際接線與安裝畫面尚未重新拍攝。

參考：[Raspberry Pi 官方相機軟體文件](https://www.raspberrypi.com/documentation/accessories/camera-software.html)。
