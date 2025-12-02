# person_bbox.py
# Detect people on a photo and print bounding boxes (x1, y1, x2, y2).
# Uses Ultralytics YOLOv8 (PyTorch under the hood).

import sys
from pathlib import Path

import cv2
from ultralytics import YOLO  # type: ignore


def show_fit(win, img, max_w=1280, max_h=720):
	h, w = img.shape[:2]
	scale = min(max_w / w, max_h / h, 1.0)  # не увеличиваем, только уменьшаем
	if scale < 1.0:
		img = cv2.resize(
			img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
		)
	cv2.imshow(win, img)


def detect_people_bboxes(
	image_bgr, weights="yolov8s.pt", conf=0.35, iou=0.5, device=None
):
	"""
	Returns: list of dicts: {"bbox": [x1,y1,x2,y2], "conf": float}
	COCO class id for 'person' is 0.
	"""
	model = YOLO(weights)

	image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
	result = model.predict(
		source=image_rgb,
		conf=conf,
		iou=iou,
		device=device,  # "cpu", "cuda:0", etc. (or None -> auto)
		verbose=False,
	)[0]

	out = []
	if result.boxes is None:
		return out

	for b in result.boxes:
		cls_id = int(b.cls[0].item())
		if cls_id != 0:  # keep only "person"
			continue
		x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
		score = float(b.conf[0].item())
		out.append({"bbox": [int(x1), int(y1), int(x2), int(y2)], "conf": score})
	return out


def main():
	if len(sys.argv) < 2:
		print("Usage: python person_bbox.py path/to/image.jpg [--draw]")
		sys.exit(2)

	img_path = Path(sys.argv[1])
	draw = "--draw" in sys.argv[2:]

	img = cv2.imread(str(img_path))
	if img is None:
		raise FileNotFoundError(f"Cannot read image: {img_path}")

	detections = detect_people_bboxes(img, weights="yolov8s.pt", conf=0.35)
	# Print bboxes
	for d in detections:
		x1, y1, x2, y2 = d["bbox"]
		print(f"bbox={x1,y1,x2,y2} conf={d['conf']:.3f}")

	if draw:
		win = "people"
		cv2.namedWindow(win, cv2.WINDOW_NORMAL)  # окно можно растягивать

		vis = img.copy()
		for d in detections:
			x1, y1, x2, y2 = d["bbox"]
			cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)

		show_fit(win, vis)  # подгон под экран
		cv2.waitKey(0)
		cv2.destroyAllWindows()


if __name__ == "__main__":
	main()

# python .\source\inference\person_detector.py .\source\inference\ae09d1dab98e3ffcf18e76a50247c3ae.jpg --draw
