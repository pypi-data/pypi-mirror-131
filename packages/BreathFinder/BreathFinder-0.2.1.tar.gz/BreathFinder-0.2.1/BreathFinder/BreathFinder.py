import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import savgol_filter
import scipy
import math

def move_overlaps(bss, signal, fs):
    '''Remove overlaps between breaths.

    Args:
        bss: List of raw BSS predictions.
        rip_signal: The signal.
        rip_sf: sampling frequency of the RIP signal.

    Returns:
        List of breath location estimates with no overlapping regions.
    '''
    print("Moving overlaps")
    new_bss = [bss[0]]

    for b in bss[1:]:
        # find last breath
        lb = new_bss[-1]
        # find current breath
        cb = b
        # Find the overlap amount.
        ocb = get_percentage_overlap(cb, lb)
        if ocb > 0:
            # find moment in time when overlap starts
            overlap_start = max(lb[0], cb[0])
            # find moment in time when overlap ends
            overlap_end = min(sum(lb[:2]), sum(cb[:2]))
            # extract the overlap region from the signal
            overlap_region = signal[int(overlap_start*fs):int(overlap_end*fs)]
            # If the region is empty, the breaths only overlap superficially
            if len(overlap_region) == 0:
                new_bss.append(cb)
                continue
            min_val_idx = np.argmax(overlap_region)
            # find the location in time when the breaths are seperated
            new_breath_sep = overlap_start + (min_val_idx / fs)
            # Find new duration of last breath
            nlbl = new_breath_sep - lb[0]
            # new current breath start
            ncbs = new_breath_sep
            # new current breath length
            ncbl = sum(cb[:2]) - new_breath_sep
            # delete last breath from new_bss
            new_bss = new_bss[:-1]
            # add the new breaths
            new_bss.append([lb[0], nlbl])
            new_bss.append([ncbs, ncbl])
        else:
            new_bss.append(cb)
    return new_bss



def get_percentage_overlap(b1, b2):
    '''Calculate the overlap duration of b1 and b2
    as a percentage of the length of b1.

    Args:
        b1: Span in the format [onset, length]
        b2: Span in the format [onset, length]

    Returns:
        The overlap duration as a percentage of cumulative duration length.
    '''
    l = b1[1]
    s = max(b1[0], b2[0])
    e = min(sum(b1[:2]), sum(b2[:2]))
    return max(0, (e-s)/l)


def subsume_overlaps(bss, thresh=0.8):
    '''Loop through all detected breaths, merge them if they
    occupy the same region.

    Args:
        bss: Raw result from BSS function
        thresh: Overlap threshold which is required to merge the breaths

    Returns:
        BSS, after duplicate breaths have been eliminated.

    '''
    #first breath does not overlap anything.
    new_bss = [bss[0]]
    for i in bss[1:]:
        # the last breath that does not overlap.
        lb = new_bss[-1]
        # the breath we are checking for overlap.
        cb = i
        # get how much of current breath overlaps with old one
        ocb = get_percentage_overlap(cb, lb)
        # if the current breath is completely overlapped in the last one,
        # skip the current breath.
        if ocb >= 0.99:
            continue
        # get how much of last breath is overlapped in the current one
        olb = get_percentage_overlap(lb, cb)
        # if the old breath is completely subsumed by the new one
        if olb >= 0.99:
            # the old breath is replaced by the new one.
            new_bss[-1] = [cb[0], cb[1]]
            continue
        # if this is true, then the breaths are merged.
        if olb >= thresh or ocb >= thresh:
            # the start of the breath is the first start.
            start = min(lb[0], cb[0])
            # the end is the later of the ends
            end = max(sum(lb[:2]), sum(cb[:2]))
            new_bss[-1] = [start, end-start]
            continue
        # if we got here, then the breaths do not significantly overlap.
        new_bss.append(cb)
    return new_bss


def postprocess(bss, signal, sf):
    '''Performs the post processing step of the algorithm:
    1) merge duplicate detections 2) Remove overlaps

    Args:
        bss: List of breaths in the format [onset, length]
        signal: Same signal as the BSS was performed on
        sf: Sampling frequency of the signal.

    Returns:
        The list of breaths after the post processing steps are complete.
    '''
    bss.sort(key=lambda x: x[0])
    bss = subsume_overlaps(bss)
    bss = move_overlaps(bss, signal, sf)
    return bss


