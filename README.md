# BA5077 教材與 Raspberry Pi 5 相容性查核

[重製教材目錄（逐篇完成中）](./教材/README.md)

56 篇均已補充初學者背景、思考練習、後續應用及圖例；第 18、28、29、30 課有 RP5 相機實拍後的結果圖。其他圖例可能是概念圖或合成測試輸出，並非安裝或操作截圖；逐篇完整實測仍在進行。

[依文章標題查看 56 篇教材查核與更新後的安裝指引](./各篇教材查核.md)

[逐步安裝教學與本機實測輸出](./安裝操作與實測紀錄.md)

查核基準是 Raspberry Pi 5、8 GB RAM、Raspberry Pi OS Bookworm 64-bit、Python 3.11，更新日期 2026-10-29。文章清單根據課程來源盤點；網站當時載入逾時，目錄順序與線上版本仍待覆核。

實機已驗證相機、OpenCV 基本功能、LiteRT MobileNetV1 基本推論、MediaPipe Hands / Face Mesh 的單張相機影格處理、Tesseract 合成英文辨識，以及 YOLOv8n CPU 單張影格推論。每篇完整範例、圖形介面、模型正確率和所有安裝流程並未全部測試；詳情與限制請看逐篇文件。

已發現需調整的項目包括 Bookworm 的 Python 虛擬環境、舊版相機指令、LiteRT 與 NumPy 相依衝突、YOLO 文章的 CUDA 安裝指令，以及個別程式的非標準空白字元。

AI HAT+ 2 的官方軟體指引目前指定 64-bit Raspberry Pi OS Trixie；這台機器使用 Bookworm。請使用備用儲存裝置測試系統升級與 Hailo，並先保留既有資料。[官方 AI 文件](https://www.raspberrypi.com/documentation/computers/ai.html)
