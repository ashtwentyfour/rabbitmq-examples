#!/usr/bin/env python
'''Job which consumes RabbitMQ queue messages'''

import os
import sys
import time
import pika

def callback(ch, method, properties, body):
    '''listener callback function'''
    print("consumed message => " + str(body))
    n_integers = sum(i.isdigit() for i in list(set(list(str(body)))))
    time.sleep(n_integers)
    print("processing completed ...")
    ch.basic_ack(delivery_tag=method.delivery_tag)


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

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=routing_key, on_message_callback=callback)

print("listening for messages ...")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n consumer force stopped")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
