import tornado.ioloop
import tornado.web

import sockjs.tornado

import threading
import pika
import uuid
import time

RABBIT_SERVER = 'localhost'

class RabbitConsumer(threading.Thread):
  def __init__(self, t_client):
    self.t_client = t_client
    self.key = t_client.id
    self.connection = None
    self.last_active = time.time()
    self.started = time.time()
    self._stop = threading.Event()

    threading.Thread.__init__(self)

  def stop(self):
    self._stop.set()

  def stopped(self):
    print "stopped %s" % self.key
    return self._stop.isSet()

  def on_connected(self, connection):
    self.last_active = time.time()
    connection.channel(self.on_channel_open)
    self.connection = connection

  def on_channel_open(self, new_channel):
    self.last_active = time.time()
    self.channel = new_channel

    self.channel.exchange_declare(exchange='links', type='fanout')

    self.channel.queue_declare(queue=self.key, durable=True,
        exclusive=True, auto_delete=False, callback=self.on_queue_declared)
    self.channel.queue_bind(exchange='links', queue=self.key)
      
  def on_queue_declared(self, frame):
    self.last_active = time.time()
    self.channel.queue_bind(exchange='links', queue=self.key)
    self.channel.basic_consume(self.handle_delivery, queue=self.key)

  def kill_me(self, clear = False):
    if clear:
      self.channel.queue_delete(queue=self.key)

    self.connection.close()
    self.stop()

  def handle_delivery(self, channel, header, method, body):
    self.last_active = time.time()
    if body == "die":
      self.kill_me()
    else:
      self.t_client.send(body)

  def startCall(self):
    print "Starting %s" % self.key
    self.last_active = time.time()
    connection = pika.SelectConnection(pika.ConnectionParameters(
        host=RABBIT_SERVER), self.on_connected)

    connection.ioloop.start()

  def run(self):
    self.startCall()

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render('index.html')

class LinkConnection(sockjs.tornado.SockJSConnection):
  def __init__(self, session):
    self.id = str(uuid.uuid1())

    self.consumer = RabbitConsumer(self)
    self.consumer.start()

    sockjs.tornado.SockJSConnection.__init__(self, session)

  def close(self):
    if self.consumer:
      self.consumer.kill_me()
    sockjs.tornado.SockJSConnection.close(self)

  def on_message(self, message):
    pass
  
if __name__ == "__main__":
  LinkRouter = sockjs.tornado.SockJSRouter(LinkConnection, '/link')

  app = tornado.web.Application(
      [(r"/", IndexHandler)] + LinkRouter.urls
  )

  app.listen(8080)

  tornado.ioloop.IOLoop.instance().start()
