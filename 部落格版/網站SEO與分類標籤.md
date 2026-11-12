# 網站 SEO 與分類標籤

digithouse.net 上部落格版文章的 SEO、分類（Categories）與標籤（Tags）設定。完整規則寫在平台 repo 的 `.agent/skills/payload-seo-social/SKILL.md`（Blog posts: SEO, categories and tags）。

## 共同規則

- slug：`ba5077-blog-NN`（NN 是新課號）。
- 分類：NCU（`course-ba5077`）、技術文章（`digithouse-technical-articles`）。
- 基本標籤：AIoT（`digithouse-aiot`）、AIoT產品發展實作（`digithouse-aiot-product-development`）、RaspberryPI（`digithouse-raspberry-pi`）；再依內容加主題標籤。
- **不要**加 BA5077（`digithouse-ba5077`）：BA5077 課程頁會列出所有帶這個標籤的文章，加了就會混進原本的課程列表。
- SEO 標題：搜尋關鍵字放前面，結尾加「 | DigitHouse」；SEO 描述約 80～120 字，只寫頁面上真的有的內容，尚未實測的事不寫成已驗證。
- SEO 圖片：從該篇已上傳的圖中挑最有代表性的一張；沒有合適的圖就留空。
- 已發布的文章改 SEO 時，先存成草稿版本，再由使用者按「發佈」。

## 各篇設定（2026-11-12 寫入草稿版本，待按「發佈」）

| 篇 | 主題標籤 | SEO 標題 | SEO 描述 | SEO 圖片 |
| --- | --- | --- | --- | --- |
| 00 | Python、OpenCV、Picamera2 | Raspberry Pi OS Bookworm 與 Trixie 差異：教材升級導讀 | DigitHouse | Raspberry Pi OS 從 Bookworm（Debian 12）到 Trixie（Debian 13）改了什麼？整理 Python 3.13、wayvnc、OpenCV、MediaPipe、虛擬環境與相機的差異，並附官方與實測出處。 | — |
| 01 | AI | BA5077 AIoT 產品發展實作課程地圖：從問題到原型 | DigitHouse | BA5077 AIoT 產品發展實作課程導覽：認識 AIoT 的資料流程與 56 篇學習路線，再用產品規劃表把生活問題變成可以驗證的 Raspberry Pi 原型題目。 | — |
| 02 | Linux | 認識 Raspberry Pi 5：用指令查型號、記憶體與系統版本 | DigitHouse | 零基礎認識 Raspberry Pi 5：CPU、RAM、儲存與作業系統各自負責什麼，用七行終端機指令查出型號、架構、記憶體與 Raspberry Pi OS Trixie 版本，附實測輸出與截圖。 | `lesson02-trixie-system.png` |
| 03 | Linux | Raspberry Pi 網路與 Linux 入門：介面狀態與名稱解析 | DigitHouse | 網路連不上怎麼查？在 Raspberry Pi 上檢查網路介面狀態與 localhost 名稱解析，並認識 Linux 核心、發行版與目錄結構，附 Trixie 實測輸出與截圖。 | `lesson03-trixie-network.png` |
| 04 | Linux | Raspberry Pi OS 安裝教學：Imager 燒錄與第一次開機 | DigitHouse | 用 Raspberry Pi Imager 把 Raspberry Pi OS 燒錄到 microSD：選機型與系統、設定帳號與 SSH、第一次開機後的檢查項目，以及按下寫入前一定要確認的事。 | — |
| 05 | Linux、Python | Raspberry Pi SSH 與 Apache 網頁伺服器入門教學 | DigitHouse | 確認 Raspberry Pi 的 SSH 服務，用 Python 理解 HTTP 請求與回應，再用 APT 安裝 Apache 2.4，讓另一台電腦打開 Pi 的網頁，附實測輸出與排錯表。 | `lesson04-trixie-cross-http-20261110.jpg` |
| 06 | — | Raspberry Pi 5 遠端桌面：wayvnc 與 VNC Viewer 設定 | DigitHouse | 在 Raspberry Pi 5（Trixie）確認 wayvnc 服務，用 Windows 的 VNC Viewer 遠端操作桌面；另介紹不需要 IP 的 Raspberry Pi Connect 桌面分享，附排錯表。 | `lesson10-connect-screen-20261110.jpg` |
| 07 | Linux | MobaXterm X11 轉發：把 Raspberry Pi 視窗顯示在 Windows | DigitHouse | 用 MobaXterm 的 X11 轉發，把 Raspberry Pi 上的程式視窗顯示在 Windows；說明 SSH、X11 與 VNC 的差別，並示範 Raspberry Pi Connect 遠端終端機。 | `lesson06-trixie-connect-status.png` |
