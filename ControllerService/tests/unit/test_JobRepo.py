from unittest import TestCase
import os

os.chdir('../../')

from Repositories.JobRepo.JobRepo import JobRepo
from Models.Inputs.JobInputModel import JobInputModel
from Models.DTO.JobDTO import JobDTO

class test_JobRepo(TestCase):

    def setUp(self):
        self.repo = JobRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_integration_getAllJobs(self):
        resp = self.repo.getAllJobs()



    def test_insertJob(self):
        input = JobInputModel('KICK', {'batch_size': 64, 'noise_dim': 100})

        resp = self.repo.insertJob(input)



    def test_get_job_by_id(self):

        job = self.repo.getJobById(2)



    def test_delete_job_by_id(self):

        self.repo.deleteJobById(2)



    def test_put_job(self):
        putModel = JobDTO(3, 8, None, None, 'KICK/8/model.h5', 1, 18)

        self.repo.putJob(putModel)





