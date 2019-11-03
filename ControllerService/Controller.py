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
        self.feature_queue = 'gan.training.features'

        # Publish keys
        self.training_key = 'gan.train.GPU'
        self.ingestion_key = 'gan.train.ingestion'
        self.deployment_key = 'gan.training.deploy'  # The deployment queue

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.scheduling_queue, durable=True)
        self.channel.queue_declare(queue=self.retrieve_queue, durable=True)
        self.channel.queue_declare(queue=self.feature_queue, durable=True)

        # consume all queues needed
        self.channel.basic_consume(
            queue=self.scheduling_queue, on_message_callback=self.trainingScheduleCallback, auto_ack=True)
        self.channel.basic_consume(
            queue=self.retrieve_queue, on_message_callback=self.trainingRetrievalCallback, auto_ack=True)
        self.channel.basic_consume(
            queue=self.feature_queue, on_message_callback=self.featureEngineeringCallback, auto_ack=True)


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

        jobInput = JobInputModel(info_obj['version'] ,info_obj['sound_type'], ParameterInputModel(info_obj['parameters']['batch_size'], info_obj['parameters']['noise_dim']))
        jobDto = _jobService.createJob(jobInput)

        if jobDto:
            #self.channel.basic_publish(exchange='', routing_key=self.training_key, body=jobDto.json())
            print(jobDto.__dict__())
            self.channel.basic_publish(exchange='', routing_key=self.ingestion_key, body=jobDto.json())


    def featureEngineeringCallback(self, ch, method, props, body):
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
                        info_obj['model_location'], info_obj['data_location'], info_obj['sound_type'], info_obj['parameters'], info_obj['status'])

        jobDto = _jobService.deployJob(jobDto)

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
                        info_obj['model_location'], info_obj['data_location'], info_obj['sound_type'], info_obj['parameters'], info_obj['status'])

        jobDto = _jobService.jobRetrieval(jobDto)

        if jobDto:
            self.channel.basic_publish(exchange='', routing_key=self.deployment_key, body=jobDto.json())


    def _validate_jobDto(self, jobDto):
        if not ('id' in jobDto and 'version' in jobDto and 'date_time_start' in jobDto and 'date_time_stop' in jobDto
                and 'model_location' in jobDto and 'data_location' in jobDto and 'sound_type' in jobDto and 'parameters' in jobDto and 'status' in jobDto):
            return False
        return True


    def _validate_jobInput(self, jobInput):
        if not ('version' in jobInput and 'sound_type' in jobInput and 'parameters' in jobInput):
            return False
        return True


    def consume(self):
        print('Controller started')
        self.channel.start_consuming()

if __name__ == '__main__':
    controller = Controller()
    controller.consume()



