import numpy as np
import tensorflow as tf

from keras import losses, models, optimizers
from keras.constraints import K
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import (Layer, Input, Flatten, Dropout, BatchNormalization, Reshape,
                          MaxPool1D, AveragePooling1D, AveragePooling2D, GlobalAveragePooling1D, GlobalAveragePooling2D,
                          Conv2DTranspose, Conv1D, Dense, LeakyReLU, ReLU, Activation,
                          LSTM, SimpleRNNCell)


def lrelu(inputs, alpha=0.2):
  return tf.maximum(alpha * inputs, inputs)


def apply_phaseshuffle(x, rad, pad_type='reflect'):
  b, x_len, nch = x.get_shape().as_list()

  phase = tf.random_uniform([], minval=-rad, maxval=rad + 1, dtype=tf.int32)
  pad_l = tf.maximum(phase, 0)
  pad_r = tf.maximum(-phase, 0)
  phase_start = pad_r
  x = tf.pad(x, [[0, 0], [pad_l, pad_r], [0, 0]], mode=pad_type)

  x = x[:, phase_start:phase_start+x_len]
  x.set_shape([b, x_len, nch])

  return x


class DiscrimModel():

    def __init__(self, input):
        #input = tf.random.uniform([64, 100], -1., 1., dtype=tf.float32)
        kernel_len = 25
        dim = 64
        use_batchnorm = False
        phaseshuffle_rad = 0
        batch_size = tf.shape(input)[0]


        if use_batchnorm:
            batchnorm = lambda x: tf.layers.batch_normalization(x, training=True)
        else:
            batchnorm = lambda x: x

        if phaseshuffle_rad > 0:
            phaseshuffle = lambda x: apply_phaseshuffle(input, phaseshuffle_rad)
        else:
            phaseshuffle = lambda x: x

        # Layer 0
        # [16384, 1] -> [4096, 64]
        output = input
        with tf.variable_scope('downconv_0'):
            output = tf.layers.conv1d(output, dim, kernel_len, 4, padding='SAME')
        output = lrelu(output)
        output = phaseshuffle(output)

        # Layer 1
        # [4096, 64] -> [1024, 128]
        with tf.variable_scope('downconv_1'):
            output = tf.layers.conv1d(output, dim * 2, kernel_len, 4, padding='SAME')
        output = batchnorm(output)
        output = lrelu(output)
        output = phaseshuffle(output)

        # Layer 2
        # [1024, 128] -> [256, 256]
        with tf.variable_scope('downconv_2'):
            output = tf.layers.conv1d(output, dim * 4, kernel_len, 4, padding='SAME')
        output = batchnorm(output)
        output = lrelu(output)
        output = phaseshuffle(output)

        # Layer 3
        # [256, 256] -> [64, 512]
        with tf.variable_scope('downconv_3'):
            output = tf.layers.conv1d(output, dim * 8, kernel_len, 4, padding='SAME')
        output = batchnorm(output)
        output = lrelu(output)
        output = phaseshuffle(output)

        # Layer 4
        # [64, 512] -> [16, 1024]
        with tf.variable_scope('downconv_4'):
            output = tf.layers.conv1d(output, dim * 16, kernel_len, 4, padding='SAME')
        output = batchnorm(output)
        output = lrelu(output)

        # Flatten
        output = tf.reshape(output, [batch_size, -1])

        # Connect to single logit
        with tf.variable_scope('output'):
            output = tf.layers.dense(output, 1)[:, 0]

            # Don't need to aggregate batchnorm update ops like we do for the generator because we only use the discriminator for training


        self.output = output

