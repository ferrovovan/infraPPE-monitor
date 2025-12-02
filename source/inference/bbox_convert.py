from .bbox_types import dBBox

def convert_ppe_bboxes(ppe_rel: list[dBBox], worker_bbox: dBBox) -> list[dBBox]:
	abs_list = []
	for p in ppe_rel:
		ppe_abs_bbox = {
			"x1": worker_bbox["x1"] + p["x1"],
			"y1": worker_bbox["y1"] + p["y1"],
			"x2": worker_bbox["x1"] + p["x2"],
			"y2": worker_bbox["y1"] + p["y2"]
		}
		abs_list.append(ppe_abs_bbox)
	return abs_list

