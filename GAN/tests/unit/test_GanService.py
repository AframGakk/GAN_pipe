from unittest import TestCase
import os
import numpy as np
import soundfile as sf

from Services.GanService import GanService

os.chdir('../../')

class test_GanService(TestCase):

    def setUp(self):
        self.service = GanService()

    def test_init(self):
        self.assertTrue(self.service)

    def test_real_audio_batch_size(self):
        self.service.train()



        name = ''

    def save_wav(self, wav, path):
        sf.write(path, wav, 16000, subtype='PCM_16')  # 16000 sample rate

