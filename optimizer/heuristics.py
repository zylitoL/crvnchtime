# -*- coding: utf-8 -*-

"""Contains heuristics to determine volume threshholds of non-speaking volumes.
Heuristics are functions on audio streams that return a volume to which all
portions of an audio segment that have a larger volume are likely to contain
speech.
The first argument of all heuristics is an audiostream. This is typically a
numpy array of volumes, but can be any iterable.
	Typical usage example:
	vol = min_of_max(audiostream)
"""

import random
import pandas as pd
import numpy as np

def min_of_max(vols: np.ndarray, obs: int=100, samples: int=1000) -> float:
	"""
	Given an audiostream, finds minimum of all sample maximums.
	Parameters
	----------
	vols : np.array
		An audio stream.
	obs: int
		Number of observations per sample. The default is 100.
	samples: int
		Number of samples. The default is 1000.
	
	Returns
	-------
	float
		Volume threshold.
	"""

	## TODO: Rewrite this!
	return min(
		[
			max([vols[random.randrange(len(vols))] for j in range(obs)]) for i in range(samples)
		]
	)

def lower_modes(vols: np.ndarray, modes: int=2, bins: int=100) -> float:
	"""
	Given an audiostream, finds the left cutoff of the minimum of the x most
	frequent modes.
	Parameters
	----------
	vols : np.array
		An audio stream.
	modes: int
		Number of most frequent modes to consider. The default is 2.
	cuts: int
		Number of bins. The default is 100.
	
	Returns
	-------
	float
		Volume threshold.
	"""
	## TODO: Write this. You may want to consider looking at other libraries
	## TODO: histogram/binning functions.

	## TODO: Create bins/histograms

	## TODO: Find the x most frequent.

	## TODO: Return the left cutoff of the smallest bin
	split_bin = np.arange(0,1, 1 / bins)
	
	split_labels = np.arange(0,bins-1)
	
	###bin_indicies = np.digitalize(vols, split_bin)

	myDF = pd.DataFrame({"Volume":vols})
	
	myDF["binned"] = pd.cut(x=myDF["Volume"], bins=split_bin)
	myDF["bin_level"] = pd.cut(x = myDF["Volume"],bins = split_bin, labels = split_labels)
	values = myDF.loc[:,"bin_level"]
	values = list(dict.fromkeys(values))
	values.sort()
	
	hold = 0
	for i in range(modes):
		
		if hold < values[i]:
			
			hold = values[i]

	
	return hold*(1/bins)

    
def volportion(vols: np.ndarray) -> np.ndarray:
	lower = lower_modes(vols)
	myDF = pd.DataFrame({"Volume":vols})

	myDF["add"] = np.where(myDF["Volume"]>lower, True, False)
	values = myDF.loc[:,"add"]
	
	return values
