#!/usr/bin/env python
'''Job which subscribes to RabbitMQ messages'''

import os
import sys
import pika

def callback(ch, method, properties, body):
    '''listener callback function'''
    print("consumed message => " + str(body))

# credentials
rabbit_user = os.getenv("RMQ_USER")
rabbit_password = os.getenv("RMQ_PASSWORD")
# fanout exchange name
rabbit_exchange = os.getenv("RMQ_EXCHANGE") or 'fanout01'

# connection specs
credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RMQ_HOST") or 'localhost',
                                5672,
                                os.getenv("RMQ_VHOST") or '/',
                                credentials=credentials))
    channel = connection.channel()
except (pika.exceptions.AMQPConnectionError, Exception) as err:
    print(type(err).__name__)
    print(err)
    raise

channel.exchange_declare(exchange=rabbit_exchange, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=rabbit_exchange, queue=queue_name)

print("listening for messages ...")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n consumer force stopped")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
        