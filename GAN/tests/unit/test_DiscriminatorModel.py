from unittest import TestCase
import numpy as np
import os
import librosa
import matplotlib.pyplot as plt

from Models.DiscriminatorModel import DiscriminatorModel, DiscrimModel, Discriminator_new

os.chdir('../../')

def plotWav(audio):
    plt.figure(figsize=(16, 5))
    plt.plot(audio[:], '.')
    plt.plot(audio[:], '-')
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    plt.title('Raw Audio')
    plt.show()

class test_DiscriminatorModel(TestCase):

    #def setUp(self):
    #    self.model = DiscriminatorModel()


    def test_init(self):
        '''
        the model can build!
        :return:
        '''
        model = DiscriminatorModel()


    def test_model_input_size_64000(self):
        '''
        the model has input size of 4 second file
        :return:
        '''
        model = DiscriminatorModel()
        self.assertEqual(model.model.input_shape[1], 64000)


    def test_kerasDiscrimi(self):
        input_length = 16384
        data, _ = librosa.core.load('./tmp/WRLD-KICK-1-D.wav', sr=16000, res_type='kaiser_fast')

        # Random offset / Padding
        if len(data) > input_length:
            max_offset = len(data) - input_length
            offset = np.random.randint(max_offset)
            data = data[:(input_length + offset)]
        else:
            if input_length > len(data):
                max_offset = input_length - len(data)
                offset = np.random.randint(max_offset)
            else:
                offset = 0

            data = np.pad(data, (0, input_length - len(data)), "constant")


        model = kerasDiscriminator(data)

    def test_train_batch(self):
        input_length = 16000
        data, _ = librosa.core.load('./tmp/WRLD-KICK-1-D.wav', sr=16000, res_type='kaiser_fast')

        # Random offset / Padding
        if len(data) > input_length:
            max_offset = len(data) - input_length
            offset = np.random.randint(max_offset)
            data = data[:(input_length + offset)]
        else:
            if input_length > len(data):
                max_offset = input_length - len(data)
                offset = np.random.randint(max_offset)
            else:
                offset = 0

            data = np.pad(data, (0, input_length - len(data)), "constant")

        #plotWav(data)

        model = DiscrimModel()

    def test_DiscriminatorModel(self):

        model = DiscriminatorModel()
        model.model.summary()

        #noise = np.random.normal(0, 1, (32, 16000))
        #noise_2 = np.random.normal(0, 1, (32, 16000))

        #model.train_batch(noise, noise_2)


    def test_keras_discriminator(self):

        model = Discriminator_new()




        name = ''

