import pika
from pika.exceptions import StreamLostError
import json
import os
import traceback

from Services.DataIngestionService import DataIngestionService
from Services.Log.Log import Log

logger = Log(file_handler=True, file='./logs/logs.log')
ingestionService = DataIngestionService()


class IngestionController:

    def __init__(self):
        RABBIT = os.environ['RABBIT']
        RABBIT_USER = os.environ['RABBIT_USER']
        RABBIT_PASS = os.environ['RABBIT_PASS']

        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, '/', credentials))
        self.channel = self.connection.channel()
        self.ingestion_queue = 'ml.raw_ingest'
        self.feature_queue = 'ml.feature_service'

        # Declare the queue, if it doesn't exist
        self.channel.queue_declare(queue=self.ingestion_queue, durable=True)
        self.channel.basic_consume(queue=self.ingestion_queue, on_message_callback=self.RawIngestionCallback, auto_ack=True)

    def consume(self):

        logger.info(__name__, 'Ingestion Service has started')
        self.channel.start_consuming()

    def RawIngestionCallback(self, ch, method, properties, body):
        try:
            body_obj = json.loads(body)
        except Exception as ex:
            logger.error(__name__, 'Body is not json compatable in broker callback')
            return

        ingestionService.convertRawToRecordDataLocal()

        self.channel.basic_publish(exchange='', routing_key=self.feature_queue, body=body)

if __name__ == '__main__':
    controller = IngestionController()
    #controller.consume()

    try:
        controller.consume()
    except StreamLostError:
        logger.error(__name__, 'Error with AMQP stream connection, shutting down!')
        controller.connection.close()
    except KeyboardInterrupt:
        logger.info(__name__, 'manually closed ingestion service, goodbye!')
        controller.connection.close()
    except Exception as e:
        logger.error(__name__, 'Error in Ingestion controller', exception=e)
    else:
        logger.error(__name__, 'Unknown Error in Ingestion controller', exception=traceback.print_exc())

