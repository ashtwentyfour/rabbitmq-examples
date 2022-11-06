#!/usr/bin/env python
'''Remote Procedure Call (RPC) Client for RabbitMQ'''

import json
import os
import string
import sys
import random
import pika

try:
    angle = sys.argv[1]
except IndexError as ierr:
    print(ierr)
    raise
except (ValueError, Exception) as err:
    print(err)
    raise

CORRELATION_ID = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))
print("CORRELATION_ID = " + CORRELATION_ID)

def validate_response(ch, method, properties, body):
    '''check correlation ID'''
    if CORRELATION_ID == properties.correlation_id:
        print("response = " + str(body))

# credentials
rabbit_user = os.getenv("RMQ_USER")
rabbit_password = os.getenv("RMQ_PASSWORD")

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

# set callback queue
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
print("callback queue = " + callback_queue)
# consume response from server and validate result
channel.basic_consume(queue=callback_queue, on_message_callback=validate_response, auto_ack=True)

# send a message with corrleation ID and callback queue details
channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=CORRELATION_ID
            ),
            body=angle)
connection.process_data_events(time_limit=None)
