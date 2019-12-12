from unittest import TestCase

from Models.AdverserialModel import AdverserialModel
from Models.GeneratorModel import GeneratorModel, Generator_new
from Models.DiscriminatorModel import DiscriminatorModel, Discriminator_new

class test_AdverserialModel(TestCase):

    def test_init(self):
        gen = GeneratorModel()
        print(gen.model.summary())
        disc = DiscriminatorModel()
        print(disc.model.summary())
        model = AdverserialModel(disc.model, gen.model)
        print(model.model.summary())

        name = ''


    def test_new(self):
        gen = Generator_new()
        disc = Discriminator_new()

        model = AdverserialModel(gen.model, disc.model)

        print(model.model.summary())


