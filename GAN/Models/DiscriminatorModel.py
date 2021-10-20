from keras.models import Sequential
from keras.layers import (Flatten, Dropout, BatchNormalization, Reshape,
                          AveragePooling1D, Conv1D, Dense, LeakyReLU, ReLU)


class DiscriminatorModel():
    def __init__(self, alpha=0.2):
        '''
        The main discriminator model.
        :param alpha: the slope of the activation function
        '''
        InputShape = 64000
        input_dim = 32

        model = Sequential()

        model.add(Reshape((InputShape, 1), input_shape=(InputShape,)))
        model.add(Conv1D(32, 25, strides=4, padding='valid'))
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




class Discriminator_v2():
    def __init__(self):
        #output = K.constant(input, 1)
        dim = 64
        kernel_len = 25
        phaseshuffle_rad = 2

        InputShape = 16384

        model = Sequential()

        model.add(Reshape((InputShape, 1), input_shape=(InputShape,)))
        # Layer 0
        # [16384, 1] -> [4096, 64]
        model.add(Conv1D(dim, kernel_size=kernel_len, strides=4, padding='SAME', input_shape=(16384, 1)))
        model.add(LeakyReLU(alpha=0.2)) # TODO: is alpha important
        #model.add(BatchNormalization(0.9))
        #output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 1
        # [4096, 64] -> [1024, 128]
        model.add(Conv1D(dim * 2, kernel_size=kernel_len, strides=4, padding='SAME'))
        model.add(BatchNormalization())
        model.add(LeakyReLU())
        #output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 2
        # [1024, 128] -> [256, 256]
        model.add(Conv1D(dim * 4, kernel_size=kernel_len, strides=4, padding='SAME'))
        model.add(BatchNormalization())
        model.add(LeakyReLU())
        #output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 3
        # [256, 256] -> [64, 512]
        model.add(Conv1D(dim * 8, kernel_size=kernel_len, strides=4, padding='SAME'))
        model.add(BatchNormalization())
        model.add(LeakyReLU())
        #output = apply_phaseshuffle(output, phaseshuffle_rad)

        # Layer 4
        # [64, 512] -> [16, 1024]
        model.add(Conv1D(dim * 16, kernel_size=kernel_len, strides=4, padding='SAME'))
        model.add(BatchNormalization())
        model.add(LeakyReLU())

        model.add(Flatten())
        model.add(Dense(1))

        # Flatten
        #output = Flatten()(output)
        #output = Reshape()
        #output = Dense(1)(output)  #[:, 0]

        #model.add(Flatten())
        #model.add(Dense(1024))
        #model.add(LeakyReLU(alpha=0.01))
        #model.add(BatchNormalization(momentum=0.9))
        #model.add(Dense(1, activation='sigmoid'))

        print(model.summary())

        self.model = model



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



