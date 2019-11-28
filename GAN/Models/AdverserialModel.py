from keras.models import Sequential
from keras.optimizers import Adam

class AdverserialModel:
    def __init__(self, discriminator, generator):
        #optimizer = RMSprop(lr=0.0004, clipvalue=1.0, decay=3e-8)
        #optimizer = Adam(lr=0.0002, beta_1=0.9)
        discriminator.trainable = False
        self.model = Sequential()
        self.model.add(generator)
        self.model.add(discriminator)
        #self.model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])




