import pika
import json
from os import environ


from Services.TrainingService.TrainingService import train

RABBIT = environ['RHOST']
RABBIT_USER = environ['RUSER']
RABBIT_PASS = environ['RPASS']
RABBIT_VHOST = environ['RVHOST']

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT, 5672, RABBIT_VHOST, credentials, heartbeat=0))
channel = connection.channel()

# The queues
training_queue = 'gan.training.CPU'

# Publish keys
retrieval_key = 'gan.training.retrieval'


# Declare the queue, if it doesn't exist
channel.queue_declare(queue=training_queue)
channel.queue_declare(queue=retrieval_key)


def trainingCallback(ch, method, props, body):

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
    except Exception:
        #logger.error(__name__, 'body object is non json seriable: {}'.format(body))
        print('The body object could not be serialized: {}'.format(body))
        return
    print(info_obj)

    results, model_location = train(info_obj)

    info_obj['results'] = results
    info_obj['model_location'] = model_location
    channel.basic_publish(exchange='', routing_key=retrieval_key, body=json.dumps(info_obj))


# consume all queues needed
channel.basic_consume(
        queue=training_queue, on_message_callback=trainingCallback, auto_ack=True)



if __name__ == '__main__':
    channel.start_consuming()

