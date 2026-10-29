# 第 10 課｜Raspberry Pi 5 安裝與設定 VNC Viewer

[原始文章](https://liusming.pixnet.net/blog/posts/14222855754) · 更新日期：2026-10-29

## 學習目標

使用電腦上的 VNC Viewer 連接 RP5 的圖形桌面。Viewer 是觀看端，RP5 必須有相容的 VNC 伺服器；連線方式與系統使用 X11 或 Wayland 有關。

## 確認伺服器

本次 RP5 使用 X11，並檢查現有 VNC 服務：

```bash
systemctl is-active vncserver-x11-serviced
```

本機實際輸出：

```text
active
```

這表示本機使用的服務已啟動；其他 Raspberry Pi OS 版本或 Wayland 桌面可能使用不同伺服器。

## 連線流程

1. 確保電腦可以連到 RP5，並查明 RP5 的位址。
2. 在電腦開啟 VNC Viewer，輸入 RP5 的位址。
3. 首次連線若要求確認伺服器身分，先核對指紋；輸入認證資料時由使用者自行操作，不要把密碼放進教材或聊天。
4. 連線後確認視窗顯示的是 RP5 桌面。本次已由使用者完成登入並看到桌面。

## 與原文章的差異

- 補充 X11、Wayland 與 VNC 伺服器的差異，並保留本機服務的實測輸出。
- 加入首次連線的身分確認；本次沒有把帳號密碼放入教材。
- 已實際連上桌面，但尚未保存可公開的操作截圖。

參考：[Raspberry Pi 官方遠端存取文件](https://www.raspberrypi.com/documentation/computers/remote-access.html)。
