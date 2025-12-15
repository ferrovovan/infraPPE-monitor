# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2025 ferrovovan
#
# bbox_types.py

from __future__ import annotations  # Делает аннотации строками до рантайма
from typing import TypedDict  # Optional нужен для совместимости
import numpy as np


# Python 3.9+ (Работает везде с future import)
class dBBox(TypedDict):
    x1: int
    y1: int
    x2: int
    y2: int
    conf: float | None 
    label: str | None


class Worker(TypedDict):
    id: int                    # порядковый номер
    bbox: dBBox                # личный bbox
    crop: np.ndarray           # вырез из кадра
    # Используем новый синтаксис для list[DBBox], он теперь работает
    ppe_rel: list[dBBox]       # относительные bbox PPE от классификатора
    ppe: list[dBBox]           # абсолютные bbox PPE
