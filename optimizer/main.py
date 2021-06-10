# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple

import numpy as np
import os
import pandas as pd

from scipy.io import wavfile
import heuristics

FPS = 44100
ASTREAM_CMD = """ffmpeg -hide_banner -loglevel warning -i {fpath} -vn -acodec pcm_s16le -ar 44100 -ac 1 ./scratch/{out:}.wav"""
CMD = """ffmpeg -i {vid} -vf "select='{bw}', setpts=N/FRAME_RATE/TB" -af "aselect='{bw}', asetpts=N/SR/TB" out.mp4"""
TS = "between(t, {start}, {stop})"

def audiostream(fname: str) -> np.ndarray:
	# implicitly use only the first channel of amplitudes
	file = os.path.basename(fname)
	name = os.path.splitext(file)[0]

	print("Obtaining audio stream")
	
	os.system(ASTREAM_CMD.format(
		fpath=fname,
		out=name
	))

	_, data = wavfile.read(
		"./scratch/{}.wav".format(name))
	return np.absolute(data)


def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
	lower = heuristics.min_of_max(vols)
	gaps = []

	i = 0
	while i < len(vols):
		if vols[i] > lower or i < FPS:
			j = i + FPS
			while j < len(vols) and (vols[j] > lower or j <= FPS):
				j += 1
			gaps.append((i, j - 1))
			i = j
		i += 1

	return gaps, lower

def optimize(fname: str, fout: str="merge") -> None:
	# file = os.path.basename(fname)
	# name = os.path.splitext(file)[0]
	# vols = audiostream(fname)
	# # abs_file_path = os.path.abspath(fname)
	# # name = os.path.basename(abs_file_path)
	# # name_without_extension = name.split(".")[0]
	vols = audiostream(fname)
	seg, _ = segments(vols)
	bws = [TS.format(start=round(i[0]/FPS, 3), stop=round(i[1]/FPS, 3) + 1) for i in seg]
	print(CMD.format(bw="+".join(bws), vid=fname), file=open("bruh", "w"))
	os.system(CMD.format(bw="+".join(bws), vid=fname))


def optimize_files(*fnames: str) -> None:
	pass