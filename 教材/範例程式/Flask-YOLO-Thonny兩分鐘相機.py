import threading
import time
import webbrowser

import cv2
from flask import Flask, Response, jsonify
from picamera2 import Picamera2
from ultralytics import YOLO
from werkzeug.serving import make_server


def main():
    app = Flask(__name__)
    model = YOLO('yolov8n.pt')
    started = threading.Event()
    finished = threading.Event()
    lock = threading.Lock()
    stats = {'frames': 0, 'state': 'waiting'}

    @app.get('/')
    def home():
        return '''<!doctype html><html><head><meta charset="utf-8">
        <title>RP5 Camera YOLO</title></head><body>
        <h1>RP5 Camera YOLO</h1>
        <p>Two-minute single-client camera test.</p>
        <p id="status">Waiting for camera...</p>
        <button onclick="document.getElementById('feed').style.visibility='hidden'">
          Hide preview</button>
        <p><img id="feed" src="/stream" alt="camera stream"></p>
        <script>
        async function update() {
          try {
            const response = await fetch('/status', {cache: 'no-store'});
            const data = await response.json();
            document.getElementById('status').textContent =
              'Server frames produced: ' + data.frames + ' | state: ' + data.state;
            if (data.state !== 'finished') setTimeout(update, 1000);
          } catch (error) {
            document.getElementById('status').textContent = 'Status unavailable';
          }
        }
        update();
        </script></body></html>'''

    @app.get('/status')
    def status():
        with lock:
            return jsonify(stats.copy())

    @app.get('/stream')
    def stream():
        with lock:
            if started.is_set():
                return 'This example supports one camera stream.', 409
            started.set()

        def frames():
            camera = Picamera2()
            count = 0
            begin = None
            next_report = 30
            try:
                camera.configure(camera.create_preview_configuration(
                    main={'size': (640, 480), 'format': 'RGB888'}))
                camera.start()
                time.sleep(1)
                begin = time.perf_counter()
                with lock:
                    stats['state'] = 'streaming'
                while time.perf_counter() - begin < 120:
                    frame = camera.capture_array()
                    result = model.predict(frame, imgsz=320, device='cpu', verbose=False)[0]
                    ok, jpeg = cv2.imencode('.jpg', result.plot())
                    if not ok:
                        raise RuntimeError('JPEG 編碼失敗')
                    count += 1
                    elapsed = time.perf_counter() - begin
                    with lock:
                        stats['frames'] = count
                    if elapsed >= next_report:
                        print(f'after {next_report}s: frames={count}', flush=True)
                        next_report += 30
                    yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
                yield b'--frame--\r\n'
            finally:
                elapsed = time.perf_counter() - begin if begin is not None else 0
                camera.stop()
                camera.close()
                with lock:
                    stats['state'] = 'finished'
                print('camera frames:', count, flush=True)
                print('elapsed seconds:', round(elapsed, 2), flush=True)
                print('average FPS:', round(count / elapsed, 2) if elapsed else 0, flush=True)
                print('camera released', flush=True)
                finished.set()
        return Response(frames(), content_type='multipart/x-mixed-replace; boundary=frame')

    server = make_server('127.0.0.1', 18766, app, threaded=True)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        print('Open: http://127.0.0.1:18766/', flush=True)
        print('Browser opened:', webbrowser.open('http://127.0.0.1:18766/'), flush=True)
        if not started.wait(30):
            print('No browser stream in 30 seconds', flush=True)
        elif not finished.wait(150):
            print('Camera stream did not finish in time', flush=True)
        else:
            time.sleep(5)  # 讓頁面有機會讀取完成狀態。
    finally:
        server.shutdown()
        worker.join()
        server.server_close()
        print('server stopped', flush=True)


if __name__ == '__main__':
    main()
