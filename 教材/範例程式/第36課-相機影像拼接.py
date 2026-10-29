import cv2

first = cv2.imread('feature-board-a.png')
second = cv2.imread('feature-board-b.png')
if first is None or second is None:
    raise RuntimeError('請準備 feature-board-a.png 與 feature-board-b.png')
for label, mode in [('PANORAMA', cv2.Stitcher_PANORAMA), ('SCANS', cv2.Stitcher_SCANS)]:
    status, output = cv2.Stitcher_create(mode).stitch([first, second])
    print(label, 'status:', status)
    print(label, 'image produced:', output is not None)
    if output is not None:
        name = f'lesson36-camera-{label.lower()}.png'
        if not cv2.imwrite(name, output):
            raise RuntimeError('無法存檔')
        print('saved:', name, 'shape:', output.shape)
