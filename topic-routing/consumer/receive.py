#!/usr/bin/env python
'''Job which consumes RabbitMQ queue messages from a topic exchange'''

import os
import sys
import json
import pika

def callback(ch, method, properties, body):
    '''listener callback function'''
    print("consumed message => " + str(body))

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

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# fetch list of routing keys
try:
    key_list = json.loads(os.environ['RMQ_ROUTINGKEYS'])
except (json.decoder.JSONDecodeError, Exception) as err:
    print(type(err).__name__)
    print(err)
    raise

for r_key in key_list:
    channel.queue_bind(
        exchange=rabbit_exchange, queue=queue_name, routing_key=r_key)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print("listening for messages ...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n consumer force stopped")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
        