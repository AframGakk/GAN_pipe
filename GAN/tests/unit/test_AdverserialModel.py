from unittest import TestCase

from Models.AdverserialModel import AdverserialModel
from Models.GeneratorModel import GeneratorModel
from Models.DiscriminatorModel import DiscriminatorModel

class test_AdverserialModel(TestCase):

    def test_init(self):
        '''
        The stacked generator and discriminator can build!
        :return:
        '''
        gen = GeneratorModel()
        disc = DiscriminatorModel()
        model = AdverserialModel(disc.model, gen.model)



