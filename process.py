'''HRTF Tools: Deconvolver
'''

import numpy as np
from numpy.fft import rfft, irfft
import click
from scipy.io import wavfile
from sweep import sweep

@click.command()
@click.option('-i', '--input', type=str, help='Input path.')
@click.option('--duration', type=float, default=5.0,
              help='Duration of the sweep in seconds.')
@click.option('--fmin', type=float, default=20.0,
              help='Minimum frequency in Hz.')
@click.option('--fmax', type=float, default=20000.0,
              help='Maximum frequency in Hz')
@click.option('--predelay', type=float, default=5.0,
              help='Predelay in seconds.')
@click.option('--log/--lin', default=True,
              help='Whether to cast a logarithmic or linear sweep.')
@click.option('-o', '--output', type=str,
              help='Output path.')
@click.option('--window', type=int, default=16384,
              help='Length of the kernel. Increase if FIR is cut off.')
@click.option('--seek', type=int, default=128,
              help='Seek length used to crop the FIR. Set to 0 when automatic cropping does not seem to work.')
def main(input, duration, fmin, fmax, predelay, log, output, window, seek):
    fs, data = wavfile.read(input)

    # Deconvolution via fft
    S = sweep(fmin, fmax, duration, fs, log)
    S_padded = np.hstack((S, np.zeros(len(data) - len(S))))
    data_deconv = irfft(rfft(data) / rfft(S_padded))
    out = np.column_stack((
              data_deconv, np.roll(data_deconv,
                                   -int((predelay + duration) * fs))
          ))

    # Automagic window cropping by looking at the covariance of the channels.
    if seek >= 1:
        iterator = np.arange(0, len(data), seek)
        idx = np.argmax([np.cov(np.abs(out[i:i + seek, 0]),
                                np.abs(out[i:i + seek, 1]))[0, 1]
                         for i in iterator])
        idx_max = iterator[idx]
        cropped_out = out[idx_max - seek : idx_max - seek + window]
    else:
        cropped_out = out

    wavfile.write(output, fs, (cropped_out / np.max(np.abs(cropped_out))))


if __name__ == '__main__':
    main()