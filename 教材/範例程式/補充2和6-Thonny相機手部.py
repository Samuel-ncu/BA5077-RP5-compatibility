import time
from collections import Counter
import cv2
from picamera2 import Picamera2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=2, detectionCon=0.5)
camera = Picamera2()
counts = []
try:
    camera.configure(camera.create_preview_configuration(
        main={'size': (640, 480), 'format': 'RGB888'}))
    camera.start()
    time.sleep(1)
    start = time.perf_counter()
    while len(counts) < 50:
        frame = camera.capture_array()
        hands, shown = detector.findHands(frame, draw=True, flipType=False)
        counts.append(len(hands))
        cv2.imshow('CVZone camera - Q to stop', shown)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    elapsed = time.perf_counter() - start
    print('frames:', len(counts))
    print('hand count histogram:', dict(sorted(Counter(counts).items())))
    print('elapsed seconds:', round(elapsed, 2))
    print('average FPS:', round(len(counts) / elapsed, 2))
finally:
    camera.stop()
    camera.close()
    cv2.destroyAllWindows()
    print('camera released')
