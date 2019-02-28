'''HRTF Tools: Process files
'''
import numpy as np
from numpy.fft import fft, ifft
import click
from scipy.io import wavfile


def convolve(x, kernel):
    '''This is a fast convolution that only works for kernels that are
    far smaller than the signal. The trick is to convolve the signal in parts
    that are each three times the size of the kernel.'''

    assert len(x) > len(kernel), 'Kernel size must be smaller than data size.'

    ksize = len(kernel)
    fft_kernel = fft(np.pad(kernel, (0, 2 * ksize), mode='constant'))
    N_ksizes = int(np.ceil(len(x) / ksize))
    nsize = int(ksize * N_ksizes)

    output = np.zeros(nsize)
    x = np.pad(x, (ksize, (nsize - len(x)) + ksize), mode='constant')

    for i in range(N_ksizes):
        chunk = x[i * ksize : (i + 3) * ksize]
        conv_chunk = ifft(fft(chunk) * fft_kernel)
        output[i * ksize:(i + 1)*ksize] = np.real(conv_chunk[ksize:2*ksize])
    return output


@click.command()
@click.option('-i', '--input', type=str, help='Input path.')
@click.option('-r', '--right', type=str, help='Path to right HRTF')
@click.option('-l', '--left', type=str, help='Path to left HRTF')
@click.option('-o', '--output', type=str, help='Output Path')
def main(input, right, left, output):
	fs, data = wavfile.read(input)
	_, left = wavfile.read(left)
	_, right = wavfile.read(right)
	norm = max([np.max(np.abs(left)), np.max(np.abs(right))])
	data_conv = np.column_stack((
		convolve(data[:,0], left[:,0] / norm) + convolve(data[:,1], right[:,0] / norm),
		convolve(data[:,0], left[:,1] / norm) + convolve(data[:,1], right[:,1] / norm),
	))
	out = (data_conv / np.max(np.abs(data_conv)) * 2 ** 15).astype('int16')
	wavfile.write(output, fs, out)


if __name__ == '__main__':
	main()