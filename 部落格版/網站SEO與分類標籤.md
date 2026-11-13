# 網站 SEO 與分類標籤

digithouse.net 上部落格版文章的 SEO、分類（Categories）與標籤（Tags）設定。完整規則寫在平台 repo 的 `.agent/skills/payload-seo-social/SKILL.md`（Blog posts: SEO, categories and tags）。

## 共同規則

- slug：英文小寫、連字號、`ba5077-` 前綴加 3～6 個搜尋關鍵字，不用流水號；全部 57 篇的 slug 定在[新舊課號對照表](./新舊課號對照表.md)。
- 分類：NCU（`course-ba5077`）、技術文章（`digithouse-technical-articles`）。
- 基本標籤：AIoT（`digithouse-aiot`）、AIoT產品發展實作（`digithouse-aiot-product-development`）、RaspberryPI（`digithouse-raspberry-pi`）；再依內容加主題標籤。
- **不要**加 BA5077（`digithouse-ba5077`）：BA5077 課程頁會列出所有帶這個標籤的文章，加了就會混進原本的課程列表。
- SEO 標題：搜尋關鍵字放前面，結尾加「 | DigitHouse」；SEO 描述約 80～120 字，只寫頁面上真的有的內容，尚未實測的事不寫成已驗證。
- SEO 圖片：從該篇已上傳的圖中挑最有代表性的一張；沒有合適的圖就留空。
- 已發布的文章改 SEO 時，先存成草稿版本，再由使用者按「發佈」。

## 各篇設定

00～07 於 2026-11-12 寫入草稿版本；08～15 於 2026-11-12 建立草稿時一併填入。16～22 於 2026-11-13 寫好設定，尚未建立網站草稿。

