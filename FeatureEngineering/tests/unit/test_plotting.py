from unittest import TestCase
import os
import pickle
import pandas as pd
from scipy.io import wavfile
import librosa
import numpy as np

os.chdir('../../')

from services.FeatureEngineeringService.FeatureEngineeringService import FeatureEngineeringService
from services.plots.plots import plot_audio, plot_mfcc_spectogram, plt_mfcc_signal
from Config.FeatureConfig import FeatureConfig

class test_plotting(TestCase):

    def setUp(self):
        self.fService = FeatureEngineeringService()

    def test_plot_audio(self):
        records = self.fService.getRecordDataframe('KICK', 1)
        config = FeatureConfig()
        input_length = config.sample_length

        first_loc = records['locations'][0]
        rate, data = wavfile.read(first_loc)

        plot_audio(data, save=True, filename='full_audio.png')
        plot_audio(data, frames=15000, save=True, filename=('scraped_audio.png'))

        data, sr = librosa.core.load(first_loc, sr=16000, res_type='kaiser_fast')

        if len(data) > input_length:
            max_offset = len(data) - input_length
            offset = np.random.randint(max_offset)
            data = data[offset:(input_length + offset)]
        else:
            if input_length > len(data):
                max_offset = input_length - len(data)
                offset = np.random.randint(max_offset)
            else:
                offset = 0
            data = np.pad(data, (offset, input_length - len(data) - offset), "constant")

        data = librosa.feature.mfcc(data, sr=config.sampling_rate, n_mfcc=config.mfcc_mels)
        #data = np.expand_dims(data, axis=-1)

        plot_mfcc_spectogram(data, sr)
        plt_mfcc_signal(data, frames=120, save=True, filename='first_four_mels.png')
        plt_mfcc_signal(data, save=True, filename='full_mfcc.png')

        name = ''





