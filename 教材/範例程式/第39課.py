from ultralytics import YOLO

model = YOLO('yolov8n.pt')
print('class count', len(model.names))
print('class 0', model.names[0])
