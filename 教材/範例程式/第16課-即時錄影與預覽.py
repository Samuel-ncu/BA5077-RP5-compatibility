"""第 16 課：Picamera2 連續取像、即時顯示並錄成影片。

在 Raspberry Pi 5 桌面的 Thonny 執行。右下角請選能同時匯入
picamera2、cv2、numpy 的直譯器（本課紀錄使用
/home/pi/ba5077-camera-contrib-trixie-20261110/bin/python3）。

執行後會跳出預覽視窗：左邊是相機原始畫面，右邊是轉成灰階、
加上邊緣的處理結果。按 q 提早停止；不按也會在 MAX_SECONDS 秒後自動停止。
輸出檔放在這支程式所在的資料夾，同名檔會被覆寫：
  lesson16-live.avi          錄下的處理後影片
  lesson16-live-preview.png  停止前最後一張預覽畫面
"""
from pathlib import Path
import time

import cv2
import numpy as np
from picamera2 import Picamera2

MAX_SECONDS = 20      # 最長錄影秒數；想錄久一點就改這個數字
FPS = 10              # 要求相機每秒給 10 張，也當作影片的播放速度
SIZE = (640, 480)     # 寬, 高

folder = Path(__file__).resolve().parent
video_path = folder / "lesson16-live.avi"
preview_path = folder / "lesson16-live-preview.png"

camera = Picamera2()
writer = None
written = 0
last_view = None
start = time.monotonic()
try:
    config = camera.create_video_configuration(
        main={"size": SIZE, "format": "RGB888"},
        controls={"FrameRate": FPS},
    )
    camera.configure(config)
    camera.start()
    time.sleep(1)  # 讓曝光與白平衡先穩定

    writer = cv2.VideoWriter(str(video_path), cv2.VideoWriter_fourcc(*"MJPG"), FPS, SIZE)
    if not writer.isOpened():
        raise RuntimeError("無法建立 MJPG 影片，請檢查資料夾權限與磁碟空間")

    start = time.monotonic()
    while True:
        frame = camera.capture_array()          # 等到下一張影格才回來
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 60, 150)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        processed[edges > 0] = (0, 255, 0)      # 邊緣畫成綠色

        elapsed = time.monotonic() - start
        cv2.putText(processed, f"REC {elapsed:4.1f}s frame {written + 1}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        writer.write(processed)
        written += 1

        last_view = cv2.hconcat([frame, processed])
        cv2.imshow("lesson16 live (press q to stop)", last_view)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("stopped by q")
            break
        if elapsed >= MAX_SECONDS:
            print("stopped by time limit")
            break
finally:
    elapsed = time.monotonic() - start
    if writer is not None:
        writer.release()
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()

if last_view is not None:
    cv2.imwrite(str(preview_path), last_view)

reader = cv2.VideoCapture(str(video_path))
read_count = 0
while True:
    ok, _ = reader.read()
    if not ok:
        break
    read_count += 1
reader.release()

print("frames written:", written)
print("seconds:", round(elapsed, 1))
print("measured fps:", round(written / elapsed, 1) if elapsed > 0 else 0)
print("frames read back:", read_count)
print("saved:", video_path.name, preview_path.name)