| 篇 | slug | 主題標籤 | SEO 標題 | SEO 描述 | SEO 圖片 |
| --- | --- | --- | --- | --- | --- |
| 00 | `ba5077-raspberry-pi-os-bookworm-vs-trixie` | Python、OpenCV、Picamera2 | Raspberry Pi OS Bookworm 與 Trixie 差異：教材升級導讀 | DigitHouse | Raspberry Pi OS 從 Bookworm（Debian 12）到 Trixie（Debian 13）改了什麼？整理 Python 3.13、wayvnc、OpenCV、MediaPipe、虛擬環境與相機的差異，並附官方與實測出處。 | — |
| 01 | `ba5077-aiot-course-roadmap` | AI | BA5077 AIoT 產品發展實作課程地圖：從問題到原型 | DigitHouse | BA5077 AIoT 產品發展實作課程導覽：認識 AIoT 的資料流程與 56 篇學習路線，再用產品規劃表把生活問題變成可以驗證的 Raspberry Pi 原型題目。 | — |
| 02 | `ba5077-raspberry-pi-5-hardware-check` | Linux | 認識 Raspberry Pi 5：用指令查型號、記憶體與系統版本 | DigitHouse | 零基礎認識 Raspberry Pi 5：CPU、RAM、儲存與作業系統各自負責什麼，用七行終端機指令查出型號、架構、記憶體與 Raspberry Pi OS Trixie 版本，附實測輸出與截圖。 | `lesson02-trixie-system.png` |
| 03 | `ba5077-raspberry-pi-network-linux-basics` | Linux | Raspberry Pi 網路與 Linux 入門：介面狀態與名稱解析 | DigitHouse | 網路連不上怎麼查？在 Raspberry Pi 上檢查網路介面狀態與 localhost 名稱解析，並認識 Linux 核心、發行版與目錄結構，附 Trixie 實測輸出與截圖。 | `lesson03-trixie-network.png` |
| 04 | `ba5077-install-raspberry-pi-os-imager` | Linux | Raspberry Pi OS 安裝教學：Imager 燒錄與第一次開機 | DigitHouse | 用 Raspberry Pi Imager 把 Raspberry Pi OS 燒錄到 microSD：選機型與系統、設定帳號與 SSH、第一次開機後的檢查項目，以及按下寫入前一定要確認的事。 | — |
| 05 | `ba5077-raspberry-pi-ssh-apache` | Linux、Python | Raspberry Pi SSH 與 Apache 網頁伺服器入門教學 | DigitHouse | 確認 Raspberry Pi 的 SSH 服務，用 Python 理解 HTTP 請求與回應，再用 APT 安裝 Apache 2.4，讓另一台電腦打開 Pi 的網頁，附實測輸出與排錯表。 | `lesson04-trixie-cross-http-20261110.jpg` |
| 06 | `ba5077-raspberry-pi-wayvnc-remote-desktop` | — | Raspberry Pi 5 遠端桌面：wayvnc 與 VNC Viewer 設定 | DigitHouse | 在 Raspberry Pi 5（Trixie）確認 wayvnc 服務，用 Windows 的 VNC Viewer 遠端操作桌面；另介紹不需要 IP 的 Raspberry Pi Connect 桌面分享，附排錯表。 | `lesson10-connect-screen-20261110.jpg` |
| 07 | `ba5077-mobaxterm-x11-forwarding` | Linux | MobaXterm X11 轉發：把 Raspberry Pi 視窗顯示在 Windows | DigitHouse | 用 MobaXterm 的 X11 轉發，把 Raspberry Pi 上的程式視窗顯示在 Windows；說明 SSH、X11 與 VNC 的差別，並示範 Raspberry Pi Connect 遠端終端機。 | `lesson06-trixie-connect-status.png` |
| 08 | `ba5077-linux-terminal-commands` | Linux | Raspberry Pi 終端機入門：常用 UNIX 指令實作 | DigitHouse | 在 Raspberry Pi 的練習資料夾裡實際操作 mkdir、mv、chmod、grep、tar、df 等 UNIX 指令，看懂 sudo、apt、systemctl，並學會哪些指令會覆寫或刪除資料。 | `lesson09-trixie-move-permission-20261110.jpg` |
| 09 | `ba5077-nano-vi-text-editor` | Linux | nano 與 vi 編輯器入門：在終端機修改文字檔 | DigitHouse | 在 Raspberry Pi 終端機用 nano 與 vi 各寫一行文字、存檔、離開並讀回確認，搞懂 vi 的命令模式與插入模式，附兩個編輯器的操作比較表。 | `lesson11-output.png` |
| 10 | `ba5077-qiv-image-viewer-apt` | Linux | Raspberry Pi 安裝 qiv：用 apt 安裝與終端機看圖 | DigitHouse | 在 Raspberry Pi OS Trixie 用 sudo apt install 從零安裝 qiv 3.0.1，看懂安裝訊息、用三種方法確認，再從桌面終端機一行指令開啟圖片，附排錯表。 | `lesson08-qiv-301-window-20261111.png` |
| 11 | `ba5077-thonny-opencv-virtual-environment` | Python、OpenCV | Raspberry Pi 5 安裝 OpenCV：Thonny 虛擬環境教學 | DigitHouse | 在 Raspberry Pi 5（Trixie、Python 3.13）用 Thonny 建立虛擬環境，以固定版本安裝 OpenCV 4.12，排除 pkg_resources 錯誤，並畫圖、存檔、開視窗。 | `lesson14-trixie-demo.png` |
| 12 | `ba5077-first-python-thonny-opencv` | Python、OpenCV | Thonny 入門：第一支 Python 程式與 OpenCV 影像陣列 | DigitHouse | 認識 Thonny 的編輯區、Shell 與直譯器，用 sys.executable 找出正在執行的 Python，再用 OpenCV 建立一張圖，讀懂影像的形狀與 BGR 顏色順序。 | `lesson12-trixie-thonny-20261110.jpg` |
| 13 | `ba5077-raspberry-pi-camera-rpicam-hello` | Camera、Libcamera | Raspberry Pi 5 相機模組連接與 rpicam-hello 偵測 | DigitHouse | Raspberry Pi 5 相機排線要注意什麼？用 rpicam-hello --list-cameras 確認系統偵測到相機，再用 Picamera2 取得一張影格，並說明 libcamera 指令的改名。 | `lesson18-camera-board.png` |
| 14 | `ba5077-picamera2-capture-photo` | Camera、Picamera2、Python | Picamera2 拍照教學：用 Python 拍照並存成 JPEG | DigitHouse | 用不到十五行的 Picamera2 程式在 Raspberry Pi 拍照並存成 JPEG，搞懂解析度、釋放相機與工作目錄，並用 os.getcwd() 找到照片存放的位置。 | `lesson18-camera-board.png` |
| 15 | `ba5077-picamera2-opencv-frame` | Picamera2、OpenCV、Python | Picamera2 加 OpenCV：把相機影格轉成灰階陣列 | DigitHouse | 建立同時能用 Picamera2 與 OpenCV 的 Thonny 環境，用 capture_array 取得 Raspberry Pi 相機影格、cvtColor 轉成灰階，並讀懂影像陣列的形狀。 | `thonny2-camera-env-test.png` |
| 16 | `ba5077-rpicam-vid-picamera2-capture` | Camera、Libcamera、Picamera2、OpenCV | Raspberry Pi 5 相機錄影：rpicam-vid 與 Picamera2 兩種取像 | DigitHouse | 在 Raspberry Pi 5 用 rpicam-vid 錄 5 秒影片、以 ffprobe 與 OpenCV 檢查 142 張影格，說明 CSI 相機為何不能用 VideoCapture(0)，並用 Picamera2 開限時預覽。 | `lesson13-thonny-readback-20261111.png` |
| 17 | `ba5077-opencv-live-preview-recording` | Camera、Picamera2、OpenCV、Python | Picamera2 即時預覽與錄影：OpenCV VideoWriter 教學 | DigitHouse | 一支 Python 程式同時開相機預覽、做灰階與邊緣處理、用 VideoWriter 錄成 MJPG 影片再讀回；在 Raspberry Pi 5 實測 20 秒 202 張、每秒 10.1 張，附排錯表。 | `lesson16-thonny-preview-20261111.png` |
| 18 | `ba5077-opencv-grayscale-image` | OpenCV、Python | OpenCV 讀取灰階圖片：imread 與 IMREAD_GRAYSCALE 入門 | DigitHouse | 用 OpenCV 的 imread 把圖片讀成灰階、存檔並開視窗顯示，讓程式到自己所在的資料夾找圖，讀懂灰階影像只有高與寬的形狀，並比較彩色與灰階留下了什麼。 | `lesson17-trixie-thonny-window-20261110.jpg` |
| 19 | `ba5077-opencv-draw-shapes` | OpenCV、Python | OpenCV 繪圖教學：直線、矩形、圓、橢圓與多邊形 | DigitHouse | 在 OpenCV 畫布上畫直線、矩形、圓、橢圓與多邊形，搞懂左上角原點、x 向右 y 向下的座標與 BGR 顏色順序，並在 Raspberry Pi 的 Thonny 存檔、開視窗。 | `lesson19-thonny-result.png` |
| 20 | `ba5077-opencv-fonts-text` | OpenCV、Python | OpenCV putText 教學：八種 Hershey 字型比較 | DigitHouse | 用 OpenCV 的 putText 把同一句英文以八種 Hershey 字型寫上畫布，看懂基準線座標、縮放與線寬，解決視窗超出畫面的問題，並說明為什麼不要假設它能寫中文。 | `lesson20-thonny-result.png` |
| 21 | `ba5077-opencv-shapes-text-practice` | OpenCV、Python | OpenCV 圖形加文字：矩形、圓與 putText 綜合練習 | DigitHouse | 在同一張 OpenCV 畫布上畫矩形、圓形並寫上文字，理解繪製先後順序與文字對比，並在 Raspberry Pi 的 Thonny 存檔、開視窗確認結果，附練習題。 | `lesson21-drawing.png` |
| 22 | `ba5077-opencv-roi` | Camera、Picamera2、OpenCV、Python | OpenCV ROI 教學：用 NumPy 切片處理即時相機畫面 | DigitHouse | 用 NumPy 切片取出影像的感興趣區域（ROI），搞懂先 y 後 x、上界不含與 copy 的差別，再把固定 ROI 放進 Raspberry Pi 相機的即時畫面，並說明固定座標的缺點。 | `lesson24-trixie-live-roi-20261110.png` |
