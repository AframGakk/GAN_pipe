from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import (Layer, Input, Flatten, Dropout, BatchNormalization, Reshape,
                          MaxPool1D, AveragePooling1D, AveragePooling2D, GlobalAveragePooling1D, GlobalAveragePooling2D,
                          Convolution1D, Conv2DTranspose, Conv1D, Dense, LeakyReLU, ReLU, Activation,
                          LSTM, SimpleRNNCell)

import tensorflow as tf

def conv1d_transpose(inputs, filters, kernel_width, stride=4, padding='same', upsample='zeros'):
    if upsample == 'zeros':
        return Conv2DTranspose(
            filters,
            (1, kernel_width),
            strides=(1, stride),
            padding='same'
            )(tf.expand_dims(inputs, axis=1))[:, 0]
    elif upsample == 'nn':
        batch_size = tf.shape(inputs)[0]
        _, w, nch = inputs.get_shape().as_list()

        x = inputs

        x = tf.expand_dims(x, axis=1)
        x = tf.image.resize_nearest_neighbor(x, [1, w * stride])
        x = x[:, 0]

        return Conv1D(
            x,
            filters,
            kernel_width,
            1,
            padding='same')
    else:
        raise NotImplementedError


def Conv1DTranspose(input_tensor, filters, kernel_size, strides=2, padding='same'):
    x = Lambda(lambda x: K.expand_dims(x, axis=2))(input_tensor)
    x = Conv2DTranspose(filters=filters, kernel_size=(kernel_size, 1), strides=(strides, 1), padding=padding)(x)
    x = Lambda(lambda x: K.squeeze(x, axis=2))(x)
    return x


class GenModel:
    def __init__(self):

        input = tf.random.uniform([64, 100], -1., 1., dtype=tf.float32)
        slice_len = 16384
        nch = 1
        kernel_len = 25
        dim = 64
        use_batchnorm = False
        upsample = 'zeros'
        train = False

        assert slice_len in [16384, 32768, 65536]
        batch_size = tf.shape(input)[0]

        if use_batchnorm:
            batchnorm = lambda x: tf.layers.batch_normalization(x, training=train)
        else:
            batchnorm = lambda x: x

        # FC and reshape for convolution
        # [100] -> [16, 1024]
        dim_mul = 16
        output = input
        with tf.variable_scope('z_project'):
            output = tf.layers.dense(output, 4 * 4 * dim * dim_mul)
            output = tf.reshape(output, [batch_size, 16, dim * dim_mul])
            output = batchnorm(output)
        output = tf.nn.relu(output)
        dim_mul //= 2

        # Layer 0
        # [16, 1024] -> [64, 512]
        with tf.variable_scope('upconv_0'):
            output = conv1d_transpose(output, dim * dim_mul, kernel_len, 4, upsample=upsample)
            output = batchnorm(output)
        output = tf.nn.relu(output)
        dim_mul //= 2

        # Layer 1
        # [64, 512] -> [256, 256]
        with tf.variable_scope('upconv_1'):
            output = conv1d_transpose(output, dim * dim_mul, kernel_len, 4, upsample=upsample)
            output = batchnorm(output)
        output = tf.nn.relu(output)
        dim_mul //= 2

        # Layer 2
        # [256, 256] -> [1024, 128]
        with tf.variable_scope('upconv_2'):
            output = conv1d_transpose(output, dim * dim_mul, kernel_len, 4, upsample=upsample)
            output = batchnorm(output)
        output = tf.nn.relu(output)
        dim_mul //= 2

        # Layer 3
        # [1024, 128] -> [4096, 64]
        with tf.variable_scope('upconv_3'):
            output = conv1d_transpose(output, dim * dim_mul, kernel_len, 4, upsample=upsample)
            output = batchnorm(output)
        output = tf.nn.relu(output)

        # Layer 4
        # [4096, 64] -> [16384, nch]
        with tf.variable_scope('upconv_4'):
            output = conv1d_transpose(output, nch, kernel_len, 4, upsample=upsample)
        output = tf.nn.tanh(output)


        # Automatically update batchnorm moving averages every time G is used during training
        if train and use_batchnorm:
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS, scope=tf.get_variable_scope().name)
            if slice_len == 16384:
                assert len(update_ops) == 10
            else:
                assert len(update_ops) == 12
            with tf.control_dependencies(update_ops):
                output = tf.identity(output)

        G_opt = tf.train.AdamOptimizer(
            learning_rate=1e-4,
            beta1=0.5,
            beta2=0.9)


        self.model = output


    def generate_sound(self, noise, training=True):
        return self.model.predict(noise)
        #self.model.


class GeneratorModel:
    def __init__(self):
        dim_mul = 16
        dim = 64
        output = (64, 100)
        kernel_len = 25

        # [100] -> [16, 1024]
        #model = Sequential()
        #model.add(Dense((output, 4 * 4 * dim * dim_mul), input_shape=(100,)))
        #model.add(Reshape(output, [64, 16, dim * dim_mul]))
        #model.add(BatchNormalization(output))
        #model.add(ReLU())
        #output = Input(batch_shape=output)
        #output = Convolution1D(64, 10, input_shape=(100, ))
        output = Dense(4 * 4 * dim * dim_mul)(output)
        output = Reshape([64, 16, dim * dim_mul])(output)
        output = BatchNormalization()(output)
        output = ReLU()(output)

        dim_mul //= 2

        # [16, 1024] -> [64, 512]
        output = conv1d_transpose(output, dim * dim_mul, kernel_len, 4, upsample='zeros')
        output = BatchNormalization(output)
        output = ReLU(output)

        dim_mul //= 2



# OLD MODEL
'''
model = Sequential()

        model.add(Dense(256 * D, input_dim=100))
        model.add(layers.Reshape((4, 4, 16 * D)))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(8 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(4 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(2 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))
        model.add(layers.Conv2D(D, (5, 5), padding='same'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(2, (5, 5), padding='same'))
        model.add(layers.Activation('tanh'))

'''


'''
        model = Sequential()
        model.add(Dense(1000, input_shape=(100,)))
        model.add(LeakyReLU(alpha=0.01))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Reshape((1000, 1)))

        model.add(Conv1D(4, 25, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(8, 50, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(16, 100, padding='same'))
        model.add(Dropout(rate=0.3))
        model.add(Flatten())

        model.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.0002, beta_1 = 0.9), metrics =['accuracy'])

        self.model = model
'''