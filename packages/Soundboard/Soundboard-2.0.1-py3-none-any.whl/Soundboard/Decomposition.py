import numpy as np
import scipy.signal
from matplotlib import pyplot as plt

from Soundboard import *

def unmake(name):
    wav_file = wave.open(name + ".wav")
    nframes = wav_file.getnframes() * 16
    frames = wav_file.readframes(nframes)
    ticks = 0
    percent = -1
    string = ""
    for i in range(0,nframes,2):
        try:
            string += str(struct.unpack('h',bytes(frames[i-2:i]))[0])+"\n"
        except:
            pass
        ticks += 2
        if percent < math.floor(ticks / nframes * 100):
            percent = math.floor(ticks / nframes * 100)
            print("\rUncompiling: " + str(percent) + "%", end="")
    wav_file.close()
    build = open(name + ".sbld", "w")
    build.write(string)
    build.close()

def spectrum(name):
    file = open(name+".sbld","r")
    signal = []
    N = filesize(name + ".sbld")
    for i in range(N):
        signal.append(int(file.readline()[:-1])/DRANGE)
    return scipy.signal.spectrogram(np.array(signal), SAMPLERATE, nfft=2^16)

