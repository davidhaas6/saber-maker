import sys
import numpy as np
import madmom
from madmom.audio.filters import MelFilterbank

# import the file
sys.path.insert(0, '../common/')
from audio_preprocessor import SpectrogramProcessor


def gen_spectrogram(window_size_ms, src):
    sig = madmom.audio.signal.Signal(src, num_channels=1)

    win_size_samples = int(sig.sample_rate * (window_size_ms/1000))

    fs = madmom.audio.signal.FramedSignal(sig, frame_size=win_size_samples, fps=100)
    stft = madmom.audio.stft.STFT(fs)

    filt_spec = madmom.audio.spectrogram.FilteredSpectrogram(stft, filterbank=MelFilterbank, num_bands=80, fmin=27.5, fmax=16000)

    log_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(filt_spec, add=1)
    norm_spec = log_spec - np.mean(log_spec)
    norm_spec /= np.std(norm_spec)

    num_context = 7
    padding_format = ((num_context, num_context), (0, 0))
    pad_spec = np.pad(norm_spec, padding_format, 'constant', constant_values=0)

    context_frames = [  pad_spec[i-num_context:i+num_context+1] 
                        for i, frame in enumerate(norm_spec, start=num_context)
                     ]
    return (norm_spec, context_frames)


# Test cases
def test(verbose=False):
    src = '../../examples/audio/haraiya-single.ogg'
    winsize = 46

    sp1 = SpectrogramProcessor(winsize, formatted=False)
    sp2 = SpectrogramProcessor(winsize, formatted=True)
    pspec_unformatted = sp1.process(src)
    pspec_formatted = sp2.process(src)

    norm_spec, context_frames = gen_spectrogram(winsize, src)

    if verbose:
        print(pspec_unformatted.shape)
        print(pspec_formatted.shape)
        print(norm_spec.shape)
        print(context_frames[0].shape)

    assert np.array_equal(norm_spec[0:15], context_frames[7])
    assert not np.array_equal(norm_spec[0:15], context_frames[8])

    assert np.array_equal(norm_spec[21756], pspec_unformatted[21756])
    assert np.array_equal(norm_spec[2176], pspec_unformatted[2176])
    assert not np.array_equal(norm_spec[21756], pspec_unformatted[216])

    assert pspec_formatted[100][1][2][0] == context_frames[100][2][1]
    return True

if __name__ == "__main__":
    if test(verbose=True):
        print("Audio Preprocessing Tests Passed")


