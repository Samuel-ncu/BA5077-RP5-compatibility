# 第 5 課｜Raspberry Pi OS 安裝完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222880489) · 更新日期：2026-10-29

## 學習目標

了解如何使用 Raspberry Pi Imager，為 Raspberry Pi 5 準備 Raspberry Pi OS。這台 RP5 已有可用的 Bookworm 系統；**本次沒有重新燒錄或驗證新安裝流程**。

## 準備工作

需要一台可執行 Raspberry Pi Imager 的電腦、讀卡機，以及準備作為新系統的 microSD。燒錄會清除選定裝置的內容。若要保留目前 RP5 的系統與資料，請使用另外一張卡，並在操作前備份重要資料。

## 安裝步驟

1. 從 [Raspberry Pi 官方下載頁面](https://www.raspberrypi.com/software/) 取得並開啟 Raspberry Pi Imager。
2. 選擇 Raspberry Pi 5 和需要的 64 位元作業系統。若教學需要圖形介面，選擇含桌面的版本。
3. 選擇**備用** microSD，核對容量與裝置名稱；不要選到現有系統碟或其他重要磁碟。
4. 依 Imager 畫面設定帳號、時區、鍵盤、網路及 SSH。帳號與密碼應自行建立，切勿將密碼寫進公開教材。
5. 再次確認目標裝置後開始寫入並等待驗證。完成後安全退出卡片，插入已斷電的 RP5，再接上電源。
6. 首次啟動後，以第二課的方法確認型號、架構及系統版本，再按實際需求安裝課程套件。

## 版本選擇

目前這台機器使用 Bookworm，已用於既有的相機、OpenCV 和部分 AI 測試。若日後使用官方 AI HAT+ 2，請先確認 [官方 AI 軟體文件](https://www.raspberrypi.com/documentation/computers/ai.html)對 Raspberry Pi OS 版本的要求；本次沒有在現有卡上升級或測試 HAT。

## 測試與畫面狀態

- 已確認現有 RP5 可以開機、SSH 登入並執行 Python。
- 未執行 Imager 寫卡、首次開機及系統升級；沒有把其他機器的輸出冒充為本次結果。
- 尚未補拍安裝畫面。

## 與原文章的差異

- 以目前的 Raspberry Pi Imager 流程描述操作，並明確標出燒錄會清除目標裝置。
- 加入本次使用 Bookworm、AI HAT+ 2 版本選擇，以及備用卡與備份的考量。
- 原文章流程未在本次重新燒錄實測，請以 Imager 當前畫面為準。
