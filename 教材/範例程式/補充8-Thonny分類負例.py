import numpy as np
from tflite_runtime.interpreter import Interpreter

with open('labels.txt', encoding='utf-8') as f:
    labels = [line.strip() for line in f]
model = Interpreter(model_path='mobilenet.tflite')
model.allocate_tensors()
inp = model.get_input_details()[0]
out = model.get_output_details()[0]
if tuple(inp['shape']) != (1, 224, 224, 3) or inp['dtype'] != np.uint8:
    raise RuntimeError('需要 uint8 224x224 MobileNetV1')
if out['quantization'][0] <= 0:
    raise RuntimeError('模型輸出量化參數無效')
for pixel, name in [(0, 'black'), (255, 'white')]:
    model.set_tensor(inp['index'], np.full((1, 224, 224, 3), pixel, dtype=np.uint8))
    model.invoke()
    raw = model.get_tensor(out['index'])[0]
    scale, zero = out['quantization']
    scores = (raw.astype(np.float32) - zero) * scale
    if len(labels) != len(scores):
        raise RuntimeError('標籤數與輸出數不一致')
    i = int(np.argmax(scores))
    print(f'{name} blank: {i} {labels[i]} {scores[i]:.4f}')
