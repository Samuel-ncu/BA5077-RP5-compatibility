# 第 4 課｜網路基礎與作業系統：應用於 Raspberry Pi（下）

[原始文章](https://liusming.pixnet.net/blog/posts/14222880483) · 更新日期：2026-10-29

## 學習目標

認識 Linux、套件管理器與 SSH，並能確認系統是否具備相關工具。套件管理器安裝系統程式；Python 專案則可用獨立虛擬環境管理額外套件。

## 背景：遠端操作與軟體從哪裡來？

當 RP5 沒有接螢幕時，另一台電腦仍可經網路使用 SSH 遠端登入。SSH 提供加密的連線，讓你在 RP5 的終端機執行命令；輸入命令的位置仍是 RP5，不是本機的 Windows。登入前需確認設備、帳號與網路連線正確。

作業系統中的套件管理器協助下載與管理軟體。APT 管理 Debian 系列的系統套件；Python 專案也可能使用虛擬環境管理程式庫。這是兩個不同層次：系統有 `apt`，不代表某個 Python 套件一定已安裝。

```mermaid
flowchart LR
    A[電腦的 SSH 用戶端] --> B[RP5 SSH 服務]
    B --> C[RP5 的 Linux 終端機]
    C --> D[APT 或 Python 程式]
```

上圖是教學流程圖；它不顯示或證明真實的網路連線狀態。

## 實作：確認作業系統與架構

```bash
python3 -c "import platform; print(platform.system()); print(platform.machine())"
command -v apt
```

本機實際輸出：

```text
Linux
aarch64
/usr/bin/apt
```

第一行是核心所屬系統，第二行是處理器架構；`/usr/bin/apt` 表示目前系統找得到 APT。這不代表每個需要的套件均已安裝。

## 實作：確認 SSH

```bash
systemctl is-active ssh
```

本機實際輸出：

```text
active
```

`active` 表示此時 SSH 服務正在執行；遠端登入仍需網路可達、帳號以及適當的認證方式。完成操作後應妥善保護密碼與私鑰。

## 套件與系統更新

APT 的套件來源、版本和網路狀況都會影響安裝結果。先確認要安裝的套件及儲存空間，再依該篇教材操作；不需要為了每一篇文章都全面升級系統。開放 Apache 等服務之前，應確認是否真的需要提供網路存取。

## 練習與後續應用

1. 解釋 `systemctl is-active ssh` 回傳 `active` 所表示的事，以及它不能保證什麼。
2. 說明 `command -v apt` 找得到程式，和某個套件已安裝，為什麼不是同一件事。
3. 設計一個本地網頁顯示感測資料的情境，寫出可能需要的輸入、處理方式與使用者；本次尚未依原文完成網頁伺服器實作。

遠端操作適用於沒有螢幕的感測節點，也讓維護人員能檢查狀態。正式部署還要考量帳號認證、連線範圍、軟體更新與裝置失聯時的處置。[Raspberry Pi 遠端存取文件](https://www.raspberrypi.com/documentation/computers/remote-access.html)可供後續學習。

## 與原文章的差異

- 新增本機實測的 Linux、ARM64、APT 與 SSH 服務檢查。
- 不將全面升級或啟動網頁伺服器視為閱讀文章的必要步驟。
- 尚未補拍本課畫面。
- 補充 SSH、套件管理、連線流程圖及學生練習；原文網頁伺服器情境仍未在本篇完整實測。
