#!/usr/bin/env python3

import madmom
import numpy as np
import matplotlib.pyplot as pyplot

SAMPLE_RATE_HZ = 44100
FRAME_TIME_MS = 150
# HOP_TIME_MS = 10 # equivalent to the stride from dance dance convolution
FRAMES_PER_SECOND = 100

def mono_signal(audio_fpath):
    signal = madmom.audio.signal.Signal(audio_fpath)
    return signal

def stereo_signal(audio_fpath):
    stereo = madmom.audio.signal.Signal(audio_fpath)
    return stereo

def frame_signal(signal):
    # hop_size = float(signal.sample_rate) / (float(1000) / float(STRIDE_TIME_MS)) # hop_size can be floating point for madmom
    frame_size = int(signal.sample_rate / (1000 / FRAME_TIME_MS))
    fs = madmom.audio.signal.FramedSignal(signal, frame_size=frame_size, fps=FRAMES_PER_SECOND)
    return fs

def fourier(framed_signal):
    transformed = madmom.audio.stft.STFT(framed_signal)
    return transformed

def __display_spectrogram(transformed_signal):
    spectrogram = madmom.audio.spectrogram.Spectrogram(transformed_signal)
    pyplot.imshow(spectrogram[:, :FRAMES_PER_SECOND].T, aspect='auto', origin='lower')
    pyplot.show()

'''
Builds a functor that accepts a filepath and returns the preprocessed data
'''
def mono_signal_processor():
    frame_size = int(SAMPLE_RATE_HZ / (1000 / FRAME_TIME_MS))
    signal_reader = madmom.audio.signal.SignalProcessor(num_channels=1, sample_rate=SAMPLE_RATE_HZ)
    frame_builder = madmom.audio.signal.FramedSignalProcessor(frame_size=frame_size, fps=FRAMES_PER_SECOND)
    stft = madmom.audio.stft.ShortTimeFourierTransformProcessor()
    mel_filter = madmom.audio.spectrogram.LogarithmicFilteredSpectrogramProcessor(num_bands=80, log=np.log, fmin=27.5, fmax=16000,
        filterbank=madmom.audio.filters.MelFilterbank)
    # the example I'm working off of also specified a value for LogarithmicFilt...Processor(add=EPSILON)
    # I don't understand the what/why it's there, so I left it out for now

    return madmom.processors.SequentialProcessor([signal_reader, frame_builder, stft, mel_filter])

def old_version():
    # grab the raw audio file data
    signal = mono_signal('examples/audio/haraiya-single.ogg')
    # group it into frames of FRAME_TIME_MS in length, with FRAMES_PER_SECOND as a rate
    fs = frame_signal(signal)
    # get a short-time fourier transform of the framed signal
    stft = fourier(fs)
    __display_spectrogram(stft)

    # stereo = stereo_signal('examples/audio/haraiya.ogg')
    print(signal)

if __name__ == '__main__':
    preprocessor = mono_signal_processor()
    output = preprocessor('examples/audio/haraiya-single.ogg')
    __display_spectrogram(output)
    print(output)
