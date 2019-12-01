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

body_json = {
    'label': 'new test',
    'version': 3,
    'sound_type': 1,
    'parameters': {
        'batch_size': 64,
        'adam_learning_rate': 0.002,
        'adam_beta': 0.5,
        'lrelu_alpha': 0.2
    },
    'description': 'test desc'
}

body_json_retrieve = { 'id': 1,
                       'label': 'new training stuff',
                       'version': 4,
                       'date_time_start': 0,
                       'date_time_stop': 0,
                       'model_location': 'KICK/latest/model.h5',
                       'record_location': 'KICK/latest/model.h5',
                       'sound_type': 1,
                       'parameters': {
                           'batch_size': 64,
                           'adam_learning_rate': 0.002,
                           'adam_beta': 0.5,
                           'lrelu_alpha': 0.2
                       },
                       'status': 1,
                       'results': None,
                       'description': 'adsgasg'
}


class test_Controller(TestCase):

    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_accept(self, pika_mock, service_mock):
        controller = Controller()

        body = json.dumps(body_json)
        controller.trainingScheduleCallback(None, None, None, body)

        #jobInput = JobInputModel('KICK', ParameterInputModel(64, 100))

        service_mock.assert_called_once()
        #service_mock.assert_called_with(jobInput)
        #service_mock.assert_called()


    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_unsuccess_jsonobject_nonserializable(self, pika_mock, service_mock):
        controller = Controller()
        body = 'hello'

        controller.trainingScheduleCallback(None, None, None, body)

        service_mock.assert_not_called()



    @patch('Controller.JobService.createJob')
    @patch('Controller.pika')
    def test_schedule_callback_unsuccess_object_not_valid(self, pika_mock, service_mock):
        controller = Controller()
        body_json = {'sound': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}
        body = json.dumps(body_json)

        controller.trainingScheduleCallback(None, None, None, body)
        # service_mock.assert_called()



    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_accept(self, pika_mock, service_mock):
        controller = Controller()

        body = json.dumps(body_json_retrieve)
        controller.trainingRetrievalCallback(None, None, None, body)

        service_mock.assert_called_once()



    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_unsuccess_jsonobject_nonserializable(self, pika_mock, service_mock):
        controller = Controller()

        body = 'hello'
        controller.trainingRetrievalCallback(None, None, None, body)

        service_mock.assert_not_called()


    @patch('Controller.JobService.jobRetrieval')
    @patch('Controller.pika')
    def test_retrieval_callback_unsuccess_object_not_valid(self, pika_mock, service_mock):
        controller = Controller()
        tmp_json = {
            'id': 5
        }
        body = json.dumps(tmp_json)

        controller.trainingRetrievalCallback(None, None, None, body)

        service_mock.assert_not_called()


    @patch('Controller.pika')
    def test_validateJobDto_success(self, pika_mock):
        controller = Controller()

        self.assertTrue(controller._validate_jobDto(body_json_retrieve))


    @patch('Controller.pika')
    def test_validateJobDto_unsuccess(self, pika_mock):
        controller = Controller()

        self.assertFalse(controller._validate_jobDto(body_json))


    @patch('Controller.pika')
    def test_validateJobInput_success(self, pika_mock):
        controller = Controller()

        self.assertTrue(controller._validate_jobInput(body_json))


    @patch('Controller.pika')
    def test_validateJobInput_unsuccess(self, pika_mock):
        controller = Controller()
        body = {'sound': 'KICK', 'parameters': {'batch_size': 64, 'noise_dim': 100}}

        self.assertFalse(controller._validate_jobInput(body))




