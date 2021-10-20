from unittest import TestCase

from Models.encoder import encoder
from Models.GeneratorModel import GeneratorModel
from Models.AutoEncoder import AutoEncoder
import librosa

class test_Encoder(TestCase):

    def test_encoder_build(self):
        y, s = librosa.load('clap.wav', sr=16000)



        e = encoder()

        g = GeneratorModel()

        auto = AutoEncoder(e, g)

        ret = auto.model.predict(y)

        librosa.output.write_wav('kick_down.wav', ret, s)
