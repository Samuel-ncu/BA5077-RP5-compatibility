import numpy as np
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path='mobilenet.tflite')
interpreter.allocate_tensors()
input_info = interpreter.get_input_details()[0]
output_info = interpreter.get_output_details()[0]
interpreter.set_tensor(input_info['index'], np.zeros(input_info['shape'], dtype=input_info['dtype']))
interpreter.invoke()
print('input shape', tuple(input_info['shape']))
print('output shape', interpreter.get_tensor(output_info['index']).shape)
