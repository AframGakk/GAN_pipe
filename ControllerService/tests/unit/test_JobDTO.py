from unittest import TestCase
import os

os.chdir('../../')

from Models.DTO.JobDTO import JobDTO

class test_JobDTO(TestCase):


    def test_init_no_parameters(self):
        with self.assertRaises(TypeError):
            job = JobDTO()

    

