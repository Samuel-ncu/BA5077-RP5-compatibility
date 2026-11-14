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

00～07 於 2026-11-12 寫入草稿版本；08～15 於 2026-11-12 建立草稿時一併填入。16～22 於 2026-11-14 建立草稿時一併填入。23～28 於 2026-11-14 建立草稿時一併填入。29～34 於 2026-11-14 建立草稿時一併填入。35～40 於 2026-11-14 建立草稿時一併填入。41～45 於 2026-11-14 建立草稿時一併填入。46～50 於 2026-11-14 建立草稿時一併填入。

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
| 23 | `ba5077-opencv-contour-detection` | OpenCV、Python | OpenCV 輪廓偵測教學：findContours 找出物體外框 | DigitHouse | 用 HSV 顏色遮罩把物體和背景分開，再用 OpenCV 的 findContours 找外框、算面積並依位置編號，說明面積門檻與相機照片透視校正的用法，附 Raspberry Pi 實測結果圖。 | `lesson29-trixie-public-contours-20261110.png` |
| 24 | `ba5077-opencv-polygon-approximation` | OpenCV、Python | OpenCV approxPolyDP 教學：把輪廓簡化成多邊形 | DigitHouse | 用 OpenCV 的 approxPolyDP 以周長 2% 的誤差把輪廓簡化成多邊形，從頂點數分辨圓形、矩形與三角形，並說明為什麼圓形會得到 8 個頂點，附相機拍攝圖形的處理結果。 | `lesson34-camera-polygons.png` |
| 25 | `ba5077-opencv-convex-hull-defects` | OpenCV、Python | OpenCV 凸包與凹缺點教學：convexHull 與 convexityDefects | DigitHouse | 用橡皮筋的比喻理解凸包，以 OpenCV 的 convexHull 與 convexityDefects 找出輪廓往內凹最深的位置，把深度換算成像素並用門檻過濾，附合成圖形與相機圖形的結果。 | `lesson35-camera-hull.png` |
| 26 | `ba5077-opencv-hough-circles` | OpenCV、Python | OpenCV 霍夫圓偵測教學：HoughCircles 參數怎麼調 | DigitHouse | 用 OpenCV 的 HoughCircles 在相機拍攝的校正圖上找出圓心與半徑，逐一說明 dp、minDist、param1、param2 與半徑範圍的作用，以及沒找到圓時要處理的 None。 | `shapes-circles.png` |
| 27 | `ba5077-opencv-hsv-color-tracking` | Camera、Picamera2、OpenCV、Python | Picamera2 顏色追蹤教學：OpenCV HSV 紅色偵測與框選 | DigitHouse | 用 Picamera2 連續取像，把影格轉成 HSV、以兩段紅色範圍做遮罩，框出最大的紅色區塊並畫出移動軌跡；Raspberry Pi 5 實測 20 秒 1606 張影格全部偵測到，附排錯表。 | `lesson28-thonny-camera-tracking-20261111.png` |
| 28 | `ba5077-opencv-frame-difference-motion` | OpenCV、Python | OpenCV 影格差分教學：absdiff 找出畫面中的移動 | DigitHouse | 用 OpenCV 的 absdiff 與門檻比較前後兩張影格，找出畫面中改變的像素，說明移動物體為何在舊位置與新位置都留下白色，以及光線與文字變化造成的誤報。 | `lesson26-camera-diff.png` |
| 29 | `ba5077-opencv-mog-background-subtraction` | OpenCV、Python | OpenCV MOG 背景減法教學：讓程式自己學習背景 | DigitHouse | 用 OpenCV 擴充模組的 MOG 背景減法處理 Raspberry Pi 相機短影片，理解背景模型如何隨影格更新、前景遮罩代表什麼，並說明原文程式其實使用 GMG。 | `lesson27-camera-mog.png` |
| 30 | `ba5077-opencv-csrt-object-tracking` | OpenCV、Python | OpenCV CSRT 目標追蹤教學：框住目標一路跟隨 | DigitHouse | 用 OpenCV 的 CSRT 追蹤器在 Raspberry Pi 上追蹤短影片中的圓形，說明 init 與 update、追蹤框的 (x, y, 寬, 高)，以及回報成功不等於框得準。 | `lesson25-trixie-video-csrt-20261110.png` |
| 31 | `ba5077-sift-surf-orb-features` | OpenCV、Python | SIFT、SURF、ORB 特徵點比較：OpenCV 特徵偵測入門 | DigitHouse | 認識特徵點與描述子，在 Raspberry Pi 用 OpenCV 比較 SIFT、SURF、ORB 找到的特徵點，並說明 SURF 因專利在目前環境無法使用、程式如何跳過它。 | `lesson31-features.png` |
| 32 | `ba5077-opencv-feature-matching` | OpenCV、Python | OpenCV 特徵匹配教學：BFMatcher 與雙向檢查 | DigitHouse | 在 Raspberry Pi 用 SIFT 描述子與 BFMatcher 雙向檢查，配對兩張相機校正圖的特徵點，從結果圖找出配錯的連線，說明 L2 距離的用途，以及候選配對數為什麼不等於準確率。 | `lesson31-33-trixie-sift-20261110.png` |
| 33 | `ba5077-opencv-orb-matching` | OpenCV、Python | OpenCV ORB 特徵匹配教學：免授權的二進位描述子 | DigitHouse | 用免授權的 ORB 在 Raspberry Pi 偵測並配對兩張圖的特徵點，理解二進位描述子與 Hamming 距離，並和 SIFT 比較時注意點數上限與重複圖案造成的錯配。 | `lesson31-33-trixie-orb-20261110.png` |
| 34 | `ba5077-opencv-panorama-stitching` | OpenCV、Python | OpenCV 全景拼接教學：Stitcher 把相鄰照片接成全景 | DigitHouse | 在 Raspberry Pi 用 OpenCV 的 Stitcher 把三張相鄰照片拼成全景，看懂 status 0 與 1 的意思，並用重疊太少的照片示範失敗時該補照片而不是調程式。 | `lesson36-thonny-run-20261111.png` |
| 35 | `ba5077-opencv-haar-face-detection` | OpenCV、Python | OpenCV Haar 臉部偵測教學：找出臉在哪裡 | DigitHouse | 在 Raspberry Pi 用 OpenCV 內建的 Haar 級聯分類器找臉，學會用 cv2.data.haarcascades 載入模型、調整 detectMultiScale 參數，並分清楚臉部偵測和臉部辨識的差別。 | `lesson22-trixie-thonny-closed-20261110.jpg` |
| 36 | `ba5077-opencv-lbph-face-recognition` | OpenCV、Python | OpenCV LBPH 臉部辨識教學：偵測、訓練、預測 | DigitHouse | 用 OpenCV 擴充模組的 LBPH 辨識器走一次臉部辨識流程：偵測臉、裁成同樣大小、訓練與預測，並說明距離值的意思，以及為什麼同一張臉自我預測不能代表準確率。 | `lesson23-trixie-lbph-closed-20261110.jpg` |
| 37 | `ba5077-opencv-dnn-face-detection` | OpenCV、Python、AI | OpenCV DNN 人臉偵測教學：用神經網路找臉 | DigitHouse | 在 Raspberry Pi 用 OpenCV DNN 模組載入訓練好的人臉模型，學會 blobFromImage 與 forward，從輸出張量讀出信心分數和方框，並和傳統的 Haar 方法比較。 | `lesson37-thonny-clean.png` |
| 38 | `ba5077-yolov4-tiny-object-detection` | Camera、Picamera2、OpenCV、Python、AI | YOLOv4-tiny 物件偵測教學：OpenCV 單張圖與即時相機 | DigitHouse | 用 OpenCV DNN 載入 YOLOv4-tiny，在 Raspberry Pi 偵測杯子、蘋果、香蕉，學會解碼 YOLO 輸出、用非極大值抑制去掉重疊框，再接上 Picamera2 做即時偵測。 | `lesson38-camera-yolov4.png` |
| 39 | `ba5077-yolov8-coco-setup-training` | Python、AI | YOLOv8 與 COCO 教學：Raspberry Pi 建立 CPU 環境並訓練一回合 | DigitHouse | 在 Raspberry Pi 另建 YOLOv8 專用的 CPU 環境，認識資料集、標註、回合與權重檔，用 COCO8 小資料集訓練一回合再重新載入權重推論，並說明結果為何不能當準確率。 | `lesson39-trixie-coco8-train-20261110.png` |
| 40 | `ba5077-yolov8-image-detection` | OpenCV、Python、AI | YOLOv8 圖片物件偵測教學：predict 與 plot 一次搞定 | DigitHouse | 用預訓練的 YOLOv8n 在 Raspberry Pi 偵測一張物件圖，從 result.boxes 讀出類別和信心值、用 plot 畫框存檔，並和 YOLOv4-tiny 的結果比較，說明信心值不等於正確率。 | `lesson40-trixie-yolov8-20261110.png` |
| 41 | `ba5077-yolov8-video-detection` | OpenCV、Python、AI | YOLOv8 影片物件偵測教學：逐格推論、存檔與播放 | DigitHouse | 在 Raspberry Pi 用 OpenCV 逐格讀取影片、交給 YOLOv8 偵測、寫成新影片並讀回檢查，再於 Thonny 播放成果，說明影片播放 FPS 和實際處理速度為什麼是兩回事。 | `lesson41-trixie-moving-first-last-20261110.png` |
| 42 | `ba5077-yolov8-camera-realtime` | Camera、Picamera2、Python、AI | YOLOv8 接上 Raspberry Pi 相機：Picamera2 即時物件偵測 | DigitHouse | 在 Raspberry Pi 建立同時能用 Picamera2 和 YOLOv8 的環境，先用四張影格確認取像與推論，再開 20 秒即時預覽視窗框出物品，並在程式結束時正確釋放相機。 | `lesson42-trixie-camera-yolo-preview-20261112.jpg` |
| 43 | `ba5077-picamera2-yolov8-realtime` | Camera、Picamera2、Python、AI | Picamera2 加 YOLOv8 即時流程：看懂速度、停止與重開相機 | DigitHouse | 拆解 Raspberry Pi 即時偵測的取像、推論、畫框、顯示四個階段，用實測數字說明短測試為何 FPS 偏低，並練習按 q 停止、重新開啟相機與兩分鐘連續預覽。 | `yolo-120s-thonny.png` |
| 44 | `ba5077-yolov8-image-video-realtime-comparison` | Python、AI | YOLOv8 圖片、影片、即時相機比較：看懂數字與公平比較 | DigitHouse | 把 YOLOv8 在 Raspberry Pi 上處理圖片、影片與即時相機的實測結果放進同一張表，練習分辨播放 FPS 與處理速度，並說明要固定哪些條件才能公平比較準確率。 | `lesson41-trixie-moving-first-last-20261110.png` |
| 45 | `ba5077-flask-yolo-web-stream` | OpenCV、Python、AI | Flask 加 YOLO 教學：把物件偵測畫面變成網頁串流 | DigitHouse | 用 Flask 讓 Raspberry Pi 變成網頁伺服器，把 YOLOv8 偵測後的影格壓成 JPEG 串流給同一區網的瀏覽器觀看，並說明只允許單一觀看者、自動結束與區網安全的注意事項。 | `flask-trixie-lan-browser-20261110.png` |
| 46 | `ba5077-ollama-raspberry-pi` | Linux、AI | Raspberry Pi 5 安裝 Ollama 教學：在本機跑語言模型 | DigitHouse | 在 Raspberry Pi 5 用官方腳本安裝 Ollama，逐項確認程式、服務、API 與模型清單，下載 91 MB 的 SmolLM2 回答問題，再用 Python 透過本機 API 提問，並提醒生成文字要查證。 | `ollama-new-model-thonny.png` |
| 47 | `ba5077-tflite-litert-image-classification` | OpenCV、Python、AI | TensorFlow Lite／LiteRT 入門：Raspberry Pi 圖片分類 | DigitHouse | 在 Raspberry Pi 建立 LiteRT 環境，下載 4 MB 的 MobileNetV1 量化模型，看懂輸入張量的形狀與型別、量化輸出如何換算分數，並說明圖像分類和物件偵測的差別。 | `supp3-trixie-litert-new-classify-20261110.png` |
| 48 | `ba5077-mobilenet-camera-classification` | Camera、Picamera2、OpenCV、Python、AI | Picamera2 加 MobileNetV1：Raspberry Pi 相機即時影像分類 | DigitHouse | 把 LiteRT 的 MobileNetV1 接上 Raspberry Pi 相機，即時在畫面寫出分類結果，練習按 q 停止與重開相機，並用全黑全白的負例說明分類器一定會挑一個答案的限制。 | `supp8-trixie-litert-q-stop-20261110.png` |
| 49 | `ba5077-mediapipe-setup` | Python、AI | MediaPipe 入門：Raspberry Pi 建立環境並找出手與臉的特徵點 | DigitHouse | 說明 MediaPipe 1.x 移除舊 solutions 介面的原因，在 Raspberry Pi 建立 MediaPipe 與 CVZone 環境，從一張圖片找出手部 21 點與臉部 478 點，並用簡單規則判斷手勢。 | `supp-mediapipe-version-thonny.png` |
| 50 | `ba5077-mediapipe-hand-landmarks` | Camera、Picamera2、Python、AI | MediaPipe 手部 21 個特徵點：Raspberry Pi 相機手勢偵測 | DigitHouse | 認識 MediaPipe 手部 21 個特徵點的編號，用 CVZone 從 Raspberry Pi 相機連續找手並統計每張找到幾隻手，說明正例與負例測試的意義，以及拍攝真人前的同意與隱私。 | `cvzone-camera-thonny.png` |
| 51 | `ba5077-mediapipe-face-mesh` | Python、AI | MediaPipe 臉部網格教學：為什麼新版回傳 478 點 | DigitHouse | 說明 MediaPipe 臉部網格是什麼、和臉部辨識的差別，以及新版 Face Landmarker 回傳 478 點的原因：多出左右眼虹膜各 5 點，並提醒程式不要寫死點數、使用臉部資料前要取得同意。 | `supp-mediapipe-result.png` |
| 52 | `ba5077-cvzone-hand-distance` | OpenCV、Python、AI | CVZone 雙手距離計算：用手部特徵點量像素距離 | DigitHouse | 用 CVZone 在 Raspberry Pi 同時找出兩隻手，取出食指指尖座標並以畢氏定理算出像素距離，用全白圖做負例，並說明像素距離為什麼會隨遠近與解析度改變、不能直接當成公分。 | `two-hands-mirror-result.png` |
| 53 | `ba5077-rock-paper-scissors-gesture` | Python、AI | 剪刀石頭布手勢判斷：MediaPipe 手指狀態規則 | DigitHouse | 用 MediaPipe 手部特徵點判斷四根手指是否伸直，整理剪刀、石頭、布的規則與容易失效的情況，說明為什麼不用大拇指，以及完整遊戲還需要倒數、穩定判斷和勝負規則。 | `supp-mediapipe-result-thonny.png` |
| 54 | `ba5077-east-text-detection` | OpenCV、Python、AI | EAST 文字偵測教學：OpenCV DNN 找出圖中的文字框 | DigitHouse | 在 Raspberry Pi 下載 EAST 模型並核對 SHA-256，看懂分數與幾何輸出如何換算成文字框、用非極大值抑制去掉重疊框，並用全黑全白圖做負例，分清文字偵測和文字辨識。 | `supplement9-camera-east.png` |
| 55 | `ba5077-east-camera-text-detection` | Camera、Picamera2、OpenCV、Python、AI | Picamera2 加 EAST：Raspberry Pi 相機文字偵測 | DigitHouse | 用 Picamera2 拍一張影格直接交給 EAST 找文字框，說明相機影格和照片檔在程式裡是同一種陣列，以及把單張改成即時預覽時需要的迴圈、停止方式、計時與有字無字的對照。 | `text-board.png` |
| 56 | `ba5077-east-tesseract-ocr` | Camera、Picamera2、OpenCV、Python、Linux、AI | EAST 加 Tesseract 文字辨識：整張、逐框與相機即時 OCR | DigitHouse | 在 Raspberry Pi 安裝 Tesseract，比較整張圖與 EAST 逐框兩種 OCR 做法，從 OPEN CV 被讀成 OPEN C 看框選的影響，再接上相機連續辨識並試讀繁體中文。 | `east-box-ocr-result.png` |
