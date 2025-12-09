# inference_source.py

# Источник внешних функций, как
#  обработка каждого кадра, взятие кадра.
# То есть механизмы _вне_ Steamlit.

from source.data.load_video import frame_generator as _frame_generator  # noqa: F401
from source.data.load_video import ir_frame_generator as _ir_frame_generator  # noqa: F401
from source.inference.ppe_detector import detect_ppe as _detect_ppe  # noqa: F401
from source.inference.ppe_detector import ir_detect_ppe as _ir_detect_ppe  # noqa: F401
