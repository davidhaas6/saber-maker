import madmom
import numpy as np


class SpectrogramProcessor(madmom.processors.SequentialProcessor):
    SAMPLE_RATE_HZ = 44100
    FRAMES_PER_SECOND = 100

    def __init__(self, window_size_ms, formatted=False, fps=FRAMES_PER_SECOND,
                 sample_rate=SAMPLE_RATE_HZ, context_frames=7):

        win_size_samples = int(sample_rate * (window_size_ms/1000))

        # Read signal in and compute STFT
        fs = madmom.audio.signal.FramedSignalProcessor(
            frame_size=win_size_samples, fps=fps, num_channels=1
        )
        stft = madmom.audio.stft.STFTProcessor()

        # generate filtered spectrogram using mel scale and scale logarithmically
        # to approximate human perception of frequencies
        filt_spec = madmom.audio.spectrogram.FilteredSpectrogramProcessor(
            filterbank=madmom.audio.filters.MelFilterbank,
            num_bands=80, fmin=27.5, fmax=16000
        )
        log_spec = madmom.audio.spectrogram.LogarithmicSpectrogramProcessor(
            add=1
        )

        # Normalize frequency bands to zero mean and unit variance
        def normalize(spec):
            # REVIEW: Is this how you accomplish this goal?
            norm_spec = spec - np.mean(spec)  # zero mean
            norm_spec /= np.std(norm_spec)    # zero unit variance
            return norm_spec

        # sequentially process everything
        pipeline = [fs, stft, filt_spec, log_spec, normalize]

        if formatted:
            def format_spec_data(spectrogram):
                padding_format = ((context_frames, context_frames), (0, 0))
                pad_spec = np.pad(
                    spectrogram, padding_format,
                    'constant', constant_values=0
                )
                segmented = madmom.utils.segment_axis(
                    pad_spec, frame_size=(context_frames*2 + 1),
                    hop_size=1, axis=0, end='pad', end_value=0
                )

                # Swapped rows and columns and added a channel to fit keras data input requirements
                swapped = segmented.swapaxes(1, 2)[..., np.newaxis]
                return swapped

            pipeline.append(format_spec_data)

        super(SpectrogramProcessor, self).__init__(pipeline)
