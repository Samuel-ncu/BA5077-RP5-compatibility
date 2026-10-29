import cv2
import numpy as np

net = cv2.dnn.readNet('frozen_east_text_detection.pb')
image = np.zeros((320, 320, 3), dtype=np.uint8)
blob = cv2.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
scores, geometry = net.forward(['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3'])
print('scores shape', scores.shape)
print('geometry shape', geometry.shape)
