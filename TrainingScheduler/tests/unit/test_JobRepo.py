from unittest import TestCase
from unittest.mock import patch
import os
from datetime import datetime

#os.chdir('../../')

from Repositories.JobRepo.JobRepo import JobRepo
from Models.Inputs.JobInputModel import JobInputModel
from Models.DTO.JobDTO import JobDTO
from Models.Inputs.ParameterInputModel import ParameterInputModel

parameters = {
    'id': 28,
    'batch_size': 64,
    'adam_learning_rate': 0.002,
    'adam_beta': 0.5,
    'lrelu_alpha': 0.2
}

jobDto = JobDTO(
    30,
    'new test job',
    1,
    datetime.timestamp(datetime.now()),
    datetime.timestamp(datetime.now()),
    '1/1/30/generator.h5',
    '1/30/sample_records.npy',
    1,
    28,
    4,
    None,
    'Test job info'
)

env_var = {
    'PGHOST': '34.89.28.185',
    'PGDATABASE': 'ml-pipe-database',
    'PGUSER': 'villi',
    'PGPASSWORD': 'aframgakk19'
}

jobInput = JobInputModel(
    'new input test',
    1,
    1,
    {
        'batch_size': 64,
        'adam_learning_rate': 0.002,
        'adam_beta': 0.5,
        'lrelu_alpha': 0.2
    },
    'new test input model'
)

del_job_id = None

class test_JobRepo(TestCase):

    #@patch.dict('Repositories.JobRepo.JobRepo.environ', env_var)
    def setUp(self):
        self.repo = JobRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_insertJob(self):
        del_job_id = self.repo.insertJob(jobInput).id


    def test_integration_getAllJobs(self):
        resp = self.repo.getAllJobs()


    def test_get_job_by_id(self):
        job = self.repo.getJobById(73)
        print(job.__dict__())

    def test_put_job(self):
        jobDto.parameters = 36
        jobDto.id = del_job_id
        self.repo.putJob(jobDto)

    def test_delete_job_by_id(self):

        self.repo.deleteJobById(del_job_id)








