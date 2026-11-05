from pathlib import Path
from importlib.metadata import version

import cv2
import numpy as np

image = np.zeros((120, 160, 3), dtype=np.uint8)
cv2.rectangle(image, (20, 20), (140, 100), (0, 255, 0), 3)

encoded_ok, encoded = cv2.imencode(".png", image)
decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR) if encoded_ok else None
output = Path("lesson14-opencv-test.png")
saved = decoded is not None and cv2.imwrite(str(output), decoded)

print("OpenCV module:", cv2.__version__)
print("OpenCV wheel:", version("opencv-python"))
print("NumPy:", np.__version__)
print("Image shape:", image.shape)
print("Encode/decode:", encoded_ok and decoded is not None)
print("Saved:", saved)
