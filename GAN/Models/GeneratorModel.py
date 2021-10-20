from keras.models import Sequential
from keras.layers import (Flatten, Dropout, BatchNormalization, Reshape,
                            Conv2DTranspose, Conv1D, Conv2D, Dense, LeakyReLU, ReLU, Activation, UpSampling2D)

class GeneratorModel:
    def __init__(self, alpha=0.2):
        '''
        Main generator model used for the GAN engine.
        :param alpha: the slope of the activation function
        '''
        noise_dim = 500

        model = Sequential()
        model.add(Dense(1000, input_shape=(noise_dim,)))
        model.add(BatchNormalization(momentum=0.9))
        model.add(LeakyReLU(alpha=alpha))
        model.add(Reshape((1000, 1)))

        model.add(Conv1D(16, 20, padding='same'))
        model.add(BatchNormalization(momentum=0.9))
        model.add(LeakyReLU(alpha=alpha))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(32, 25, padding='same'))
        model.add(BatchNormalization(momentum=0.9))
        model.add(LeakyReLU(alpha=alpha))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(64, 50, padding='same'))
        model.add(BatchNormalization(momentum=0.9))
        model.add(LeakyReLU(alpha=alpha))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(64, 100, padding='same'))
        model.add(Dropout(rate=0.3))
        model.add(Flatten())

        self.model = model



class Generator_v5:
    def __init__(self):
        dim = 64
        dim_mul = 16

        model = Sequential()

        # [100] -> [16, 1024]
        model.add(Dense(4 * 4 * dim * dim_mul, input_shape=(100,)))
        #model.add(LeakyReLU(alpha=0.01))
        model.add(Reshape((16, dim * dim_mul)))
        model.add(BatchNormalization())
        model.add(ReLU())
        #model.add(Reshape([64, 16, dim * dim_mul]))
        dim_mul //= 2

        # [16, 1024] -> [64, 512]
        model.add(Conv1D(dim * dim_mul, 25, strides=4, padding='same'))
        #model.add(Reshape((64, dim * dim_mul)))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # [64, 512] -> [256, 256]
        model.add(Conv1D(dim * dim_mul, 25, strides=4, padding='same'))
        #model.add(Reshape((256, dim * dim_mul)))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # [256, 256] -> [1024, 128]
        model.add(Conv1D(dim * dim_mul, 25, padding='same'))
        #model.add(Reshape((1024, dim * dim_mul)))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # [1024, 128] -> [4096, 128]
        model.add(Conv1D(dim * dim_mul, 25, padding='same'))
        #model.add(Reshape((4096, dim * dim_mul)))
        model.add(BatchNormalization())
        model.add(ReLU())


        # [4096, 64] -> [16384, nch]
        model.add(Conv1D(1, 4, padding='same'))
        model.add(Dropout(rate=0.3))
        model.add(Flatten())

        print(model.summary())

        self.model = model


class Generator_v6:
    def __init__(self):
        dim_mul = 16
        dim = 64

        # FC and reshape for convolution
        # [100] -> [16, 1024]
        model = Sequential()

        model.add(Reshape(4 * 4 * dim * dim_mul))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # Layer 0
        # [16, 1024] -> [64, 512]
        model.add(Conv1D(dim * dim_mul, kernel_size=25, strides=4))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # Layer 1
        # [64, 512] -> [256, 256]
        model.add(Conv1D(dim * dim_mul, kernel_size=25, strides=4))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # Layer 2
        # [256, 256] -> [1024, 128]
        model.add(Conv1D(dim * dim_mul, kernel_size=25, strides=4))
        model.add(BatchNormalization())
        model.add(ReLU())
        dim_mul //= 2

        # Layer 3
        # [1024, 128] -> [4096, 64]
        model.add(Conv1D(dim * dim_mul, kernel_size=25, strides=4))
        model.add(BatchNormalization())
        model.add(ReLU())

        model.add(Conv1D(1, kernel_size=25, strides=4))
        model.add(ReLU())

        print(model.summary())

        self.model = model


class GeneratorModel_v4:
    def __init__(self, input):
        dim = 64
        dim_mul = 16

        model = Sequential()

        output = input

        # [100] -> [16, 1024]
        #model.add(Dense(4 * 4 * dim * dim_mul, input_shape=(100,)))
        output = Dense(4 * 4 * dim * dim_mul, input_shape=(100,))(output)
        #model.add(LeakyReLU(alpha=0.01))
        #model.add(BatchNormalization(momentum=0.9))
        output = BatchNormalization(momentum=0.9)(output)
        #model.add(Reshape((16, dim * dim_mul)))
        output = Reshape()
        #model.add(Reshape([64, 16, dim * dim_mul]))
        dim_mul //= 2


        # [16, 1024] -> [64, 512]
        #model.add(Conv1D(dim * dim_mul, 25, strides=4, padding='same'))
        model.add(Conv2DTranspose(dim * dim_mul, (1, 25), strides=(1, 4), padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        #model.add(Reshape((64, dim * dim_mul)))
        dim_mul //= 2

        # [64, 512] -> [256, 256]
        model.add(Conv1D(dim * dim_mul, 25, strides=4, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        model.add(Reshape((256, dim * dim_mul)))
        dim_mul //= 2

        # [256, 256] -> [1024, 128]
        model.add(Conv1D(dim * dim_mul, 25, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))
        dim_mul //= 2

        # [1024, 128] -> [4096, 128]
        model.add(Conv1D(dim * dim_mul, 25, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        # [4096, 64] -> [16384, nch]
        model.add(Conv1D(1, 4, padding='same'))
        model.add(Dropout(rate=0.3))
        model.add(Flatten())

        print(model.summary())

        self.model = model



class GeneratorModel_v3:
    def __init__(self):
        D = 64

        model = Sequential()

        model.add(Dense(256 * D, input_dim=100))
        model.add(Reshape((4, 4, 16 * D)))
        model.add(Activation('relu'))

        model.add(UpSampling2D(size=(2, 2)))
        model.add(Conv2D(8 * D, (5, 5), padding='same'))
        model.add(Activation('relu'))

        model.add(UpSampling2D(size=(2, 2)))
        model.add(Conv2D(4 * D, (5, 5), padding='same'))
        model.add(Activation('relu'))

        model.add(UpSampling2D(size=(2, 2)))
        model.add(Conv2D(2 * D, (5, 5), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(D, (5, 5), padding='same'))

        model.add(UpSampling2D(size=(2, 2)))
        model.add(Activation('relu'))

        model.add(UpSampling2D(size=(2, 2)))
        model.add(Conv2D(2, (5, 5), padding='same'))
        model.add(Activation('tanh'))
