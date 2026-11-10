from pathlib import Path

import cv2

folder = Path(__file__).resolve().parent
video = cv2.VideoCapture(str(folder / 'lesson16-camera.avi'))
ok, frame = video.read()
if not ok:
    video.release()
    raise RuntimeError('Cannot read lesson16-camera.avi')

# This box is for frame 1 of the supplied video only: x, y, width, height.
initial_box = (218, 127, 82, 88)
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, initial_box)
frames = 1
results = []
panels = []

def panel(image, box, number):
    image = image.copy()
    x, y, w, h = (int(value) for value in box)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, str(number), (20, 65), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2)
    return image

panels.append(panel(frame, initial_box, frames))
try:
    while True:
        ok, frame = video.read()
        if not ok:
            break
        frames += 1
        found, box = tracker.update(frame)
        box = tuple(int(value) for value in box)
        results.append((bool(found), box))
        if frames in (4, 8, 12) and found:
            panels.append(panel(frame, box, frames))
finally:
    video.release()

if len(panels) != 4:
    raise RuntimeError('Could not collect all four tracking panels')
output = folder / 'lesson25-video-csrt.png'
if not cv2.imwrite(str(output), cv2.vconcat([cv2.hconcat(panels[:2]), cv2.hconcat(panels[2:])])):
    raise RuntimeError('Could not save tracking result')
print('frames read:', frames)
print('successful updates:', sum(found for found, _ in results), '/', len(results))
print('first update:', results[0])
print('last update:', results[-1])
print('saved:', output.name)
