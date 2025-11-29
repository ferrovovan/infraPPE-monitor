# inference_source.py

# Источник внешних функций, как
#  обработка каждого кадра, взятие кадра.
# То есть механизмы _вне_ Steamlit.

from source.data.load_video import frame_generator as _frame_generator
from source.data.load_video import ir_frame_generator as _ir_frame_generator
from source.inference.ppe_detector import detect_ppe as _detect_ppe

ir_frame_generator = _ir_frame_generator
frame_generator = _frame_generator
#
run_inference = _detect_ppe
