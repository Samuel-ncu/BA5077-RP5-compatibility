from pathlib import Path
from picamera2 import Picamera2

path = Path("lesson18-photo.jpg")
camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={"size": (1920, 1080)}))
    camera.start()
    camera.capture_file(str(path))
    print("photo saved:", path.exists())
finally:
    camera.stop()
    camera.close()
