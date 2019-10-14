from unittest import TestCase
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np
import wave

from Models.GeneratorModel import GeneratorModel

os.chdir('../../')

class test_GeneratorModel(TestCase):

    def setUp(self):
        self.generator = GeneratorModel()

    def test_init(self):
        #self.assertTrue(self.generator)
        noise = np.random.rand(10, 100)
        images = self.generator.generate_sound(noise, training=False)

        for i in range(4):
            w = images[i]
            outfile = os.path.join(, "train_epoch_%02d(%02d).wav" % (epoch, i))
            save_audio(w, outfile)

        test_image_stack = (test_image_stack * 127.5) + 127.5
        test_image_stack = np.squeeze(np.round(test_image_stack).astype(np.uint8))
        tiled_output = tile_images(test_image_stack)
        tiled_output = Image.fromarray(tiled_output, mode='L')  # L specifies greyscale
        outfile = os.path.join(output_dir, 'epoch_{}.png'.format(epoch))
        tiled_output.save(outfile)



        #raw = wave.open('./tmp/WRLD-Kick-1-D.wav')

        #plt.imshow(images)
        #plt.imshow(images[0, :, :, 0], cmap='gray')
        #plt.show()

        #plt.figure(figsize=(16, 4))
        #plt.plot(images[0][:500], '.')
        #plt.plot(images[0][:500], '-')
        #plt.show()

        name = ''

    def test_other(self):
        name  = ''

    def save_audio(y, path):
        """ generate a wav file from a given spectrogram and save it """
        s = np.squeeze(y)
        s = denormalize(s)
        w = audio.inv_melspectrogram(s)
        audio.save_wav(w, path)




