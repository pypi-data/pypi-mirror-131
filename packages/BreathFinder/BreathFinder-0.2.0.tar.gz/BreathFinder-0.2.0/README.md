# BreathFinder

![screenshot](https://user-images.githubusercontent.com/7534594/120475771-4e89d300-c399-11eb-874a-619ffcb5b925.png)

---
A python3 module implemented an algorithm designed to locate individual breaths within a PSG using the thoracic RIP signal.
The algorithm was validated on a thoracic RIP signal that was sampled with 25hz sampling frequency. Currently, the algorithm is un-validated on any other sampling frequency.

The result of the evaluation was that this algorithm found around 94\% of breaths correctly, with only 5\% of predictions being false positives.

---

## Installation

```console
bla@bla:~$ git clone git@github.com:benedikthth/BreathFinder.git

bla@bla:~$ cd BreathFinder

bla@bla:~$ pip install -e .
```

Currently, the package is in development, and is not released on PiPy.
The installation was tested on an ubuntu 20 system.

## Usage

### Basic use case

The following use cases assume that you have loaded a thoracic RIP signal in the form of a python list into the variable `signal`, and that you stored the sampling frequency of the signal in the variable `sampling_frequency`.

```python
import BreathFinder as BF
breath_locations = BF.find_breaths(signal, sampling_freuency)
# output is a list of breaths in the format [start, duration]
# where start is the timestamp of the breath-start in seconds
# since the signal start, and duration is the
# duration of the breath in seconds.
# breath_locations = [[1, 2], ...]
```

### Run-time Estimation

The BreathFinder run time can be estimated using the `estimate_run_time` function.

```python
import BreathFinder as BF
et = BF.estimate_run_time(signal, sampling_frequency)
print(f'The algorithm is estimated to process this recording in {et/60} minutes')
```

This is just an estimation however, the algorithm may take more, or less time to locate the breaths within the signal.

### Parallelization

BreathFinder does not support multiprocessing as part of the package.
However, a potential workaround for that is to split the signal up into smaller segments, and process each segment individually.
The following code is a template for how to accomplish this, but there may still be some issues associated with this approach, as currently, this package does not support multiprocessing natively.

```python
import BreathFinder as BF
from multiprocessing import Pool
# calculate how many samples are in a 10 minute window
window_size = int(10*60*fs)
# split signal into 10 minute segments
# We prepare a list of (signal, sampling_frequency, offset)
# tuples, this is necessary in order to use multiprocessing correctly.
signals = [ (signal[i:i+window_size, fs, i)] for i in range(0, len(signal), window_size)]
# Define a function that handles a single signal segment
def map_BF(signal, fs, offset):
    # calculate the offset in seconds. 
    offset_seconds = offset/fs
    # run BF
    breaths = BF.find_breats(signal, fs)
    # fix offset for breaths
    breaths = [(b[0]+offset_seconds, b[1]) for b in breaths]
    return breaths

# use 4 processes
with Pool(4) as p:
    # This returns a list of lists containing individual breaths
    breaths_list_list = p.starmap(map_BF, signals)
# flatten the breaths list
breaths = [breath for breath_list in breaths_list_list for breath in breath_list]
# Now you might have issues with the fact that
# depending on how the signal is split up the 
# algorithm migth miss the first breath, last 
# breath, or both. It might be useful to include
# some seconds of overlap between the windows. 
# and then deal with the double-detections.
# For dealing with double detections, you can do the following:
breaths = BF.postprocess(breaths, signal, fs)
# This is not tested, and if you find that there 
# are issues with this approach, please let me know
```

---

## Contact information

If there are any issues with the installation, running the algorithm, or general questions, please send me a message at [b@spock.is](mailto:b@spock.is?subject=Issue%20With%20BreathFinder)
