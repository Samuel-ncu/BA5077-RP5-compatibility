import cv2

video = cv2.VideoCapture('repeat-120s-output.avi')
if not video.isOpened():
    raise RuntimeError('無法開啟輸出影片')
count = 0
try:
    while count < 12:
        ok, frame = video.read()
        if not ok:
            break
        count += 1
        cv2.imshow('YOLO video playback sample', frame)
        cv2.waitKey(333)
finally:
    video.release()
    cv2.destroyAllWindows()
print('displayed frames:', count)
