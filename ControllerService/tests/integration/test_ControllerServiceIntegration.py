from unittest import TestCase
import os
import json
import pika
from datetime import datetime

os.chdir('../../')



class test_ControllerServiceIntegration(TestCase):

    def setUp(self):
        RABBIT = 'localhost'
        RABBIT_USER = 'guest'
        RABBIT_PASS = 'guest'
        RABBIT_VHOST = '/'

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials))
        self.channel = self.connection.channel()


    def test_sendSchedulingMessage(self):
        jobInput = { 'version': 3, 'sound_type': 'KICK', 'parameters': { 'batch_size': 64, 'noise_dim': 100 } }
        self.channel.basic_publish(exchange='', routing_key='gan.training.schedule', body=json.dumps(jobInput))


    def test_featureEngineeringMessage(self):
        jobDTO = { 'id': 3,
                   'version': 8,
                   'date_time_start': None,
                   'date_time_stop': None,
                   'model_location': 'MODELLOCATION',
                   'data_location': 'DATALOCATION',
                   'sound_type': 1,
                   'parameters': 18,
                   'status': 1
                   }
        self.channel.basic_publish(exchange='', routing_key='gan.training.features', body=json.dumps(jobDTO))


    def test_trainingRetrievalMessage(self):
        jobDTO = {'id': 19,
                  'version': 3,
                  'date_time_start': 1572714985.435909,
                  'date_time_stop': None,
                  'model_location': 'MODELLOCATION',
                  'data_location': 'DATALOCATION',
                  'sound_type': 1,
                  'parameters': 18,
                  'status': 2
                  }
        self.channel.basic_publish(exchange='', routing_key='gan.training.retrieval', body=json.dumps(jobDTO))


