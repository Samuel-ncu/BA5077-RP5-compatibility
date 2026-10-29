# 第 18 課｜使用 Picamera2 拍攝照片並保存至本地

[原始文章](https://liusming.pixnet.net/blog/posts/14222886372) · 更新日期：2026-10-29

## 學習目標

使用 Picamera2 拍攝並儲存一張照片，並確認檔案建立。

## 事前準備

相機已連接；程式會在目前目錄寫入 `lesson18-photo.jpg`，請先確認不會覆蓋自己的檔案。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第18課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第18課.py)。

```python
from pathlib import Path
from picamera2 import Picamera2

path = Path("lesson18-photo.jpg")
camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={"size": (320, 240)}))
    camera.start()
    camera.capture_file(str(path))
    print("photo saved:", path.exists())
finally:
    camera.stop()
    camera.close()
```

在該檔案所在的目錄執行 `python3 第18課.py`。

## 本機實際輸出

```text
photo saved: True
```

本機實測檔案成功建立。測試照片包含相機現場影像，因此未放到公開 repo；使用者應自行檢查拍攝內容及分享對象。

## 與原文章的差異

- 明確加入檔案存在檢查；不將可能包含私人環境的照片公開。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 尚未補拍操作畫面；圖檔（若有）是程式產生的結果，不冒充螢幕截圖。
