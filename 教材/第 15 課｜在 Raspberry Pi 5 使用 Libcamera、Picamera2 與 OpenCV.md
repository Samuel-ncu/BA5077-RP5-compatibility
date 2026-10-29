# 第 15 課｜在 Raspberry Pi 5 使用 Libcamera、Picamera2 與 OpenCV

[原始文章](https://liusming.pixnet.net/blog/posts/14222875794) · 更新日期：2026-10-29

## 學習目標

用 Picamera2 擷取彩色影格，再用 OpenCV 轉成灰階陣列。

## 事前準備

相機與 Picamera2、OpenCV 已可使用。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第15課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第15課.py)。

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

在該檔案所在的目錄執行 `python3 第15課.py`。

## 本機實際輸出

```text
frame (240, 320, 3)
gray (240, 320)
```

彩色影格有三個通道，灰階結果有單一通道。相機格式與 OpenCV 的色彩順序需要依格式確認；本例未驗證 GUI 預覽。

## 與原文章的差異

- 由舊 `libcamera-*` 安裝流程改為已存在的 Picamera2 與本機可執行範例；沒有執行原文的桌面預覽。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 尚未補拍操作畫面；圖檔（若有）是程式產生的結果，不冒充螢幕截圖。
