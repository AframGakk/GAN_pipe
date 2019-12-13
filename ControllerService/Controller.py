import pika
import json
from json.decoder import JSONDecodeError
from os import environ


from Models.DTO.JobDTO import JobDTO
from Models.Inputs.JobInputModel import JobInputModel
from Models.Inputs.ParameterInputModel import ParameterInputModel
from Services.JobService.JobService import JobService

_jobService = JobService()

class Controller:

    def __init__(self):
        '''
        The main controller for retrieving messages and sending messages via broker.
        '''

        RABBIT = environ['RHOST']
        RABBIT_USER = environ['RUSER']
        RABBIT_PASS = environ['RPASS']
        RABBIT_VHOST = environ['RVHOST']

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials))
        self.channel = self.connection.channel()

        # The queues
        self.scheduling_queue = 'gan.training.schedule'
        self.retrieve_queue = 'gan.training.retrieval'
        self.feature_queue = 'gan.training.controller.records'

        # Publish keys
        self.training_key = 'gan.training.CPU'
        self.ingestion_key = 'gan.training.ingestion'
        self.deployment_key = 'gan.training.deploy'  # The deployment queue

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.scheduling_queue)
        self.channel.queue_declare(queue=self.retrieve_queue)
        self.channel.queue_declare(queue=self.feature_queue)

        # consume all queues needed
        self.channel.basic_consume(
            queue=self.scheduling_queue, on_message_callback=self.trainingScheduleCallback, auto_ack=True)
        self.channel.basic_consume (
            queue=self.retrieve_queue, on_message_callback=self.trainingRetrievalCallback, auto_ack=True)
        self.channel.basic_consume(
            queue=self.feature_queue, on_message_callback=self.ingestionCallback, auto_ack=True)


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
            print('The body object could not be serialized: {}'.format(body))
            return

        if not self._validate_jobInput(info_obj):
            print('Body does not contain enough info on Job: {}'.format(body))
            return

        jobInput = JobInputModel(info_obj['label'],
                                 info_obj['version'],
                                 info_obj['sound_type'],
                                 ParameterInputModel(
                                     info_obj['parameters']['batch_size'],
                                     info_obj['parameters']['adam_learning_rate'],
                                     info_obj['parameters']['adam_beta'],
                                     info_obj['parameters']['lrelu_alpha'],
                                     info_obj['parameters']['episodes']
                                 ),
                                 info_obj['description']
                                 )
        jobDto = _jobService.createJob(jobInput)

        if jobDto:
            self.channel.basic_publish(exchange='', routing_key=self.ingestion_key, body=jobDto.json())

    def ingestionCallback(self, ch, method, props, body):
        print('Callback from feature engineering')
        try:
            info_obj = json.loads(body)
        except:
            #logger.error(__name__, 'body object is non json seriable: {}'.format(body))
            print('The body object could not be serialized: {}'.format(body))
            return

        if not self._validate_jobDto(info_obj):
            print('Body does not contain enough info on Job: {}'.format(body))
            return

        jobDto = JobDTO(info_obj['id'],
                        info_obj['label'],
                        info_obj['version'],
                        info_obj['date_time_start'],
                        info_obj['date_time_stop'],
                        info_obj['model_location'],
                        info_obj['record_location'],
                        info_obj['sound_type'],
                        info_obj['parameters'],
                        info_obj['status'],
                        info_obj['results'],
                        info_obj['description'])

        jobDto = _jobService.deployJob(jobDto)

        if jobDto:
            self.channel.basic_publish(exchange='', routing_key=self.training_key, body=jobDto.json(), properties=pika.BasicProperties(delivery_mode=2))


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

        print(info_obj)

        jobDto = JobDTO(info_obj['id'],
                        info_obj['label'],
                        info_obj['version'],
                        info_obj['date_time_start'],
                        info_obj['date_time_stop'],
                        info_obj['model_location'],
                        info_obj['record_location'],
                        info_obj['sound_type'],
                        info_obj['parameters'],
                        info_obj['status'],
                        info_obj['results'],
                        info_obj['description'])

        jobDto = _jobService.jobRetrieval(jobDto)


    def _validate_jobDto(self, jobDto):
        if not ('id' in jobDto and 'label' in jobDto and 'version' in jobDto and 'date_time_start' in jobDto and 'date_time_stop' in jobDto
                and 'model_location' in jobDto and 'record_location' in jobDto and 'sound_type' in jobDto and 'parameters' in jobDto and 'status' in jobDto):
            return False
        return True


    def _validate_jobInput(self, jobInput):
        if not ('label' in jobInput and 'description' in jobInput and 'version' in jobInput and 'sound_type' in jobInput and 'parameters' in jobInput):
            return False
        return True


    def consume(self):
        print('Controller started')
        self.channel.start_consuming()

if __name__ == '__main__':
    controller = Controller()
    controller.consume()



