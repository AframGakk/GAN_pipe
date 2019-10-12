from unittest import TestCase
import tensorflow as tf
import os
import matplotlib.pyplot as plt

from Models.GeneratorModel import GeneratorModel

os.chdir('../../')

class test_GeneratorModel(TestCase):

    def setUp(self):
        self.generator = GeneratorModel()

    def test_init(self):
        #self.assertTrue(self.generator)

        noise = tf.random.normal([1, 100])
        images = self.generator.generate_sound(noise, training=False)

        plt.imshow(images[0, :, :, 0], cmap='gray')
        plt.show()

        name = ''