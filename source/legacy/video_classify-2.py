# source/inference/video_classify.py
import torch
import torchvision.transforms as transforms
from torchvision import models
# from PIL import Image
# import cv2
# import numpy as np
import os

# Путь к локальной модели
MODEL_PATH = os.path.join(
	os.path.dirname(__file__),
	"../../models/ppe_thermal_efficientnet_b0.pt"
)


@torch.no_grad()
def load_ppe_model():
	model = models.efficientnet_b0(pretrained=False)
	num_ftrs = model.classifier[1].in_features

	# helmet_yes/no, mask_yes/no
	model.classifier[1] = torch.nn.Linear(num_ftrs, 4)

	if not os.path.exists(MODEL_PATH):
		raise FileNotFoundError(f"Модель не найдена: {MODEL_PATH}")

	model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
	model.eval()
	return model


transform = transforms.Compose([
	transforms.Resize((224, 224)),
	transforms.ToTensor(),
	transforms.Normalize(
		mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
	),
])

model = load_ppe_model()


def predict_image(image_pil):
	img = image_pil.convert("RGB")
	img_tensor = transform(img).unsqueeze(0)

	outputs = model(img_tensor)
	probs = torch.sigmoid(outputs).squeeze(0)

	helmet_prob = probs[0].item()
	mask_prob = probs[2].item()

	has_helmet = helmet_prob > 0.5
	has_mask = mask_prob > 0.5

	return has_helmet, helmet_prob, has_mask, mask_prob
