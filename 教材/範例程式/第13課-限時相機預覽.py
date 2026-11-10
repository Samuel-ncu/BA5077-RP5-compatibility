from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
try:
    camera.configure(camera.create_preview_configuration(main={'size': (640, 480)}))
    camera.start_preview(Preview.QTGL)
    camera.start()
    print('Preview started for 20 seconds', flush=True)
    sleep(20)
finally:
    camera.stop()
    camera.stop_preview()
    camera.close()
print('Camera closed')
