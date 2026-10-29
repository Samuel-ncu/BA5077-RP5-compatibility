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
