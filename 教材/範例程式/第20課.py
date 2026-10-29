import cv2
import numpy as np

image = np.zeros((240, 320, 3), dtype=np.uint8)
cv2.putText(image, "SIMPLEX", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(image, "PLAIN", (20, 140), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
print("saved", cv2.imwrite("lesson20-fonts.png", image))
