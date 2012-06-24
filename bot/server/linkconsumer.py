import couchdbkit
import pika
import uuid

connection = None
channel = None
couchkit = None

class Link(object):
  def __init__(self, couchkit):
    self._couchkit = couchkit

    self.id       = None
    self.type     = 'link'
    self.author   = None
    self.site     = None
    self.title    = None
    self.link     = None
    self.datetime = None
    self.sfw      = None

  def new(self, author, site, title, link, date, sfw=True):
    self.id       = "%s-%s" % (self.type, uuid.uuid1())
    self.author   = author
    self.site     = site
    self.title    = title
    self.link     = link
    if isinstance(date, str):
      date_list     = [int(i) for i in re.split(r"[-\s:.]", date)]
      self.datetime = datetime.datetime(*date_list)
    else:
      self.datetime = date
    self.sfw      = sfw

  def deserialize(self, doc):
    self.id       = doc['_id']
    self.author   = doc['author']
    self.site     = doc['site']
    self.title    = doc['title']
    self.link     = doc['link']
    datetime      = doc['datetime']
    date_list     = [int(i) for i in re.split(r"[-\s:.]", date_str)]
    self.datetime = datetime.datetime(*date_list)
    self.sfw      = doc['sfw']

  def serialize(self):
    doc = {
        '_id'      : self.id,
        'type'     : self.type,
        'author'   : self.author,
        'site'     : self.site,
        'title'    : self.title,
        'link'     : self.link,
        'datetime' : self.datetime.isoformat(sep=' '),
        'sfw'      : self.sfw,
    }
    return doc
  
  def load(self, id):
    raw = self._couchkit.get(id)
    self.deserialize(raw)

  def save(self):
    raw = self.serialize()
    self._couchkit.save_doc(raw, force_update=True)

def on_connected(connection):
  global channel
  connection.channel(on_channel_open)

def on_channel_open(channel_):
  global channel
  channel = channel_
  channel.exchange_declare(exchange="links", type="fanout",
                           callback=on_exchange_declared)

def on_exchange_declared(frame):
  channel.queue_declare(queue="couch", durable=True, exclusive=False,
                        auto_delete=False, callback=on_queue_declared)

def on_queue_declared(frame):
  channel.queue_bind(queue="couch", exchange="links",
                     callback=on_queue_bin)

def on_queue_bind(frame):
  channel.basic_consume(handle_delivery, queue="couch")

def handle_delivery(channel, method_frame, header_frame, body):
  link = Link(couchkit)
  link.new(**body)
  link.save()
  channel.basic_ack(delivery_tag=method_frame.delivery_tag)

if __name__ == '__main__':
  server = couchdbkit.Server()
  couchkit = server.get_or_create_db("links")

  connection = pika.SelectConnection(pika.ConnectionParameters('127.0.0.1'))
  try:
    connection.ioloop.start()
  except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
   