def find_breaths(signal, sf):
    '''Locate individual breaths within the signal.
    This algorithm was evaluated on the thoracic RIP signal,
    but should in theory be applicable on the abdomenal
    RIP signal as well.

    Args:
        signal: Signal to perform the BSS on.
        sf: Sampling frequency of the signal.

    Returns:
        A list of breaths, in the format of [onset, duration]
        where onset is the start of the breath in seconds after
        the signal start.
    '''
    # for the purposes of this algorithm, a simple normal
    # distribution is sufficient to model the probablities of breath lenghts.
    pdf = scipy.stats.norm(3.53, 0.79).pdf

    # use the best BSS alg to calculate the bss
    bss = sine_fit_bss(signal, sf, length_pdf=pdf)

    bss = postprocess(bss, signal, sf)
    return bss

def smooth(signal, win_size=51):
    return savgol_filter(signal, win_size,3)

def de_trend(signal):
    '''Removes systematic slant from signal.

    Args:
        signal: signal window

    Returns:
        the signal window after removing trend.
    '''
    # linear regression needs a signal with [1,] dimension
    r = [[i] for i in range(len(signal))]
    # fit line to data
    model = LinearRegression().fit(r, signal)
    # subtract the trend from the data
    return [signal[i]-(((i * model.coef_[0]))) for i in range(len(signal))]


def get_breath_template(duration, sf=1):
    '''Generate a breath template with lenght of duration.

    Args:
        duration: the length of the breath being searched for.

    Returns:
        A signal containing one period sine, starting at -1
    '''
    try:
        p = 2 * math.pi / (duration * sf)
    except:
        raise Exception("Breathfinder tried to divide by zero")
        
    return [ math.sin( (i * p) + 1.5*math.pi ) for i in range(duration*sf)]


def acf_unbiased(window):
    '''Perform auto correlation on window

    Args:
        window: window to correlate against itself

    Returns:
        The auto correlation signal of the window
    '''
    ac = np.correlate(window,window,mode='full')
    ac = ac[len(window):]
    x = []
    for i in range(len( ac ) ):
        x.append( ac[i] * (len(ac) / ( len(ac) - i ) ) )
    return x


def sig_corr(window, sin):
    '''Use pearson cross correlation coefficient to correlate a breath
    template over a window.

    Args:
        window: The signal window to locate the breath in.
        sin:    The breath template

    Returns:
        the correlation coefficient of the breath template over
        the duration of the window
    '''
    return [np.corrcoef( window[i:(i+len(sin))], sin[:len(window)-i])[0,1]
        for i in range(len(window)-1)]


def skip(i, skip_amount, overlap):
    '''Calculates the distance the analysis window should move.

    Args:
        i: Current index of signal
        skip_amount: Where to place the new signal
        overlap:    How much of skip_amount should be
        included in the new window.

    Returns:
        the last position, and the new position.
    '''
    return i, max(i + int( skip_amount * (1-overlap)), i+1  )


def get_periodicity_candidates(window, length_pdf, sf):
    '''Find potential periodicity candidates in window.

    Args:
        window: signal window that you are trying to estimate the peridicity of
        length_pdf: Probability density estimation of breath lengths.
        sf: Sampling frequency of the signal in window.

    Returns:
        List of peaks in the auto correlation function of W in the format of
        [[peak, probability of peak]]
    '''
    # get the autocorrelation.
    autocorrelation = acf_unbiased(window)
    peaks = []
    # this returns the index of the peaks in the signal.
    peaks, _ = scipy.signal.find_peaks(np.array(autocorrelation))
    if len(peaks)==0:
        return []
    # transform peak-indices into seconds
    t_peaks = list(map(lambda x: x/sf, peaks))
    # transform t_peaks to probabilities.
    t_peaks = length_pdf(t_peaks)
    t_pairs = zip(peaks, t_peaks)
    return list(t_pairs)


