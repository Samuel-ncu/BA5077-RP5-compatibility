import cv2

video = cv2.VideoCapture('lesson16-camera.avi')
frames = []
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        frames.append(frame)
finally:
    video.release()
if len(frames) < 2:
    raise RuntimeError('影片必須至少包含兩張影格，請先完成第 16 課')
first = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
last = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY)
diff = cv2.absdiff(first, last)
_, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
panels = cv2.hconcat([frames[0], frames[-1], cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
if not cv2.imwrite('lesson26-camera-diff.png', panels):
    raise RuntimeError('無法儲存結果圖')
print('frames read:', len(frames))
print('first and last changed pixels:', cv2.countNonZero(mask))
print('saved: lesson26-camera-diff.png')
