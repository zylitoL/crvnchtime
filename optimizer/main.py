# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple
import heuristics
import numpy as np

def audiostream(fname: str) -> np.array[float]:
    pass

def segments(vols: np.array[float]) -> Iterable[Tuple[int, int]]:
    pass

def optimize(fname: str) -> None:
    pass

def optimize_files(*fnames: str) -> None:
    pass