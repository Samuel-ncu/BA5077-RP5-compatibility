import cv2
import numpy as np

def detect_text(net, image, threshold=0.5):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    scores, geometry = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])
    rectangles, confidences = [], []
    for y in range(scores.shape[2]):
        for x in range(scores.shape[3]):
            score = float(scores[0, 0, y, x])
            if score < threshold:
                continue
            x0, x1, x2, x3 = (geometry[0, i, y, x] for i in range(4))
            angle = geometry[0, 4, y, x]
            h, w = float(x0 + x2), float(x1 + x3)
            end_x = x * 4.0 + np.cos(angle) * x1 + np.sin(angle) * x2
            end_y = y * 4.0 - np.sin(angle) * x1 + np.cos(angle) * x2
            rectangles.append([int(end_x-w), int(end_y-h), int(w), int(h)])
            confidences.append(score)
    if not rectangles:
        return []
    indices = cv2.dnn.NMSBoxes(rectangles, confidences, threshold, 0.4)
    boxes = []
    for index in np.asarray(indices).flatten():
        x, y, w, h = rectangles[int(index)]
        x1 = max(0, int(x * width / 320))
        y1 = max(0, int(y * height / 320))
        x2 = min(width, int((x+w) * width / 320))
        y2 = min(height, int((y+h) * height / 320))
        if x2 > x1 and y2 > y1:
            boxes.append((x1, y1, x2, y2))
    return boxes
