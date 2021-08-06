# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

from typing import Iterable, Tuple

import numpy as np
import os

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
		f"./scratch/{name}.wav")
	return data


def segments(vols: np.ndarray) -> Iterable[Tuple[int, int]]:
	limit = heuristics.min_of_max(vols)
	segs = []
	
	start, end = 0, 0
	itr = enumerate(vols)
	for i, vol in itr:
		# iterate to find the beginning of a quiet segment
		while vol >= limit:
			i, vol = next(itr, (0, float("-inf")))
		start = i
			
		# iterate to find the end of the quiet segment
		while vol < limit:
			i, vol = next(itr, (0, float("inf")))
		
		# sensitivity; only consider the segment if long
		if i - start >= FPS:
			if start - end >= 2 * FPS:
				segs.append((end, start))
			end = i
	
	return segs

def optimize(fname: str) -> None:
	vols = audiostream(fname)
	seg = segments(vols)
	bws = [TS.format(start=round(i[0]/FPS, 3), stop=round(i[1]/FPS, 3) + 1) for i in seg]
	# print(CMD.format(bw="+".join(bws), vid=fname), file=open("bruh", "w"))
	os.system(CMD.format(bw="+".join(bws), vid=fname))


def optimize_files(*fnames: str) -> None:
	pass