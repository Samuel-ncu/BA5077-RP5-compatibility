"""第 13 課：用 OpenCV 讀回 rpicam-vid 錄好的影片。

請把這支程式和 lesson13-test.mp4 放在同一個資料夾（本教材用 ~/lesson13），
在 Thonny 選第 14 課的 OpenCV 環境（/home/pi/opencv-course-env/bin/python3）後按 Run。
"""
import cv2

video = cv2.VideoCapture("lesson13-test.mp4")
print("opened", video.isOpened(), "fps", round(video.get(cv2.CAP_PROP_FPS), 2))
count = 0
shape = None
while True:
    ok, frame = video.read()
    if not ok:
        break
    count += 1
    shape = frame.shape
video.release()
print("frames read", count, "shape", shape)
