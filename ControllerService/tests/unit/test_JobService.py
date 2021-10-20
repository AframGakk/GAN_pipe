from unittest import TestCase
from unittest.mock import patch
import pika
import os
import json
from datetime import datetime

os.chdir('../../')

from Services.JobService.JobService import JobService
from Models.DTO.JobDTO import JobDTO
from Models.Inputs.JobInputModel import JobInputModel
from Models.Inputs.ParameterInputModel import ParameterInputModel

service_env_var = {
    'TRAINER': 'ml.trainer',
    'ZONE': 'ZONE',
    'PROJECT_ID': 'project'
}

repo_env_var = {
    'PGHOST': '34.89.28.185',
    'PGDATABASE': 'ml-pipe-database',
    'PGUSER': 'villi',
    'PGPASSWORD': 'aframgakk19'
}

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
    None,
    '1/1/30/generator.h5',
    '1/30/sample_records.npy',
    1,
    28,
    4,
    None,
    'Test job info aefgbaef'
)

jobInput = JobInputModel(
    'new input test',
    1,
    1,
    ParameterInputModel(
        64,
        0.002,
        0.5,
        0.2
    ),
    'new test input model'
)


class test_JobService(TestCase):


    def setUp(self):
        self.service = JobService()

    def test_pop_queue(self):
        self.service.job_queue = [1, 2, 3]
        first = self.service.pop_queue()
        self.assertEqual(first, 1)
        self.assertEqual(len(self.service.job_queue), 2)
        self.assertListEqual(self.service.job_queue, [2, 3])

    def test_pop_queue_empty(self):
        self.service.job_queue = []
        pop = self.service.pop_queue()
        self.assertFalse(pop)
        self.assertEqual(pop, None)

    @patch('Services.JobService.JobService.JobService.deployJob')
    @patch('Services.JobService.JobService.JobRepo.insertJob')
    def test_create_job_deployed(self, insertJob_mock, deploy_mock):
        #insertJob_mock.return_value = JobDTO(2, 1, None, None, 'modelLocation', 'dataLocation', 'KICK', { 'batch_size': 64, 'noise_dim': 100 })

        self.service.createJob(jobInput)

        insertJob_mock.assert_called_once()
        #deploy_mock.assert_called_once()

    @patch('Services.JobService.JobService.JobService.deployJob')
    @patch('Services.JobService.JobService.JobRepo.insertJob')
    def test_create_job_queued(self, insertJob_mock, deploy_mock):
        self.service.active_jobs = 4
        #insertJob_mock.return_value = JobDTO(2, 1, None, None, 'modelLocation', 'dataLocation', 'KICK',

        self.service.createJob(jobInput)

        insertJob_mock.assert_called_once()
        deploy_mock.assert_not_called()
        #self.assertEqual(len(self.service.job_queue), 1)


    @patch('Services.JobService.JobService.JobRepo.putJob')
    def test_deploy_job_queued(self, insertJob_mock):
        self.service.active_jobs = 4
        self.service.deployJob(jobInput)

        insertJob_mock.assert_called_once()
        self.assertEqual(self.service.active_jobs, 4)
        self.assertNotEqual(len(self.service.job_queue), 0)

    @patch('Services.JobService.JobService.JobRepo.putJob')
    def test_deploy_job_not_queued(self, insertJob_mock):
        self.service.deployJob(jobInput)

        insertJob_mock.assert_called_once()
        self.assertEqual(self.service.active_jobs, 1)

    @patch('Services.JobService.JobService.JobRepo.putJob')
    def test_job_retrieval_queue_empty(self, put_mock):
        self.service.active_jobs = 1

        ret_value = self.service.jobRetrieval(jobDto)

        put_mock.assert_called()
        self.assertEqual(ret_value, None)


    @patch('Services.JobService.JobService.JobRepo.putJob')
    def test_job_retrieval_queue(self, put_mock):
        self.service.active_jobs = 1
        self.service.job_queue.append(jobDto)

        ret_value = self.service.jobRetrieval(jobDto)

        put_mock.assert_called()
        self.assertEqual(len(self.service.job_queue), 0)
        self.assertEqual(self.service.active_jobs, 1)


    def test_learnerStatus(self):
        resp = self.service._learnerInstance_status()
        name = ''


    def test_turn_on_learner(self):
        #resp = self.service._turnOn_learner()

        name = ''


    def test_turn_off_learner(self):
        #resp = self.service._turnOff_learner()

        name = ''

    def test_updateJob(self):

        self.service.updateJob(jobDto)

        name = ''







