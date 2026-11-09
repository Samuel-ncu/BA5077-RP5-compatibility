"""第 14 課：建立、保存與顯示一張 OpenCV 圖片。"""
from pathlib import Path
import sys
import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.circle(image, (160, 120), 70, (0, 255, 0), -1)
cv2.putText(image, "OpenCV", (80, 225), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)
out = Path.home() / "Pictures" / "lesson14-opencv.png"
if out.exists():
    raise FileExistsError(f"File exists: {out}. Rename it before running.")
if not cv2.imwrite(str(out), image):
    raise RuntimeError(f"Could not save: {out}")
print("Python:", sys.version.split()[0], flush=True)
print("OpenCV:", cv2.__version__, flush=True)
print("NumPy:", np.__version__, flush=True)
print("Image shape:", image.shape, flush=True)
print("Center BGR:", image[120, 160].tolist(), flush=True)
print("Saved:", out, flush=True)
print("Showing window: press any key or wait 30 seconds.", flush=True)
cv2.imshow("Lesson 14 OpenCV", image)
cv2.waitKey(30000)
cv2.destroyAllWindows()
print("Window closed.", flush=True)
