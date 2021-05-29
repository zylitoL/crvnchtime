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
    lower = lower_modes(vols)
    myDF = pd.DataFrame({"Volume":vols})
    myDF["add"] = np.where(myDF["Volume"]>lower, True, False)
    values = myDF.loc[:,"add"]

    gaps = []
    i = 0
    start = 0
    while i < values.size:
            while i < values.size and vols[i] >= vol:
                    i += 1
            start = i

            while i < size and vols[i] < vol:
                    i += 1
            if i - start >= 44100:
                    gaps.append((start, i))   
    return gaps 
    

def timestamp(seconds: int) -> str:
		hours = int(seconds) // 3600
		seconds -= hours * 3600
		minutes = int(seconds) // 60
		seconds -= minutes * 60
		seconds = round(seconds, 3)
		return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + "%06.3f" % seconds

def optimize(fname: str) -> None:
    volume = audiostream(fname)
    start = 0
    abs_file_path = os.path.abspath(fname)
    name = os.path.basename(abs_file_path)
    name_without_extension = name.split(".")[0]
    seg = segments(volume)
    split_cmd = "ffmpeg -hide_banner -loglevel warning -ss {start} -i ./{name}.mp4 -to {end} -async 1 ./{filename}"
    fout = open("./files.txt", "w")
    print("EXTRACTING")
    c = 0
    for i in range(len(seg)):
        start = seg[i][0]
        print(start / 44100.0, timestamp(start / 44100.0))
        print(timestamp(seg[i][0]-start) / 44100.0), timestamp((seg[i][1]) / 44100.0)
        os.system(split_cmd.format(start=timestamp(start / 44100.0), end=timestamp(seg[i][1] / 44100.0 - start / 44100.0), filename="segment{}.mp4".format(c), name=name_without_extension))
        fout.write("file segment{}.mp4\n".format(c))
        c += 1
        start = gaps[i][1]
    fout.close()
    os.system("ffmpeg -f concat -i ./files.txt -c copy ./merged.mp4")


def optimize_files(*fnames: str) -> None:
    pass

