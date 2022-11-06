#!/usr/bin/env python
'''Job which consumes RabbitMQ queue messages and responds with a correlation ID'''

import os
import sys
import math
import pika

def trig(angle):
    '''calculate sin and cos of the angle'''
    a_rad = math.radians(angle)
    return {"sin": math.sin(a_rad), "cos": math.cos(a_rad)}

def callback(ch, method, properties, body):
    '''listener callback function'''
    print("consumed message => " + str(body))
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=str(trig(float(body))))
    ch.basic_ack(delivery_tag=method.delivery_tag)

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

channel.queue_declare(queue='rpc_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=callback)

print("listening for messages ...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n consumer force stopped")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
