from unittest import TestCase
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import tensorflow as tf
from keras.models import load_model
import soundfile as sf


#from utils import audio_tools as audio

from Models.GeneratorModel import GeneratorModel
from Models.GeneratorModel import GenModel

os.chdir('../../')


class test_GeneratorModel(TestCase):


    def test_init(self):

        g = GeneratorModel()
        #self.assertTrue(self.generator)
        print(g.model.summary())
        name = ''

    def test_init_2(self):

        g = GenModel()
        print(g.model.summary)
        #self.assertTrue(self.generator)

    def test_images_should_be_16(self):
        # 16 is the half of batch size 32
        generator = GenModel()
        noise = np.random.normal(0, 100, (16, 100))
        #images = generator.generate_sound(noise, training=False)

        #self.assertEqual(images.shape[0], 16)

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

        g_location = './tmp/model.h5'
        wav_location = './tmp/sample.wav'
        noise = np.random.normal(0, 1, (1, 100))

        generator = load_model(g_location)

        sound = generator.predict(noise)

        print(generator.summary())

        sf.write(wav_location, sound[0], 16000, subtype='PCM_16')

        name = ''









