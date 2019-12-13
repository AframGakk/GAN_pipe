from keras.models import Sequential
from keras.optimizers import Adam

class AdverserialModel:
    def __init__(self, discriminator, generator):
        discriminator.trainable = False
        self.model = Sequential()
        self.model.add(generator)
        self.model.add(discriminator)




