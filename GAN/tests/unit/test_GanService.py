from unittest import TestCase
import os
import numpy as np
import soundfile as sf
import tensorflow as tf

#from Services.GanService import GanService

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