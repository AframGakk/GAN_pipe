from unittest import TestCase
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import tensorflow as tf
from keras.models import load_model
import soundfile as sf
import librosa



#from utils import audio_tools as audio

from Models.GeneratorModel import GeneratorModel

os.chdir('../../')


class test_GeneratorModel(TestCase):


    def test_init(self):
        '''
        Should have output shape of 64000 equals to 4 seconds of 16 kHz file.
        :return:
        '''

        g = GeneratorModel()
        self.assertEqual(g.model.output_shape[1], 64000)



    def test_generate_sound_be_16000hz(self):
        g = GeneratorModel()
        wav_location = './tmp/sample_noise.wav'

        # 16 is the half of batch size 32
        noise = np.random.normal(-1, 1, (1, 500))
        images = g.model.predict(noise).flatten()

        # self.save_wav(first, './tmp/new_sound.wav')

        sf.write(wav_location, images, 16000, subtype='PCM_16')

    def test_version(self):
        print(tf.__version__)


    def test_load_model(self):

        g_location = './tmp/generator.h5'
        wav_location = './tmp/sample_second.wav'
        noise = np.random.normal(0, 1, (1, 100))

        generator = load_model(g_location)

        flat_sound = generator.predict(noise).flatten()
        sound = generator.predict(noise)

        print(generator.summary())

        sf.write(wav_location, flat_sound, 16000, subtype='PCM_16')

        name = ''


    def test_generator_v3(self):
        volume = 0.5  # range [0.0, 1.0]
        fs = 44100  # sampling rate, Hz, must be integer
        duration = 1.0  # in seconds, may be float
        f = 440.0
        g_location = './tmp/generator.h5'
        wav_location = './tmp/sample_sine.wav'

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(500) * f / fs)).astype(np.float32).flatten()


        generator = load_model(g_location)

        flat_sound = generator.predict(samples).flatten()

        sf.write(wav_location, flat_sound, 16000, subtype='PCM_16')

        model = ""


    def test_noise_reducer(self):

        data, r = librosa.load('./tmp/sample.wav', 16000)



        sf.write('./tmp/reduced_noise.wav', reduced_noise, 16000, subtype='PCM_16')

        name = ''















