from unittest import TestCase
import os

os.chdir('../../')

from Services.loader_service import decode_extract_and_batch, decode_audio

class test_loaderService(TestCase):

    def test_decode_extract_list(self):
        fps_list = ['./tmp/WRLD-KICK-1-D.wav']

    def test_decode_audio(self):
        path = './tmp/WRLD-KICK-1-D.wav'

        wav = decode_audio(path, normalize=True)

        name = ''
