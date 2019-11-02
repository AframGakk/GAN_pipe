import pika
import json
from json.decoder import JSONDecodeError
import os
import configparser
import traceback

from Models.DTO.JobDTO import JobDTO
from Models.Inputs.JobInputModel import JobInputModel
from Models.Inputs.ParameterInputModel import ParameterInputModel
from Services.JobService.JobService import JobService

config = configparser.ConfigParser()
_jobService = JobService()

class Controller:

    def __init__(self):
        '''
        The main controller for retrieving messages and sending messages via broker.
        '''
        try:
            config.read('./config/config.ini')
            RABBIT = config['RABBIT']['RHOST']
            RABBIT_USER = config['RABBIT']['RUSER']
            RABBIT_PASS = config['RABBIT']['RPASS']
            RABBIT_VHOST = config['RABBIT']['RVHOST']
        except:
            print('Could not load config file')
            traceback.print_exc()
            return

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials))
        self.channel = self.connection.channel()

        # The queues
        self.scheduling_queue = 'gan.training.schedule'
        self.deployment_queue = 'gan.training.deploy'  # The deployment queue
        self.retrieve_queue = 'gan.training.retrieval'

        # Publish keys
        self.training_key = 'gan.train.GPU'

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.scheduling_queue, durable=True)
        self.channel.queue_declare(queue=self.retrieve_queue, durable=True)

        # consume all queues needed
        self.channel.basic_consume(
            queue=self.scheduling_queue, on_message_callback=self.trainingScheduleCallback, auto_ack=True)
        self.channel.basic_consume(
            queue=self.retrieve_queue, on_message_callback=self.trainingRetrievalCallback, auto_ack=True)


    def trainingScheduleCallback(self, ch, method, props, body):
        '''
        Callback function retrieves messages from scheduling queue in broker.
        :param ch: the broker channel recieved from
        :param method: broker method
        :param props: object, properties object for broker message
        :param body: bstring, the body containing the data with the message
        :return: None
        '''
        try:
            info_obj = json.loads(body)
        except JSONDecodeError:
            #logger.error(__name__, 'body object is non json seriable: {}'.format(body))
            print('The body object could not be serialized: {}'.format(body))
            return

        if not self._validate_jobInput(info_obj):
            print('Body does not contain enough info on Job: {}'.format(body))
            return

        jobInput = JobInputModel(info_obj['sound_type'], ParameterInputModel(info_obj['parameters']['batch_size'], info_obj['parameters']['noise_dim']))
        jobDto = _jobService.createJob(jobInput)

        if jobDto:
            self.channel.basic_publish(exchange='', routing_key=self.training_key, body=jobDto.json())



    def trainingRetrievalCallback(self, ch, method, props, body):
        '''
        Callback funtion for queue messages from gan training on finished training sessions.
        :param ch: the broker channel recieved from
        :param method: broker method
        :param props: object, properties object for broker message
        :param body: bstring, the body containing the data with the message
        :return: None
        '''

        try:
            info_obj = json.loads(body)
        except:
            #logger.error(__name__, 'body object is non json seriable: {}'.format(body))
            print('The body object could not be serialized: {}'.format(body))
            return

        if not self._validate_jobDto(info_obj):
            print('Body does not contain enough info on Job: {}'.format(body))
            return

        jobDto = JobDTO(info_obj['id'], info_obj['version'], info_obj['date_time_start'], info_obj['date_time_stop'],
                        info_obj['model_location'], info_obj['sound_type'], info_obj['parameters'])

        jobDto = _jobService.jobRetrieval(jobDto)

        if jobDto:
            self.channel.basic_publish(exchange='', routing_key=self.training_key, body=jobDto.json())



    def _validate_jobDto(self, jobDto):
        if not ('id' in jobDto and 'version' in jobDto and 'date_time_start' in jobDto and 'date_time_stop' in jobDto
                and 'model_location' in jobDto and 'sound_type' in jobDto and 'parameters' in jobDto):
            return False
        return True

    def _validate_jobInput(self, jobInput):
        if not ('sound_type' in jobInput and 'parameters' in jobInput):
            return False
        return True




