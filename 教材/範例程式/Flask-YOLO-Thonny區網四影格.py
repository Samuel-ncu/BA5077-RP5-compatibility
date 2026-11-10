from pathlib import Path
import threading
import time

import cv2
from flask import Flask, Response
from ultralytics import YOLO
from werkzeug.serving import WSGIRequestHandler, make_server


def main():
    folder = Path(__file__).resolve().parent
    model = YOLO(str(folder / 'yolov8n.pt'))
    app = Flask(__name__)
    finished = threading.Event()
    stats = {'frames': 0}
    stream_lock = threading.Lock()

    @app.get('/')
    def home():
        return ('<!doctype html><html><head><meta charset="utf-8">'
                '<title>RP5 YOLO test</title></head><body>'
                '<h1>RP5 YOLO video test</h1>'
                '<p>Four prerecorded frames; stream ends automatically.</p>'
                '<img src="/stream" alt="YOLO video output">'
                '</body></html>')

    @app.get('/stream')
    def stream():
        if not stream_lock.acquire(blocking=False):
            return 'Stream already in use', 409

        def frames():
            video = cv2.VideoCapture(str(folder / 'lesson42-input.avi'))
            try:
                if not video.isOpened():
                    raise RuntimeError('Cannot open lesson42-input.avi')
                while stats['frames'] < 4:
                    ok, frame = video.read()
                    if not ok:
                        break
                    result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
                    ok, jpeg = cv2.imencode('.jpg', result.plot())
                    if not ok:
                        raise RuntimeError('JPEG encoding failed')
                    stats['frames'] += 1
                    yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
                    time.sleep(1)  # 讓讀者有時間觀察各張影格。
                yield b'--frame--\r\n'
            finally:
                video.release()
                finished.set()
                stream_lock.release()
        return Response(frames(), content_type='multipart/x-mixed-replace; boundary=frame')

    class QuietHandler(WSGIRequestHandler):
        def log_request(self, code='-', size='-'):
            pass

    server = make_server('0.0.0.0', 0, app, threaded=True, request_handler=QuietHandler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    print('Listening port:', server.server_port, flush=True)
    print('Open from the same LAN: http://<RP5-IP>:<port>/', flush=True)
    try:
        finished.wait(90)
    finally:
        server.shutdown()
        server.server_close()
        print('frames served:', stats['frames'], flush=True)
        print('server closed', flush=True)


if __name__ == '__main__':
    main()
