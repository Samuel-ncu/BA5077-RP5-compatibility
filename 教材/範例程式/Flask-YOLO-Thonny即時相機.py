import time
import threading
import webbrowser
import cv2
from flask import Flask, Response
from picamera2 import Picamera2
from ultralytics import YOLO
from werkzeug.serving import make_server


def main():
    app = Flask(__name__)
    model = YOLO('yolov8n.pt')

    @app.get('/')
    def home():
        return ('<h1>RP5 Camera YOLO</h1>'
                '<p>Live camera, 150 frames, then stops.</p>'
                '<img src="/stream" alt="camera stream">')

    @app.get('/stream')
    def stream():
        def frames():
            camera = Picamera2()
            count = 0
            try:
                camera.configure(camera.create_preview_configuration(
                    main={'size': (640, 480), 'format': 'RGB888'}))
                camera.start()
                time.sleep(1)
                while count < 150:
                    frame = camera.capture_array()
                    result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
                    ok, jpeg = cv2.imencode('.jpg', result.plot())
                    if not ok:
                        raise RuntimeError('JPEG 編碼失敗')
                    count += 1
                    yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
                yield b'--frame--\r\n'
            finally:
                camera.stop()
                camera.close()
                print('camera frames:', count, flush=True)
                print('camera released', flush=True)
        return Response(frames(), content_type='multipart/x-mixed-replace; boundary=frame')

    server = make_server('127.0.0.1', 18766, app, threaded=True)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        print('Open: http://127.0.0.1:18766/', flush=True)
        print('Browser opened:', webbrowser.open('http://127.0.0.1:18766/'), flush=True)
        time.sleep(70)
    finally:
        server.shutdown()
        worker.join()
        server.server_close()
        print('server stopped', flush=True)


if __name__ == '__main__':
    main()
