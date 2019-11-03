import pika
import json
from os import environ

from services.FeatureEngineeringService.FeatureEngineeringService import FeatureEngineeringService

_fService = FeatureEngineeringService()

class FeatureController:

    def __init__(self):
        RABBIT = 'localhost'#environ['RHOST']
        RABBIT_USER = 'guest'#environ['RUSER']
        RABBIT_PASS = 'guest'#environ['RPASS']
        RABBIT_VHOST = '/'#environ['RVHOST']

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials))
        self.channel = self.connection.channel()

        # Queues
        self.feature_queue = 'gan.training.features'

        # Keys
        self.controller_key = 'gan.training.features.controller'

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.feature_queue, durable=True)
        self.channel.queue_declare(queue=self.controller_key, durable=True)

        self.channel.basic_consume(
            queue=self.feature_queue, on_message_callback=self.ingestionCallback, auto_ack=True)


    def ingestionCallback(self, ch, method, properties, body):
        print('Feature Callback')
        try:
            training_info = json.loads(body)
        except:
            print('Body is not json serializable')

        _fService.transformFeatures(training_info['sound_type'], training_info['version'])
        self.channel.basic_publish(exchange='', routing_key=self.controller_key, body=body)



    def consume(self):
        print('Feature Controller started')
        self.channel.start_consuming()

if __name__ == '__main__':
    controller = FeatureController()
    controller.consume()