# 使用 Flask 和 YOLO 打造即時物件偵測網頁介面

[原始文章](https://liusming.pixnet.net/blog/posts/14222901408) · 更新日期：2026-10-29

## 學習目標

以 Flask 測試客戶端驗證首頁與一次相機 JPEG 推論回應。

## 事前準備

需要 Pi 相機、Flask、Picamera2、YOLO CPU 虛擬環境與模型檔。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#7-yolo-與-pytorch)建立並啟用 YOLO CPU 環境，再於練習目錄下載模型：

```bash
curl -fL https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt -o yolov8n.pt
```

不要使用原文的 CUDA 11.8 索引。

## 程式與執行

將下列已在 RP5 執行的程式存為 `Flask與YOLO.py`，或使用[範例程式](./範例程式/Flask與YOLO.py)。先確認目前目錄及檔案，避免覆蓋已有資料。

```python
import cv2
from flask import Flask, Response
from picamera2 import Picamera2
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('yolov8n.pt')

@app.get('/')
def index():
    return '<h1>RP5 YOLO</h1><img src="/frame" alt="camera result">'

@app.get('/frame')
def frame():
    camera = Picamera2()
    try:
        camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
        camera.start()
        image = camera.capture_array()
    finally:
        camera.stop()
        camera.close()
    result = model.predict(image, imgsz=320, device='cpu', verbose=False)[0].plot()
    ok, jpeg = cv2.imencode('.jpg', result)
    if not ok:
        return Response('JPEG encoding failed', status=500)
    return Response(jpeg.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':
    with app.test_client() as client:
        home = client.get('/')
        result = client.get('/frame')
        print('home status', home.status_code)
        print('frame status', result.status_code)
        print('frame type', result.mimetype)
```

執行 `python3 Flask與YOLO.py`。

## 本機實際輸出

```text
home status 200
frame status 200
frame type image/jpeg
```

這是程序內 Flask 測試客戶端，不會啟動公開伺服器；它提供單張 JPEG，並非已驗證的即時串流網頁。

## 與原文章的差異

- 原文提供即時物件偵測網頁；本版先安全測試單張影格與 HTTP 回應，未聲稱即時串流已完成。
- 真實場景的準確率、速度和操作畫面尚未完整驗證。
- 尚未保存操作畫面截圖。
