# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple
import heuristics
import numpy as np
import wave
import os


import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io

def audiostream(fname: str) -> np.ndarray:
    abs_file_path = os.path.abspath(fname)
    name = os.path.basename(abs_file_path)
    name_without_extension = name.split(".")[0]

    print(name)
    print(abs_file_path)

    print("Obtaining audio stream")
    os.system("ffmpeg -hide_banner -loglevel warning -i {fpath} -vn -acodec pcm_s16le -ar 44100 -ac 2 ./{out:}.wav".format(
			fpath=abs_file_path,
			out=name_without_extension
	))

    filepointer = wave.open("./{fname:}.wav".format(fname=name_without_extension), "rb")
    #filewave = filepointer.readframes(10)
    
    samplerate, data = wavfile.read("./{fname:}.wav".format(fname=name_without_extension))
    sample = data / 32768.0
    altered = sample[:,1]
    complete = np.absolute(altered)
    plt.plot(complete)
    plt.show()
    return complete


def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
    pass


def optimize(fname: str) -> None:
    pass


def optimize_files(*fnames: str) -> None:
    pass


