# 第 15 課｜在 Raspberry Pi 5 使用 Libcamera、Picamera2 與 OpenCV

[原始文章](https://liusming.pixnet.net/blog/posts/14222875794) · 更新日期：2026-11-05
> **Trixie 狀態：**本課以 Trixie 64 位元作主要教學目標；待重測項目以[基線與測試矩陣](./乾淨系統基線與測試矩陣.md)標示。Bookworm 舊輸出不代表新系統已通過。

> 舊版 Thonny 測試曾執行 Picamera2 取像和 OpenCV 灰階轉換；Trixie 的 Picamera2 基線已確認能取得 640 × 480 影格，但本篇指定尺寸、色彩和 Thonny 步驟仍需在新 venv 重測。完整原文情境及其他舊案例仍須依下文標示重測。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

## 學習目標

用 Picamera2 擷取彩色影格，再用 OpenCV 轉成灰階陣列。

## 背景與原理

相機先取得彩色影格，影像處理程式再依需要轉換或分析。Picamera2 負責擷取，OpenCV 提供影像轉換與分析工具；兩者處理的是同一張影像的不同階段。灰階只有亮度層次，資料量較彩色影像少，也常作為邊緣或輪廓處理的輸入，但會失去顏色資訊。

本機範例輸入尺寸為寬 320、高 240；Python 的影像陣列通常以 `(高, 寬, 通道數)` 顯示。注意相機格式和顏色通道的排列需以使用環境驗證；不能只依 `RGB888` 名稱猜測每個陣列通道在所有環境中的順序。本例只驗證陣列尺寸和轉換可以執行，尚未量測灰階亮度正確性。

```mermaid
flowchart LR
    A[相機] --> B[Picamera2 彩色陣列]
    B --> C[OpenCV 灰階轉換]
    C --> D[單通道陣列]
```

上圖是概念示意，並非操作畫面。[Raspberry Pi 官方相機文件](https://www.raspberrypi.com/documentation/accessories/camera-software.html)可供延伸閱讀。

## 事前準備

相機已連接，且 Raspberry Pi OS 原生 Python 可以匯入 Picamera2。請在 Thonny 執行[相機環境建立程式](./範例程式/Thonny建立相機環境.py)，輸入 `lesson-15`，再選取 `/home/pi/ba5077-camera-lesson-15/bin/python3`。接著執行[第 14 課安裝程式](./範例程式/第14課-Thonny安裝套件.py)，把本課需要的 OpenCV 與 NumPy 安裝在這個新環境。版本與環境建立原理見[Thonny 環境指南](./Thonny環境與套件安裝.md)。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第15課.py`；完整檔案也在[範例程式](./範例程式/第15課.py)。

```python
import cv2
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={"size": (320, 240), "format": "RGB888"}))
    camera.start()
    frame = camera.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("frame", frame.shape)
    print("gray", gray.shape)
finally:
    camera.stop()
    camera.close()
```

在 Thonny 選 **File → Open** 開啟 `第15課.py`，確認右下角是包含所需套件的 Python 環境，再點綠色執行鈕。若程式會輸出檔案，先在新的練習目錄操作，避免覆寫。

## 舊測試紀錄（Bookworm；非 Trixie 驗收）

```text
frame (240, 320, 3)
gray (240, 320)
```

![Bookworm 歷史測試：第 15 課在 Thonny 的程式與 Shell 畫面](./圖檔/thonny2-camera-env-test.png)

舊測試選用 `/home/pi/ba5077-camera-20261029/bin/python3`。該測試環境建立於 Bookworm，不能證明 Trixie 的安裝步驟成功；Trixie 新環境的相機影格、色彩通道與灰階轉換仍待驗收。

彩色影格有三個通道，灰階結果有單一通道。相機格式與 OpenCV 的色彩順序需要依格式確認；本例未驗證 GUI 預覽。

## 學生練習與應用

1. 從輸出指出高度、寬度及通道數；為什麼灰階沒有第三個維度？
2. 想像在彩色圖中區分紅色和綠色物件，轉成灰階可能失去什麼資訊？
3. 接續第 17 課，觀察保存的灰階圖片，再到第 28 課比較彩色遮罩。

灰階可用於文件預處理與邊緣偵測；若工作依賴顏色，應保留彩色影像或選擇適合的色彩空間。

## 預期結果

目前可支持的基本預期是收到一張指定尺寸的彩色影格並產生單通道灰階陣列。顏色通道和亮度正確性仍要用可辨識色塊逐項驗證。

## 常見錯誤與排查

若 cvtColor 回報通道錯誤，先印出影格 shape、設定的 camera format 和程式選用的轉換碼，再以紅、綠、藍色塊檢查實際通道順序；不能只憑 RGB888 名稱推測。

## 與原文章的差異

- 新增以 Thonny 操作的實測與截圖：Picamera2 單張影格及 OpenCV 灰階轉換。

- 由舊 `libcamera-*` 安裝流程改為已存在的 Picamera2 與本機可執行範例；沒有執行原文的桌面預覽。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 新增上方基本程式在 Thonny 執行的操作截圖；其他情境以各段落標示為準。
