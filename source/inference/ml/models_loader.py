# models_loader.py
from ultralytics import YOLO


# Грузим модель один раз (оптимально)
def load_ppe_detect_model():
	model_path = "models/yolov8_detect_ppe_nano.pt"
	yolo_model = YOLO(model_path)
	return yolo_model


def load_worker_detect_model():
	model_path = "models/yolov8n.pt"
	yolo_model = YOLO(model_path)
	return yolo_model
