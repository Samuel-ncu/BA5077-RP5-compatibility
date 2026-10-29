import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
interpreter = Interpreter(model_path='mobilenet.tflite')
interpreter.allocate_tensors()
input_info = interpreter.get_input_details()[0]
image = cv2.resize(frame, (224, 224)).astype(input_info['dtype'])
interpreter.set_tensor(input_info['index'], np.expand_dims(image, axis=0))
interpreter.invoke()
output = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
print('camera frame', frame.shape)
print('output shape', output.shape)
