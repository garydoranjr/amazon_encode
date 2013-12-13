#!/usr/bin/env python
import pylab as pl
import numpy as np
from scipy.io import wavfile
from scipy.misc import imresize
from PIL import Image, ImageDraw, ImageFont

def code_to_array(code):
    image = Image.new('L', (525,40), 0)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('FreeSans.ttf', 50)
    draw.text((10, -11), code, 255, font=font)
    img = np.array(image.getdata()).reshape(image.size, order='F').T
    return img

def freq_block(channels, seconds, samples=22050, fstart=1000, fstop=5000):
    bins = seconds*samples
    xx = np.vstack(channels*[np.linspace(0.0, float(seconds), bins)])
    freqs = np.column_stack(bins*[np.linspace(fstart, fstop, channels)])
    return np.flipud(np.sin(2*np.pi*np.multiply(xx, freqs)))

def encode(code, outputfile):
    code_array = code_to_array(code)
    #pl.imshow(code_array, cmap='gray', aspect='auto')
    #pl.show()
    #exit()

    freqs = freq_block(100, 10)
    code_scaled = imresize(code_array, freqs.shape)
    audio = np.multiply(freqs, code_scaled).mean(axis=0)
    audio /= np.max(np.abs(audio))
    wavfile.write(outputfile, 22050, np.array((2**15-1)*audio, dtype=np.int16))

if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(usage="Usage: %prog code outputfile.wav")

    options, args = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        exit()
    encode(*args)

