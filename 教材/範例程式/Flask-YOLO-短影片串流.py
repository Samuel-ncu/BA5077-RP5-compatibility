import threading
from urllib.request import urlopen
import cv2
import numpy as np
from flask import Flask, Response
from ultralytics import YOLO
from werkzeug.serving import make_server

app = Flask(__name__)
model = YOLO('yolov8n.pt')


@app.get('/stream')
def stream():
    def frames():
        video = cv2.VideoCapture('lesson42-input.avi')
        if not video.isOpened():
            raise RuntimeError('無法開啟影片')
        try:
            while True:
                ok, frame = video.read()
                if not ok:
                    break
                result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0].plot()
                ok, jpeg = cv2.imencode('.jpg', result)
                if not ok:
                    raise RuntimeError('JPEG 編碼失敗')
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            yield b'--frame--\r\n'
        finally:
            video.release()
    return Response(frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # 只供本機測試；0 讓系統挑選空閒連接埠，測試完後關閉。
    server = make_server('127.0.0.1', 0, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f'http://127.0.0.1:{server.server_port}/stream', timeout=60) as response:
            payload = response.read()
            print('HTTP status:', response.status)
            print('content type:', response.headers['Content-Type'])
        parts = payload.split(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n')[1:]
        images = []
        for part in parts:
            jpeg_bytes = part.split(b'\r\n--frame--\r\n')[0].rstrip(b'\r\n')
            images.append(cv2.imdecode(np.frombuffer(jpeg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR))
        print('JPEG frames:', len(images))
        print('all frames decoded:', all(image is not None for image in images))
        if images and images[0] is not None:
            if not cv2.imwrite('flask-yolo-stream-frame.png', images[0]):
                raise RuntimeError('結果圖儲存失敗')
            print('saved: flask-yolo-stream-frame.png')
    finally:
        server.shutdown()
        thread.join()
