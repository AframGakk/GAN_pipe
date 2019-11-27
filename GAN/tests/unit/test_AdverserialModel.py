from unittest import TestCase

from Models.AdverserialModel import AdverserialModel
from Models.GeneratorModel import GeneratorModel
from Models.DiscriminatorModel import DiscriminatorModel

class test_AdverserialModel(TestCase):

    def test_init(self):
        gen = GeneratorModel()
        disc = DiscriminatorModel()
        model = AdverserialModel(disc.model, gen.model)
        print(model.model.summary())

        name = ''


