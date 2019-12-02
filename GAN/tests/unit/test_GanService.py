from unittest import TestCase
import os
import numpy as np
import soundfile as sf
import tensorflow as tf

from Services.GanService import GanService
from Services.FeatureEngineering.FeatureEngineering import load_data

os.chdir('../../')

class test_GanService(TestCase):

    def setUp(self):
        #self.service = GanService()
        name = ''
    def test_init(self):
        self.assertTrue(self.service)

    def test_real_audio_batch_size(self):
        self.service.train()



        name = ''

    def save_wav(self, wav, path):
        sf.write(path, wav, 16000, subtype='PCM_16')  # 16000 sample rate


    def test_test(self):
        z = tf.random.uniform([64, 100], -1., 1., dtype=tf.float32)

        name = ''

    def test_run_training(self):
        gan = GanService()

        #gan.train(epochs=10)


    def test_math(self):
        size = 660
        batch = 128

        print(int(660/128))

    def test_load_data(self):
        res = load_data(1, 1)
        tmp = len(res)
        name = ''




