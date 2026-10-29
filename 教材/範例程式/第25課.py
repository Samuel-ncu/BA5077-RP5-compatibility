import cv2
import numpy as np
rng = np.random.default_rng(42)
frame = np.zeros((200, 300, 3), dtype=np.uint8)
frame[60:120, 80:140] = rng.integers(0, 256, (60, 60, 3), dtype=np.uint8)
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, (80, 60, 60, 60))
success, box = tracker.update(frame.copy())
print('tracker created', True)
print('same frame update', success)
