import pika
import json
from os import environ

class MQService:

    def __init__(self):

        # TODO: Change from config file over to os.environment
        RABBIT = environ['RHOST']
        RABBIT_USER = environ['RUSER']
        RABBIT_PASS = environ['RPASS']
        RABBIT_VHOST = environ['RVHOST']

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials))
        self.channel = self.connection.channel()

        # Queue key
        self.training_key = 'gan.training.schedule'

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.training_key, durable=True)


    def sendTrainingMessage(self, jobDto):
        self.channel.basic_publish(exchange='', routing_key=self.training_key, body=json.dumps(jobDto))



