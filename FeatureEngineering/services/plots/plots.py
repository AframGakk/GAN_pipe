import matplotlib.pyplot as plt
import numpy as np
import librosa.display



def plot_audio(audio, frames=None, save=False, filename=None):

    if frames:
        audio = audio[:frames]

    plt.figure(figsize=(16, 5))
    plt.plot(audio[:], '.')
    plt.plot(audio[:], '-')
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    plt.title('Raw Audio')
    if save:
        if not filename:
            filename = 'audio_plot.png'
        filelocation = './tmp/{}'.format(filename)
        plt.savefig(filelocation)
    plt.show()


def plot_mfcc_spectogram(data, sr):
    plt.title('MFCC spectogram')
    librosa.display.specshow(data, sr=sr, x_axis='time')
    plt.show()


def plt_mfcc_signal(data, frames=None, save=False, filename=None):
    data = data.flatten()

    if frames:
        data = data[:frames]

    plt.figure(figsize=(16, 5))
    plt.plot(data, '.')
    plt.plot(data, '-')
    plt.title('MFCC Mels')
    plt.xlabel('sample points')
    plt.ylabel('Amplitude')
    if save:
        if not filename:
            filename = 'mfcc_plot.png'
        filelocation = './tmp/{}'.format(filename)
        plt.savefig(filelocation)
    plt.show()
