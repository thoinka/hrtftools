'''HRTF Tools: Sweeps

2019, T. Hoinka <thoinka@gmail.com>
'''
import numpy as np
from scipy.io import wavfile
import click


def sweep(fmin, fmax, T, fs, log):
    t = np.linspace(0.0, T, int(fs * T))
    if log:
        b = np.log(fmax / fmin) / T
        phi = fmin * np.exp(b * t) / b
    else:
        b = (fmax - fmin) / T
        phi = fmin + b * t
    return np.sin(2.0 * np.pi * phi)


@click.command()
@click.option('--duration', type=float, default=5.0,
              help='Duration of the sweep in seconds.')
@click.option('--fmin', type=float, default=20.0,
              help='Minimum frequency in Hz.')
@click.option('--fmax', type=float, default=20000.0,
              help='Maximum frequency in Hz')
@click.option('--fs', type=int, default=44100,
              help='Sample rate in Hz.')
@click.option('--log/--lin', default=True,
              help='Whether to cast a logarithmic or linear sweep.')
@click.option('--stereo', is_flag=True, default=False,
              help='Whether or not to cast a stereo sweep.')
@click.option('--predelay', type=float, default=5.0,
              help='Predelay in seconds.')
@click.option('-o', '--output', type=str,
              help='Output path.')
def main(duration, fmin, fmax, fs, log, stereo, predelay, output):
    S = sweep(fmin, fmax, duration, fs, log)
    S_padded = np.hstack((np.zeros(int(fs * predelay)), S))
    S_padded = np.hstack((S_padded, S_padded))
    if stereo:
        out = (np.column_stack((
                   np.hstack((S_padded, np.zeros_like(S_padded))),
                   np.hstack((np.zeros_like(S_padded), S_padded))
               )) * 2 ** 15).astype('int16')
    else:
        out = (S_padded * 2 ** 15).astype('int16')
    wavfile.write(output, fs, out)

if __name__ == '__main__':
    main()