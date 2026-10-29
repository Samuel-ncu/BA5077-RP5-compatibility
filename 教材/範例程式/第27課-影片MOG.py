import cv2

if not hasattr(cv2, 'bgsegm'):
    raise RuntimeError('目前 OpenCV 缺少 bgsegm，無法建立 MOG')
mog = cv2.bgsegm.createBackgroundSubtractorMOG()
video = cv2.VideoCapture('lesson16-camera.avi')
frames = 0
last_image = last_mask = None
try:
    while True:
        ok, image = video.read()
        if not ok:
            break
        last_mask = mog.apply(image)
        last_image = image
        frames += 1
finally:
    video.release()
if frames == 0:
    raise RuntimeError('影片沒有可讀取的影格，請先完成第 16 課')
panels = cv2.hconcat([last_image, cv2.cvtColor(last_mask, cv2.COLOR_GRAY2BGR)])
if not cv2.imwrite('lesson27-camera-mog.png', panels):
    raise RuntimeError('無法儲存結果圖')
print('MOG created:', True)
print('frames processed:', frames)
print('last mask nonzero pixels:', cv2.countNonZero(last_mask))
print('saved: lesson27-camera-mog.png')
