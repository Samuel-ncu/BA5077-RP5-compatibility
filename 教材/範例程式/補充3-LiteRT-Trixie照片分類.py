from pathlib import Path
from importlib.metadata import version
import sys

import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter

folder = Path(__file__).resolve().parent
print("Python:", sys.version.split()[0])
print("LiteRT:", version("ai-edge-litert"))
print("OpenCV:", cv2.__version__)
print("NumPy:", np.__version__)

image = cv2.imread(str(folder / 'lesson24-camera-roi.png'))
if image is None:
    raise RuntimeError('找不到相機裁切圖 lesson24-camera-roi.png')
with open(folder / 'labels.txt', encoding='utf-8') as f:
    labels = [line.strip() for line in f]
interpreter = Interpreter(model_path=str(folder / 'mobilenet.tflite'))
interpreter.allocate_tensors()
input_info = interpreter.get_input_details()[0]
output_info = interpreter.get_output_details()[0]
print('input shape:', tuple(input_info['shape']))
print('input dtype:', input_info['dtype'].__name__)
print('input quantization:', input_info['quantization'])
print('output quantization:', output_info['quantization'])
if tuple(input_info['shape']) != (1, 224, 224, 3) or input_info['dtype'] != np.uint8:
    raise RuntimeError('此程式預期 MobileNetV1 量化模型的 uint8 224x224 RGB 輸入')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
rgb = cv2.resize(rgb, (224, 224))
interpreter.set_tensor(input_info['index'], np.expand_dims(rgb, axis=0))
interpreter.invoke()
raw = interpreter.get_tensor(output_info['index'])[0]
scale, zero = output_info['quantization']
scores = (raw.astype(np.float32) - zero) * scale
if len(labels) != len(scores):
    raise RuntimeError('標籤數與模型輸出數不一致')
for index in np.argsort(scores)[-3:][::-1]:
    print(f'top class: {index} {labels[index]} {scores[index]:.4f}')
