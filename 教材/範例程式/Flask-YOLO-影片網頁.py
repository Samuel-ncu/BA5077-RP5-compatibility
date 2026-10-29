import cv2
from flask import Flask, Response
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('yolov8n.pt')


@app.get('/')
def home():
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
    <title>RP5 YOLO video demonstration</title></head><body>
    <h1>RP5 YOLO video demonstration</h1>
    <p>Four recorded camera frames; CPU inference. This stream ends.</p>
    <img src="/stream" alt="YOLO annotated video frames" width="800">
    </body></html>'''


@app.get('/stream')
def stream():
    def frames():
        video = cv2.VideoCapture('lesson42-input.avi')
        if not video.isOpened():
            raise RuntimeError('無法開啟 lesson42-input.avi')
        try:
            while True:
                ok, frame = video.read()
                if not ok:
                    break
                annotated = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0].plot()
                ok, jpeg = cv2.imencode('.jpg', annotated)
                if not ok:
                    raise RuntimeError('無法編碼 JPEG')
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            yield b'--frame--\r\n'
        finally:
            video.release()
    return Response(frames(), content_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # 只在 RP5 本機測試，不開放給區域網路。
    app.run(host='127.0.0.1', port=18766, debug=False, threaded=False)
