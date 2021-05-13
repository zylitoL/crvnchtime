# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple
import heuristics
import numpy as np

def audiostream(fname: str) -> np.ndarray:
    pass

def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
    pass

def optimize(fname: str) -> None:
    pass

def optimize_files(*fnames: str) -> None:
    pass
