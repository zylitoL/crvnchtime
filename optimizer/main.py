# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple

import numpy as np
import wave
import os
import pandas as pd


import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io
import heuristics


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

	filepointer = wave.open(
		"./{fname:}.wav".format(fname=name_without_extension), "rb")
	#filewave = filepointer.readframes(10)

	samplerate, data = wavfile.read(
		"./{fname:}.wav".format(fname=name_without_extension))
	sample = data / 32768.0
	altered = sample[:, 1]
	complete = np.absolute(altered)

	return complete


def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
	lower = heuristics.min_of_max(vols)

	
	
	gaps = []
	i = 0
	start = 0

	print(vols.size)
	while i < vols.size:
		
		while i < vols.size and vols[i] > lower :
			
			i += 1
		
		gaps.append((start, i))
		while i < vols.size and vols[i] < lower:
			
			i = i + 1
			
		start = i
		i = i + 1

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
	print(seg)
	CMD = """ffmpeg -i {vid} -vf "select='{bw}', setpts=N/FRAME_RATE/TB" -af "aselect='{bw}', asetpts=N/SR/TB" out.mp4"""
	TS = "between(t, {start}, {stop})"
	bws = [TS.format(start=i[0]/44100, stop=i[1]/44100) for i in seg]
	os.system(CMD.format(bw="+".join(bws), vid=name))


def optimize_files(*fnames: str) -> None:
	pass


optimize("yeet.mp4")
