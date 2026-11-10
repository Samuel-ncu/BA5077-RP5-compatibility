from pathlib import Path
import cv2

folder = Path(__file__).resolve().parent
video = cv2.VideoCapture(str(folder / 'lesson41-moving-output.avi'))
if not video.isOpened():
    raise RuntimeError('Cannot open output video; run the previous example first')
count = 0
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        cv2.imshow('YOLO moving video playback', frame)
        count += 1
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
finally:
    video.release()
    cv2.destroyAllWindows()
print('displayed frames:', count)
