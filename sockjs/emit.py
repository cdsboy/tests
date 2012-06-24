#!/user/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
  host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='links', type='fanout')

message = ' '.join(sys.argv[:]) or "info: hello World!"
channel.basic_publish(exchange='links',
                      routing_key='',
                      body=message)
connection.close()
