# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple
import heuristics
import numpy as np


def audiostream(fname: str) -> np.ndarray:
    filepointer = wave.open(str, "rb")
    filewave = filepointer.readframes(-1)
    volume = np.frombuffer(filewave, dtype = 'int16')

    return volume


def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
    pass


def optimize(fname: str) -> None:
    pass


def optimize_files(*fnames: str) -> None:
    pass