class kerasDiscriminator_OLD():
    def __init__(self, input):
        output = K.constant(input, 1)
        dim = 64
        kernel_len = 25
        phaseshuffle_rad = 2

        # Layer 0
        # [16384, 1] -> [4096, 64]
        output = Conv1D(dim, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 1
        # [4096, 64] -> [1024, 128]
        output = Conv1D(dim * 2, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        # batchnorm here
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 2
        # [1024, 128] -> [256, 256]
        output = Conv1D(dim * 4, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        # batchnorm here
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 3
        # [256, 256] -> [64, 512]
        output = Conv1D(dim * 8, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        # batchnorm here
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 4
        # [64, 512] -> [16, 1024]
        output = Conv1D(dim * 16, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        # batchnorm here
        output = LeakyReLU()(output)

        # Flatten
        output = Flatten()(output)
        #output = Reshape()

        output = Dense(1)(output)  #[:, 0]

        self.output = output


class kerasDiscriminator():
    def __init__(self, input):
        output = K.constant(input, 1)
        dim = 64
        kernel_len = 25
        phaseshuffle_rad = 2

        model = Sequential()

        # Layer 0
        # [16384, 1] -> [4096, 64]
        model.add(Conv1D(dim, kernel_size=kernel_len, strides=4, padding='SAME', input_shape=(16384, 1)))
        model.add(LeakyReLU(alpha=0.2)) # TODO: is alpha important
        model.add(BatchNormalization(0.9))
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 1
        # [4096, 64] -> [1024, 128]
        output = Conv1D(dim * 2, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        model.add(BatchNormalization(0.9))
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 2
        # [1024, 128] -> [256, 256]
        output = Conv1D(dim * 4, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        model.add(BatchNormalization(0.9))
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 3
        # [256, 256] -> [64, 512]
        output = Conv1D(dim * 8, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        model.add(BatchNormalization(0.9))
        output = LeakyReLU()(output)
        output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 4
        # [64, 512] -> [16, 1024]
        output = Conv1D(dim * 16, kernel_size=kernel_len, strides=4, padding='SAME')(output)
        model.add(BatchNormalization(0.9))
        output = LeakyReLU()(output)

        # Flatten
        output = Flatten()(output)
        #output = Reshape()

        output = Dense(1)(output)  #[:, 0]

        self.output = output



class DiscriminatorModel_v1():
    def __init__(self):
        InputShape = 16384
        dim = 64

        model = Sequential()

        # [16384, 1] -> [4096, 64]
        model.add(Reshape((InputShape, 1), input_shape=(InputShape,)))
        model.add(Conv1D(64, 25, strides=4, padding='valid'))
        model.add(ReLU())
        model.add(AveragePooling1D(4))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        # [4096, 64] -> [1024, 128]
        model.add(Conv1D(dim * 2, 25, strides=4, padding='valid'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        # [1024, 128] -> [256, 256]
        model.add(Conv1D(dim * 4, 25, strides=4, padding='valid'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        # [256, 256] -> [64, 512]
        model.add(Conv1D(dim * 8, 25, strides=4, padding='valid'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        # [64, 512] -> [16, 1024]
        #model.add(Conv1D(dim * 16, 25, strides=4, padding='valid'))
        #model.add(ReLU())
        #model.add(BatchNormalization(momentum=0.9))
        #model.add(Dropout(rate=0.1))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.01))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dense(1, activation='sigmoid'))

        self.model = model

    def train_batch(self, real_inputs, fake_inputs):
        return self.model.train_on_batch(real_inputs, fake_inputs)


class DiscriminatorModel():
    def __init__(self, alpha=0.2):
        InputShape = 16000
        input_dim = 32
        '''
        Last param:
        kernel_size:
            100
            50
            25
        strides:
            7
            5
            3
        '''

        model = Sequential()

        model.add(Reshape((InputShape, 1), input_shape=(InputShape,)))
        model.add(Conv1D(input_dim, 25, strides=4, padding='valid'))
        model.add(LeakyReLU(alpha=alpha))
        model.add(AveragePooling1D(4))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        input_dim //= 2

        model.add(Conv1D(16, 25, strides=4, padding='valid'))
        model.add(LeakyReLU(alpha=alpha))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        input_dim //= 2

        model.add(Conv1D(8, 25, strides=4, padding='valid'))
        model.add(LeakyReLU(alpha=alpha))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        input_dim //= 2

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=alpha))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dense(1, activation='sigmoid'))

        self.model = model
