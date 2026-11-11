"""補充 1、2、4、5、6 共用：在目前 Trixie 用 CVZone 2.0（MediaPipe 1.x Tasks API）找手和臉。

Thonny 右下角請選「Thonny建立Trixie-MediaPipe環境.py」建立的環境。
把 facehand-board.png 和本程式放在同一個資料夾。第一次執行時，CVZone 會把
hand_landmarker.task、face_landmarker.task 兩個模型下載到 Thonny 當下的工作資料夾（需要網路）。
輸出 supplement-cvzone-result.png，同名檔會被覆寫。
"""
from pathlib import Path
from importlib.metadata import version

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector

folder = Path(__file__).resolve().parent
image = cv2.imread(str(folder / 'facehand-board.png'))
if image is None:
    raise RuntimeError('找不到 facehand-board.png，請和程式放在同一個資料夾')
print('MediaPipe:', version('mediapipe'), 'CVZone:', version('cvzone'))

hand_detector = HandDetector(staticMode=True, maxHands=1)
face_detector = FaceMeshDetector(staticMode=True, maxFaces=1)

hands, image = hand_detector.findHands(image, draw=True, flipType=False)
image, faces = face_detector.findFaceMesh(image, draw=True)
print('hands:', len(hands), 'hand points:', [len(h['lmList']) for h in hands])
print('faces:', len(faces), 'face points:', [len(f) for f in faces])

if hands:
    points = hands[0]['lmList']
    # 影像的 y 往下變大：指尖 y 比第二關節小，表示這根手指伸直朝上。
    up = [points[tip][1] < points[pip][1] for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]]
    if all(up):
        gesture = 'paper'
    elif not any(up):
        gesture = 'rock'
    elif up == [True, True, False, False]:
        gesture = 'scissors'
    else:
        gesture = 'unknown'
    print('finger states:', up)
    print('gesture:', gesture)

# 用完就關閉模型，避免程式結束時出現關閉順序的錯誤訊息。
hand_detector.detector.close()
face_detector.detector.close()

output = folder / 'supplement-cvzone-result.png'
if not cv2.imwrite(str(output), image):
    raise RuntimeError('無法儲存結果')
print('saved:', output.name)
