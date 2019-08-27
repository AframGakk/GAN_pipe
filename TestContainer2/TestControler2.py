import pika
import os

RABBIT = os.environ['RABBIT']

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT))
channel = connection.channel()

cont2_queue = 'Container2_queue'
cont1_routing = 'Container1_queue'

channel.queue_declare(queue=cont2_queue, durable=True)


def callback(ch, method, properties, body):
    print('Called with: ', body)
    answer = 'Hello im container number 2'
    channel.basic_publish(exchange='', routing_key=cont1_routing, body=answer)


channel.basic_consume(queue=cont2_queue, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