def sine_fit_bss(signal, sampling_frequency, window_size=8,
                overlap=0.4, skip_overlap=0.95,
                correlation_threshold=0.75,
                probability_cutoff=0.0001, length_pdf=None):
    '''Perform the breath synchronous segmentation

    Args:
        signal: The thoracic RIP signal.
        sampling_frequency: sampling frequency.
        The rest of the parameters are optional.

    Returns:
        A list of raw breath position estimations.
    '''

    np.seterr(all='ignore')
    # calculate the number of samples per analytical window
    window_size = int(window_size * sampling_frequency)

    breaths = []
    i = 0
    last_i = -1

    # smooth the entire signal
    signal_smooth = smooth(signal, 11)

    while i < len(signal):
        # if the window length will be less than 4 seconds,
        # ignore the rest since we can't find the periodicity.
        if len(signal) - i < 4 * sampling_frequency:
            break
        # check if we have regressed, this will cause the algorithm to not halt.
        if i <= last_i:
            raise Exception('Last position',
                str(last_i), 'Was higher than current position',
                str(i) ,'in BSS, this may not halt')
        # extract the window
        window = signal[i: i +window_size]
        if np.std(window) == 0 or max(window) == min(window):
            last_i, i = skip(i, window_size, skip_overlap)
            continue
        # remove any slant from the window
        window = de_trend(window)
        smoothed_window = signal_smooth[i:i+window_size]#smooth(window, 4, 11)
        # find the Periodicity of the signal which corresponds to the
        # possible breath length.
        length_candidates = get_periodicity_candidates(window,
            length_pdf, sampling_frequency)
        found_breath = False
        # Remove all candidates that register as less probable than the
        # probability cutoff.
        length_candidates = list(filter(lambda x: x[1] > probability_cutoff,
            length_candidates))
        # Sort length candidates by probability increasing
        length_candidates.sort(key=lambda x: -x[1])
        start = None
        duration = None
        # Now, phase 2, Breath location estimation is started.
        for peak , _ in length_candidates:
            # create a sine starting at a minimum and has the same
            # periodicity as the breath we are searching for.
            breath_approximation = get_breath_template(peak, 1)
            # perform pearson-correlation on the smoothed window and the
            # breath sine.
            sine_correlation = sig_corr(smoothed_window, breath_approximation)
            # find peaks in correlation.
            sc_peaks, _ = scipy.signal.find_peaks(sine_correlation)
            # transform to list.
            sc_peaks = list(sc_peaks)
            if len(sc_peaks) == 0:
                continue
            # There is a possibility that the breath is starting at the very
            # beginnning of the signal.
            first_sample = sine_correlation[0]
            acf_increasing = sine_correlation[1] - sine_correlation[0] > 0
            # if the starting peak is greater than the the conf. threshold
            # insert it into the peaks.
            if first_sample > correlation_threshold and not acf_increasing:
                sc_peaks.insert(0, 0)
            # loop through our peaks.
            for p in sc_peaks:
                # find how positive the correlation is at peak p
                confidence = sine_correlation[p]
                # if the correlation is greater than the threshold,
                #  then we have found a breath!
                if confidence > correlation_threshold:
                    found_breath = True
                    # start is now the index of the sample
                    # in the window where the breath is found.
                    start = p
                    # duration is now the length of the breath,
                    #  or periodicity of the signal.
                    duration = peak
                    break
            # break from loop if a breath has been found.
            if found_breath:
                break
        # if we have found no breath in this window:
        # skip to the next analysis window.
        if not found_breath:
            last_i, i = skip(i, window_size, skip_overlap)
            continue

        # calculate approximation of end
        end = start + duration
        # the end we found is past the window, this will
        # result in an error, so rather lets reanalyze this part
        if end >= len(window):
            last_i, i = skip(i, start, skip_overlap)
            continue
        # this can happen when the signal is particularly noisy.
        if duration <= 0:
            last_i, i = skip(i, window_size, skip_overlap)
            continue
        # append the new breath to the breaths.
        #   the new breath has to be in seconds since the signal start.
        breaths.append([
            (i+start)/sampling_frequency,
            duration/sampling_frequency,
            sine_correlation[start]
        ])

        last_i, i = skip(i, start+duration, overlap)

        # check if our index has not progressed.
        if i <= last_i:
            raise Exception('Index has not progressed!')

    return breaths

def estimate_run_time(signal, sf):
    '''Calculates the projected time it takes for
    BreathFinder to execute on the given signal.

    Args:
        signal: The signal that BreathFinder should operate on
        sf: The sampling frequency of the signal.

    Returns:
        The projected execution time in seconds.
    '''
    d = len(signal)/sf
    return 5.83 * 0.003 * d + 1.83


if __name__ == '__main__':
    print('''Welcome to the BreathFinder library.
    this library implements the breath synchronous segmentation algorithm introduced in
    my master's thesis. Running this file itself will not do much.''')
