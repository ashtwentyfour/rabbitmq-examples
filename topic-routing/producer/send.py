#!/usr/bin/env python
'''Job which sends messages to RabbitMQ via the topic exchange'''

import json
import os
import string
import sys
import random
import pika

try:
    n_messages = int(sys.argv[2])
    r_key = sys.argv[1]
except IndexError as ierr:
    print(ierr)
    raise
except (ValueError, Exception) as err:
    print(err)
    raise

# credentials
rabbit_user = os.getenv("RMQ_USER")
rabbit_password = os.getenv("RMQ_PASSWORD")
# topic exchange name
rabbit_exchange = os.getenv("RMQ_EXCHANGE") or 'topicex01'

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

channel.exchange_declare(exchange=rabbit_exchange, exchange_type='topic')

# send messages
COUNT = 0
while COUNT < n_messages:
    message = {
        'id': COUNT,
        'data': ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
    }
    channel.basic_publish(exchange=rabbit_exchange, routing_key=r_key, body=json.dumps(message))
    print("sent message # " + str(COUNT) + " => " + json.dumps(message))
    COUNT += 1
connection.close()
