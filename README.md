# BA5077 教材與 Raspberry Pi 5 相容性查核（進行中）

最後更新：2026-10-29。課程目錄顯示 56 篇；本文件目前僅記錄下列已辨識的問題，尚未完成逐篇審核，不能據此判定全部教材可用。

## 測試基準

- Raspberry Pi 5 Model B Rev 1.0，8 GB RAM，64 位元 ARM。
- 裝置回報 Debian GNU/Linux 12（Bookworm）；尚未確認是否為 Raspberry Pi OS 映像，或其軟體來源。
- microSD 約 32 GB；實際剩餘空間、相機和 AI HAT 是否安裝均未確認。
- 網路線與 SSH 連線曾成功；以下安裝與範例尚未在這台機器實際執行。

## 補充 8｜PiCamera2 + TensorFlow Lite (MobileNetV1) + 即時影像分類 + 顯示分類文字 的 完整教學

[原文](https://digithouse.net/blog/supplement-08-tflite-mobilenet-realtime-classification?locale=en)

**狀態：需調整，未實機測試。** 原文使用系統環境直接執行 `pip install tflite-runtime`。Raspberry Pi OS Bookworm 起系統 Python 受 externally-managed 限制，應使用虛擬環境，且須確認所選 runtime 有對應 Python 版本與 ARM64 的套件。PiCamera2 和 libcamera 的系統套件在虛擬環境中的可見性也須確認。勿以強制覆蓋系統 Python 作為一般解法。

建議先在實機檢查 Python 版本、套件來源與相機；再選定受支援的 LiteRT/TensorFlow runtime，確認模型、標籤和量化參數對應，逐步驗證推論結果。尚未確認模型及標籤下載連結目前是否有效。

來源：[Raspberry Pi Python 環境](https://www.raspberrypi.com/documentation/computers/os.html)、[Picamera2 手冊](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)。

## 第 27 課｜使用 OpenCV 比較 SIFT、SURF 與 ORB 特徵檢測

[原文](https://digithouse.net/blog/ba5077-lesson-27-opencv-feature-detectors?locale=ja)

**狀態：需調整，未實機測試。** 原範例使用 `cv2.xfeatures2d.SIFT_create()` 和 `cv2.xfeatures2d.SURF_create()`。新版 OpenCV 可先檢查 `cv2.SIFT_create()`；SURF 需要含 contrib 且啟用 nonfree 的建置，一般套件不能假設已具備。可先以 SIFT 與 ORB 完成比較；若教學一定要使用 SURF，須另行確認建置及使用條件。

檢查方式：

```bash
python3 -c "import cv2; print(cv2.__version__); print('SIFT:', hasattr(cv2, 'SIFT_create')); print('xfeatures2d:', hasattr(cv2, 'xfeatures2d'))"
```

以上只能檢查名稱是否存在，並不證明 SURF 可實際執行。[OpenCV 建置選項](https://docs.opencv.org/4.10.0/db/d05/tutorial_config_reference.html)。

## 相機相關文章的共同更新

**狀態：需逐篇檢查，未實機測試。** Raspberry Pi OS Bookworm 起官方相機範例程式使用 `rpicam-*` 名稱；Picamera2 的安裝與相機支援須依實際作業系統與軟體來源確認。更換指令名稱不代表文章的相機程式已通過測試。[官方相機文件](https://www.raspberrypi.com/documentation/accessories/camera-software.html)。

## AI HAT+ 2

官方 AI HAT+ 2 硬體支援 Raspberry Pi 5；目前官方 AI 軟體指南指定 64 位元 Raspberry Pi OS Trixie。此機目前回報 Bookworm，不能假設已符合該指南。另行安裝至備用 microSD 可保留現有系統。[官方 AI 軟體指南](https://www.raspberrypi.com/documentation/computers/ai.html)。

## 待完成

1. 確認 56 篇的完整標題與實際內容，逐篇核對安裝命令、模型下載與範例。
2. 確認實際作業系統來源、Python 版本、可用空間及外接相機。
3. 對實機測試分別記錄已通過、需調整、未測試或不適用；包含原始指令、更新方案與來源。
