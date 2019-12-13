from unittest import TestCase
import librosa
import os

os.chdir('../../')

from Services.FeatureEngineering.FeatureEngineering import load_data

class test_FeatureEngineering(TestCase):

    def test_downsampling(self):
        y, s = librosa.load('clap.wav', sr=500)

        librosa.output.write_wav('kick_down.wav', y, s)

        name = ''


    def test_load_data(self):
        location = ''
        data = load_data(location)

        name = ''


