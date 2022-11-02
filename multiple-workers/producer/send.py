#!/usr/bin/env python
'''Job which sends messages to RabbitMQ via the default exchange'''

import json
import os
import string
import sys
import random
import pika

try:
    n_messages = int(sys.argv[1])
except IndexError as ierr:
    print(ierr)
    raise
except (ValueError, Exception) as err:
    print(err)
    raise

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

channel.queue_declare(queue=routing_key, durable=True)

# send messages
COUNT = 0
while COUNT < n_messages:
    message = {
        'id': COUNT,
        'data': ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
    }
    channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print("sent message # " + str(COUNT) + " => " + json.dumps(message))
    COUNT += 1
connection.close()
