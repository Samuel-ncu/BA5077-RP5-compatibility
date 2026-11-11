"""第 28 課：用 Picamera2 相機即時追蹤紅色物體（不做透視校正的版本）。

在 Raspberry Pi 5 桌面的 Thonny 執行。右下角請選能同時匯入
picamera2、cv2、numpy 的直譯器（本課紀錄使用
/home/pi/ba5077-camera-contrib-trixie-20261110/bin/python3）。

相機前要有紅色物體在移動，例如另一個螢幕上播放的
「RP5相機測試.html → 移動追蹤」畫面，或一個紅色杯子。
執行後會跳出預覽視窗：左邊是相機畫面加上綠框與中心點，
右邊是紅色遮罩（白色＝被判定為紅色的像素）。
按 q 提早停止；不按也會在 MAX_SECONDS 秒後自動停止。
輸出檔放在這支程式所在的資料夾，同名檔會被覆寫：
  lesson28-camera-track.png  停止前最後一張預覽畫面
"""
from pathlib import Path
import time

import cv2
import numpy as np
from picamera2 import Picamera2

MAX_SECONDS = 20          # 最多執行幾秒
SIZE = (640, 480)         # 相機影像寬、高
MIN_AREA = 500            # 小於這個面積（像素）的紅色區塊當作雜訊

# 紅色在 HSV 的色相（H）橫跨 0 和 179 兩端，所以要用兩段範圍再合併
LOWER_RED_1, UPPER_RED_1 = (0, 120, 80), (10, 255, 255)
LOWER_RED_2, UPPER_RED_2 = (170, 120, 80), (179, 255, 255)

folder = Path(__file__).resolve().parent
result_path = folder / "lesson28-camera-track.png"

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": SIZE, "format": "RGB888"}))
camera.start()
time.sleep(1)             # 讓相機先調好曝光

frames = 0
centers = []              # 每張偵測到的中心 (x, y)
trail = []                # 最近 30 個中心，用來畫移動軌跡
last_view = None
stopped_by = "time limit"
start = time.monotonic()
try:
    while time.monotonic() - start < MAX_SECONDS:
        frame = camera.capture_array()          # 這個設定下的陣列是 OpenCV 用的 BGR 順序
        frames += 1
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_RED_1, UPPER_RED_1) | cv2.inRange(hsv, LOWER_RED_2, UPPER_RED_2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        big = [c for c in contours if cv2.contourArea(c) > MIN_AREA]
        if big:
            x, y, w, h = cv2.boundingRect(max(big, key=cv2.contourArea))
            center = (x + w // 2, y + h // 2)
            centers.append(center)
            trail = (trail + [center])[-30:]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, center, 5, (255, 0, 0), -1)
            cv2.putText(frame, f"center {center}", (x, max(20, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        for a, b in zip(trail, trail[1:]):
            cv2.line(frame, a, b, (255, 0, 255), 2)
        cv2.putText(frame, f"frame {frames}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        last_view = cv2.hconcat([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
        cv2.imshow("lesson28 red tracking (press q to stop)", last_view)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            stopped_by = "q"
            break
finally:
    seconds = time.monotonic() - start
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()

if last_view is not None:
    cv2.imwrite(str(result_path), last_view)
print("stopped by", stopped_by)
print("frames:", frames, "seconds:", round(seconds, 1), "fps:", round(frames / seconds, 1))
print("red detections:", len(centers))
if centers:
    xs = [c[0] for c in centers]
    print("first centers:", centers[:3])
    print("last centers:", centers[-3:])
    print("x range:", min(xs), "to", max(xs))
print("saved:", result_path.name)
