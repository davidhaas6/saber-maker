#!/usr/bin/env python3

import madmom
import numpy as np

SAMPLE_RATE_HZ = 44100
FRAMES_PER_SECOND = 100
STEP_SIZE = 1000 / FRAMES_PER_SECOND
CONTEXT_TIME_MS = 150


def __display_spectrogram(transformed_signal):
    spectrogram = madmom.audio.spectrogram.Spectrogram(transformed_signal)
    pyplot.imshow(spectrogram[:, :FRAMES_PER_SECOND].T,
                  aspect='auto', origin='lower')


'''
Builds a functor that accepts a filepath and returns the preprocessed data
'''


def mono_signal_processor(frame_time_ms):
    frame_size = int(SAMPLE_RATE_HZ / (1000 / frame_time_ms))
    signal_reader = madmom.audio.signal.SignalProcessor(
        num_channels=1, sample_rate=SAMPLE_RATE_HZ)
    fourier_frame_builder = madmom.audio.signal.FramedSignalProcessor(
        frame_size=frame_size, fps=FRAMES_PER_SECOND)  # framing for the fourier transform
    stft = madmom.audio.stft.ShortTimeFourierTransformProcessor()
    mel_filter = madmom.audio.spectrogram.LogarithmicFilteredSpectrogramProcessor(num_bands=80, log=np.log, fmin=27.5, fmax=16000,
                                                                                  filterbank=madmom.audio.filters.MelFilterbank)
    # the example I'm working off of also specified a value for LogarithmicFilt...Processor(add=EPSILON)
    # I don't understand the what/why it's there, so I left it out for now

    # frame into 150ms chunks
    context_builder = madmom.audio.signal.FramedSignalProcessor(
        frame_size=CONTEXT_TIME_MS/STEP_SIZE, hop_size=1)

    return madmom.processors.SequentialProcessor([signal_reader, fourier_frame_builder, stft, mel_filter, context_builder])


'''
The main entrypoint for this module. Returns a 4D matrix of the form [time x frames x mel-log]
'''


def preprocess_file(audio_fpath, *frame_sizes):
    outputs = []
    for i in range(len(frame_sizes)):
        pipeline = mono_signal_processor(frame_sizes[i])
        output = pipeline(audio_fpath)
        outputs.append(output)
    # this pipelining process builds a 4D matrix of the form [frames x time x mel-log]
    # transpose the first two dimensions so that we have [time x frames x mel-log]
    return np.transpose(outputs, [1, 0, 2, 3])


if __name__ == '__main__':
    import matplotlib.pyplot as pyplot  # only use plotting when running as main
    # frame_sizes = [23, 46, 93]
    # only use the one frame size since processing takes so long
    frame_sizes = [46]
    audio_fpath = 'examples/audio/haraiya.ogg'
    figure = pyplot.figure(figsize=(len(frame_sizes), 1))

    # this is basically the main entrypoint of the module
    outputs = preprocess_file(audio_fpath, *frame_sizes)

    for i in range(len(outputs)):
        figure.add_subplot(len(frame_sizes), 1, i + 1)
        __display_spectrogram(outputs[i])
    pyplot.show()
