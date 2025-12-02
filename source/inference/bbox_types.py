import numpy as np

# Python 3.11
dBBox = dict(
	x1=int, y1=int,
	x2=int, y2=int,
	conf=float | None,
	label=str | None
)

Worker = dict(
	id=int,                    # порядковый номер
	bbox=dBBox,                # личный bbox
	crop=np.ndarray,           # вырез из кадра
	ppe_rel=list[dBBox],       # относительные bbox PPE от классификатора
	ppe=list[dBBox]            # абсолютные bbox PPE
)
