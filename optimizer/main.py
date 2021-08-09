# -*- coding: utf-8 -*-

"""Helper and driver functions for removing quiet portions of videos.
"""

import argparse
import os
import tkinter as tk
from tkinter import filedialog as fd
from typing import Iterable, Tuple

import numpy as np
from scipy.io import wavfile

import heuristics

FPS = 44100

def audiostream(fname: str) -> np.ndarray:
	# remove extension
	name = os.path.splitext(fname)[0]

	print("Obtaining audio stream")
	os.system(
		f"ffmpeg -hide_banner -loglevel warning -i {fname} -vn -acodec pcm_s16le -ar 44100 -ac 1 {name}.wav")

	_, data = wavfile.read(f"{name}.wav")
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

def optimize(infile: str, outfile: str) -> None:
	vols = audiostream(infile)
	seg = segments(vols)
	bws = "+".join([f"between(t, {round(start/FPS, 3)}, {round(end/FPS, 3)})" for start, end in seg])
	os.system(
		f"""ffmpeg -i {infile} -vf "select='{bws}', setpts=N/FRAME_RATE/TB" -af "aselect='{bws}', asetpts=N/SR/TB" {outfile}""")

def optimize_files(ins: Iterable[str], outs: Iterable[str]) -> None:
	for fin, fout in zip(ins, outs):
		optimize(fin, fout)

def main():
	parser = argparse.ArgumentParser(description="Program to remove quiet portions of videos.")
	parser.add_argument("--input", "-i", nargs="+", type=str, help="Input videos to compress")
	parser.add_argument("--output", "-o", nargs="+", type=str, help="Output filenames")
	args = parser.parse_args()

	# if no input files specified, open up a GUI
	if not args.input:
		root = tk.Tk()
		root.update()
		args.input = fd.askopenfilenames(title="Select videos to compress")
		root.update()
		root.destroy()
	
	# if output filenames specified, must be same length as input
	if args.output and len(args.input) != len(args.output):
		parser.error("argument --output/-o: must be same length as input or empty")
	
	# default output filenames is appending _cmpd
	if not args.output:
		args.output = [f"{os.path.splitext(fin)[0]}_cmpd.mp4" for fin in args.input]

	optimize_files(args.input, args.output)
		

if __name__ == "__main__":
	main()
