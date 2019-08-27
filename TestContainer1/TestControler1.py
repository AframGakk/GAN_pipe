import pika
import os

RABBIT = os.environ['RABBIT']

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
channel = connection.channel()

cont2_routing = 'Container2_queue'
cont1_queue = 'Container1_queue'

channel.queue_declare(queue=cont1_queue, durable=True)


def callback(ch, method, properties, body):
    print('Called with: ', body)


channel.basic_consume(queue=cont1_queue, on_message_callback=callback, auto_ack=True)

channel.basic_publish(exchange='', routing_key=cont2_routing, body='Hello im container 1')

channel.start_consuming()


