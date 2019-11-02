from unittest import TestCase
from unittest.mock import patch
import os

os.chdir('../../')

from Services.JobService.JobService import JobService
from Models.DTO.JobDTO import JobDTO

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
        insertJob_mock.return_value = JobDTO(2, 1, None, None, 'modelLocation', 'KICK', { 'batch_size': 64, 'noise_dim': 100 })
        jobInput = { 'test': 'test' }

        self.service.createJob(jobInput)

        insertJob_mock.assert_called_once()
        deploy_mock.assert_called_once()

    @patch('Services.JobService.JobService.JobService.deployJob')
    @patch('Services.JobService.JobService.JobRepo.insertJob')
    def test_create_job_queued(self, insertJob_mock, deploy_mock):
        self.service.active_jobs = 4
        insertJob_mock.return_value = JobDTO(2, 1, None, None, 'modelLocation', 'KICK',
                                             {'batch_size': 64, 'noise_dim': 100})
        jobInput = {'test': 'test'}
        self.service.createJob(jobInput)

        insertJob_mock.assert_called_once()
        deploy_mock.assert_not_called()
        self.assertEqual(len(self.service.job_queue), 1)


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

        putModel = JobDTO(3, 8, None, None, 'KICK/8/model.h5', 1, 18)

        self.service.updateJob(putModel)

        name = ''



