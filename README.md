# crvnchtime

A program to identify and remove non-speaking portions of videos.

Comprised of a standalone program (in `\optimizer`) that can apply a number of different heuristics to identify non-speaking volume threshholds, remove non-speaking segments and other functions in the command-line.

## Inspiration

A reimagining of [BLecOpS](https://github.com/shi428/blecop) in Python 3, with more planned volume heuristics and more features.

Lecture recordings contain numerous segments that are not useful to *watch*, such as the lecturer writing, walking, or thinking without any associated vocal commentary.
One can get around this inefficiency in one of two ways: speeding up the recording, or skipping around.
The former sacrifices intelligibility; for some lectures, going to x2 speed renders the video incomprehensible.
The latter is manual, and detracts from the viewer from completely concentrating on the video.
Further, this process is ad-hoc and requires much guessing on which portions will and will not contain useful information.
Should one have over 10 hours of lectures to watch, or even just more than 2, such options become infeasible.
An automatic procedure to determine and remove potentially unimportant parts saves both time and effort.

## Methodology

crvnchtime makes use of bootstrapping for a volume threshhold, either the quietest speaking volume or the loudest non-speaking noise volume (assumed to be quieter than the speaking volume) using one of multiple heuristics (see heuristics subsection).
With a video's audiostream using **TODO**, the program then identifies which sections of the video are important/unimportant, and then aggregates these into intervals.
Through [`ffmpeg`](https://ffmpeg.org/), the segments are then cropped and stitched into a compressed video file.

### Heuristics

`min_of_max` is the default bootstrapping algorithm from BLecOpS.
This takes multiple samples for a maximum volume, and then takes the minimum of these maximums.
By bootstrapping for the maximum, assuming speaking volume is the loudest source of noise in the video, we obtain values centered around the distribution of talking volumes.
Then to obtain the quitest speaking volume, we take the minimum of the samples.

~~`lower_modes` takes the histogram of volumes, and assumes of the multiple modes in the distribution, the largest (by volume) mode corresponds to a speaking volume, and hence all other modes correspond to non-speaking volumes such as background noise.
The threshhold is then the loudest volume from the lowest mode, corresponding to the loudest possible background noise.~~

## Installation

At the present, installing the `/optimizer` folder suffices.

## Usage

crvnchtime can be used both from a command line interface:
```
python crvnchtime.py -i Uncompressed.mp4
```
as a GUI, by running the file without arguments:
```
python main.py
```
and as a module directly:
```python
>>> import crvnchtime
>>> crvnchtime.optimize("Uncompressed.mp4", "compressed.mp4")
```
