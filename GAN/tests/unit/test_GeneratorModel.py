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
import noisereduce as nr


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
        # 16 is the half of batch size 32
        noise = np.random.normal(0, 100, (16, 100))
        images = self.generator.generate_sound(noise, training=False)
        first = images[0]

        # self.save_wav(first, './tmp/new_sound.wav')

        self.assertEqual(len(first), 16000)

    def test_version(self):
        print(tf.__version__)


    def test_load_model(self):

        g_location = './tmp/generator_1.h5'
        wav_location = './tmp/sample.wav'
        noise = np.random.normal(0, 1, (1, 500))

        generator = load_model(g_location)

        flat_sound = generator.predict(noise).flatten()
        sound = generator.predict(noise)

        print(generator.summary())

        sf.write(wav_location, flat_sound, 16000, subtype='PCM_16')

        name = ''


    def test_generator_v3(self):

        model = ""


    def test_noise_reducer(self):

        data, r = librosa.load('./tmp/sample.wav', 16000)

        # perform noise reduction
        reduced_noise = nr.reduce_noise(audio_clip=data, verbose=False, noise_clip=data[:])

        sf.write('./tmp/reduced_noise.wav', reduced_noise, 16000, subtype='PCM_16')

        name = ''















