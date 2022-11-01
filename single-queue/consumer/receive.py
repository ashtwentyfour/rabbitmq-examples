#!/usr/bin/env python
'''Job which sends messages to RabbitMQ via the default exchange'''

import os
import sys
import pika

def callback(ch, method, properties, body):
    '''listener callback function'''
    print("consumed message => " + str(body))

# credentials
rabbit_user = os.getenv("RMQ_USER")
rabbit_password = os.getenv("RMQ_PASSWORD")
# routing key matches queue name for default exchange
routing_key = os.getenv("RMQ_QUEUE") or 'queue01'

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

channel.queue_declare(queue=routing_key)

channel.basic_consume(queue=routing_key, on_message_callback=callback, auto_ack=True)

print("listening for messages ...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n consumer force stopped")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
