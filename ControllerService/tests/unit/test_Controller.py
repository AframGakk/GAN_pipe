from unittest import TestCase
from unittest.mock import patch
import os
import json
from json.decoder import JSONDecodeError

os.chdir('../../')

from Controller import Controller
from Models.Inputs.JobInputModel import JobInputModel
from Models.DTO.JobDTO import JobDTO
from Models.Inputs.ParameterInputModel import ParameterInputModel


class test_Controller(TestCase):

    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_accept(self, pika_mock, service_mock):
        controller = Controller()
        body_json = { 'sound_type': 'KICK', 'parameters': { 'batch_size': 64, 'noise_dim': 100 } }
        body = json.dumps(body_json)
        controller.trainingScheduleCallback(None, None, None, body)

        jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))

        service_mock.assert_called_once()
        service_mock.assert_called_with(jobInput)
        #service_mock.assert_called()


    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_unsuccess_jsonobject_nonserializable(self, pika_mock, service_mock):
        controller = Controller()
        body = 'hello'

        controller.trainingScheduleCallback(None, None, None, body)



    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_unsuccess_object_not_valid(self, pika_mock, service_mock):
        controller = Controller()
        body_json = {'sound': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}
        body = json.dumps(body_json)

        controller.trainingScheduleCallback(None, None, None, body)
        jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))
        # service_mock.assert_called()



    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_accept(self, pika_mock, service_mock):
        controller = Controller()
        body_json = { 'id': 1,
                      'version': 4,
                      'date_time_start': 0,
                      'date_time_stop': 0,
                      'model_location': 'KICK/latest/model.h5',
                      'sound_type': 'KICK',
                      'parameters': {
                          'batch_size': 64, 'noise_dim': 100
                      }
                    }
        body = json.dumps(body_json)
        controller.trainingRetrievalCallback(None, None, None, body)

        #jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))

        #service_mock.assert_called_once()
        #service_mock.assert_called_with(jobInput)
        #service_mock.assert_called()


    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_unsuccess_jsonobject_nonserializable(self, pika_mock, service_mock):
        controller = Controller()

        body = 'hello'
        controller.trainingRetrievalCallback(None, None, None, body)

        # jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))

        #service_mock.assert_called_once()
        # service_mock.assert_called_with(jobInput)
        service_mock.assert_not_called()


    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_unsuccess_object_not_valid(self, pika_mock, service_mock):
        controller = Controller()
        body_json = {'sound': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}
        body = json.dumps(body_json)

        controller.trainingRetrievalCallback(None, None, None, body)
        jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))
        service_mock.assert_not_called()


    @patch('Controller.pika')
    def test_validateJobDto_success(self, pika_mock):
        controller = Controller()
        body = {'id': 1,
                'version': 4,
                'date_time_start': 0,
                'date_time_stop': 0,
                'model_location': 'KICK/latest/model.h5',
                'sound_type': 'KICK',
                'parameters': {
                    'batch_size': 64, 'noise_dim': 100
                    }
                }

        self.assertTrue(controller._validate_jobDto(body))


    @patch('Controller.pika')
    def test_validateJobDto_unsuccess(self, pika_mock):
        controller = Controller()
        body = {'version': 4,
                'date_time_start': 0,
                'date_time_stop': 0,
                'model_location': 'KICK/latest/model.h5',
                'sound_type': 'KICK',
                'parameters': {
                    'batch_size': 64, 'noise_dim': 100
                    }
                }

        self.assertFalse(controller._validate_jobDto(body))


    @patch('Controller.pika')
    def test_validateJobInput_success(self, pika_mock):
        controller = Controller()
        body = {'sound_type': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}

        self.assertTrue(controller._validate_jobInput(body))


    @patch('Controller.pika')
    def test_validateJobInput_unsuccess(self, pika_mock):
        controller = Controller()
        body = {'sound': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}

        self.assertFalse(controller._validate_jobInput(body))




