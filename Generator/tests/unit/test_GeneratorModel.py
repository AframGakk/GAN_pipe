from unittest import TestCase
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


#from utils import audio_tools as audio

from Models.GeneratorModel import GeneratorModel

os.chdir('../../')


class test_GeneratorModel(TestCase):

    def setUp(self):
        self.generator = GeneratorModel()

    def test_init(self):
        self.assertTrue(self.generator)

    def test_images_should_be_16(self):
        # 16 is the half of batch size 32
        noise = np.random.normal(0, 100, (16, 100))
        images = self.generator.generate_sound(noise, training=False)

        self.assertEqual(images.shape[0], 16)

    def test_generate_sound_be_16000hz(self):
        # 16 is the half of batch size 32
        noise = np.random.normal(0, 100, (16, 100))
        images = self.generator.generate_sound(noise, training=False)
        first = images[0]

        # self.save_wav(first, './tmp/new_sound.wav')

        self.assertEqual(len(first), 16000)



