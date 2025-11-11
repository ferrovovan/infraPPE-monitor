import cv2
import numpy as np

def rgb_to_ir(rgb_frame):
    """
    Простая заглушка для имитирования ИК-изображений
    """
    gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
    ir_sim = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
    return ir_sim

