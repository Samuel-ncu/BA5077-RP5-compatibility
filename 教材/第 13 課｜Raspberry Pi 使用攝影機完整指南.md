# 第 13 課｜Raspberry Pi 使用攝影機完整指南

[原始文章](https://liusming.pixnet.net/blog/posts/14222876433) · 更新日期：2026-11-05
> **Trixie 狀態：**本課以 Trixie 64 位元作主要教學目標；待重測項目以[基線與測試矩陣](./乾淨系統基線與測試矩陣.md)標示。Bookworm 舊輸出不代表新系統已通過。

> Trixie 基線已確認 Picamera2 可回傳 640 × 480 影格；本課完整程式、Thonny 操作畫面、預覽與 USB 相機尚待逐項驗收。本文既有 320 × 240 輸出與 Thonny 畫面屬舊測試，不能當作 Trixie 乾淨系統的完成證據。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

## 學習目標

認識 Picamera2 的建立、啟動、擷取與釋放流程。此示範只取得一張影格，不啟動無限錄影程序。

## 背景與原理

攝影機能把光線轉換成影像資料，供人觀看或讓程式分析。RP5 可搭配相機模組，透過相機軟體取得畫面；這台機器實際使用的是 IMX708 廣角相機。CSI 相機與 USB 攝影機的裝置介面可能不同，不能因某一種能用就假設另一種使用相同程式。

Picamera2 是 Python 使用 Raspberry Pi 相機的介面。先設定影格大小，再啟動相機並擷取資料，最後停止、釋放資源；如果另一個程式正佔用相機，新的程式可能無法啟動。[官方相機軟體文件](https://www.raspberrypi.com/documentation/accessories/camera-software.html)說明相機連接與相關工具。

```mermaid
flowchart LR
    A[相機感測光線] --> B[相機系統處理影像]
    B --> C[Picamera2 擷取影格]
    C --> D[Python 分析或保存]
```

這是概念圖，不是操作截圖。影格就是某一時刻的一張影像；連續取得多張影格則可形成影片。

## 事前準備

相機已連接，且 Raspberry Pi OS 原生 Python 可以匯入 Picamera2。為了不依賴先前課程留下的套件，先在 Thonny 執行[相機環境建立程式](./範例程式/Thonny建立相機環境.py)，並在 Shell 輸入 `lesson-13`。再到 **Tools → Options → Interpreter** 選取 `/home/pi/ba5077-camera-lesson-13/bin/python3`。程式只用 Picamera2，不需另外安裝 OpenCV。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第13課.py`；完整檔案也在[範例程式](./範例程式/第13課.py)。截至 2026-11-05，這個完整步驟尚未在 Trixie 新建環境中重跑。

```python
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={"size": (320, 240), "format": "RGB888"}))
    camera.start()
    frame = camera.capture_array()
    print("camera", frame.shape, str(frame.dtype))
finally:
    camera.stop()
    camera.close()
```

在 Thonny 選 **File → Open** 開啟 `第13課.py`，確認右下角是包含所需套件的 Python 環境，再點綠色執行鈕。若程式會輸出檔案，先在新的練習目錄操作，避免覆寫。

## 舊測試紀錄（Bookworm；非 Trixie 驗收）

```text
camera (240, 320, 3) uint8
```

![Bookworm 歷史測試：第 13 課在 Thonny 的程式與 Shell 畫面](./圖檔/lesson13-thonny2.png)

舊測試選用既有環境 `/home/pi/myenv/bin/python3`，不是從乾淨系統重建的環境。新的操作流程請使用本文「事前準備」所連結的環境建立程式；相機格式、預覽及 USB 攝影機仍待 Trixie 逐項驗收。更多環境說明見[Thonny 環境指南](./Thonny環境與套件安裝.md)。

影格是高度 240、寬度 320 的三通道陣列；`uint8` 是每個通道的資料型別。這不代表圖形預覽或 USB 攝影機已測試。

## 練習與應用

1. 說明輸出 `(240, 320, 3)` 的高度、寬度與通道數；它與設定的 `(320, 240)` 為何順序不同？
2. 檢查目前是否有其他相機程式佔用裝置，然後再執行範例。
3. 延伸至第 18 課，將影格存成照片；再思考哪些拍攝內容不適合直接公開。

相機擷取可用在影像監測或產品檢測；要得到可信結果，還須驗證光線、拍攝位置、畫質、隱私和錯誤處理。

## 預期結果

Picamera2 單張擷取應回傳寬、高與通道資訊；程式完成後相機應可釋放，讓下一個相機程式能再次啟動。

## 常見錯誤與排查

相機開啟失敗時，先確認 CSI 相機可見、選到含系統 Picamera2 的環境，而且沒有其他程式占用相機。確認 finally 區塊可執行 stop 和 close。

## 與原文章的差異

- 新增以 Thonny 操作的實測與截圖：Picamera2 單張影格擷取；不含預覽或 USB 相機。

- 原文以持續執行的 `libcamera-vid` 接著使用 `VideoCapture(0)`；本版採 Picamera2 單張擷取，避免阻塞並配合本機 CSI 相機。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 新增上方基本程式在 Thonny 執行的操作截圖；其他情境以各段落標示為準。
