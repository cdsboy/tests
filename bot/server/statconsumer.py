import couchdbkit
import datetime
import pika
import uuid

connection = None
channel = None
couchkit = None

class Line(object):
  def __init__(self, couchkit):
    self._couchkit = couchkit

    self.id     = None
    self.type   = 'line'
    self.author = None
    self.body   = None
    self.sent   = None

  def new(self, author, body, sent):
    self.id     = '%s-%s' % (self.type, uuid.uuid1())
    self.author = author
    self.body   = body
    self.sent   = sent

  def deserialize(self, doc):
    self.id     = doc['_id']
    self.author = author
    self.body   = body
    datetime    = doc['sent']
    date_list   = [int(i) for i in re.split(r"[-\s:.]", date_str)]
    self.sent   = datetime.datetime(*date_list)

  def serialize(self):
    doc = {
        '_id'    : self.id,
        'type'   : self.type
        'author' : self.author,
        'body'   : self.body,
        'sent'   : self.sent.isoformat(sep=' '),
    }
    return doc
  
  def load(self, id):
    raw = self._couchkit.get(id)
    self.deserialize(raw)

  def save(self):
    raw = self.serialize()
    self._couchkit.save_doc(raw, force_update=True)


class Stat(object):
  def __init__(self, couchkit):
    self._couchkit = couchkit

    self.id       = None
    self.type     = 'stat'
    self.username = None
    self.lines    = 0
    self.seen     = None

  def new(self, username):
    self.id = '%s-%s' % (self.type, uuid.uuid1())
    self.username = username
    self.seen = datetime.datetime.utcnow()

  def update(self, seen):
    self.lines += 1
    self.seen = seen

  def deserialize(self, doc):
    self.id       = doc['_id']
    self.username = doc['username']
    self.lines    = doc['lines']
    datetime      = doc['seen']
    date_list     = [int(i) for i in re.split(r"[-\s:.]", date_str)]
    self.seen     = datetime.datetime(*date_list)

  def serialize(self):
    doc = {
        '_id'      : self.id,
        'type'     : self.type,
        'username' : self.username,
        'lines'    : self.lines,
        'seen'     : self.seen.isoformat(sep=' '),
    }
    return doc
  
  def load(self, id):
    raw = self._couchkit.get(id)
    self.deserialize(raw)

  def load_or_create(self, username):
    try:
      result = self._couchkit.view("stats/all", reduce=False,
                                   startkey=username, endkey=username).one()
      self.deserialize(result)
    except NoResultFound:
      self.new(username)

  def save(self):
    raw = self.serialize()
    self._couchkit.save_doc(raw, force_update=True)

def on_connected(connection):
  global channel
  connection.channel(on_channel_open)

def on_channel_open(channel_):
  global channel
  channel = channel_
  channel.exchange_declare(exchange="stats", type="fanout",
                           callback=on_exchange_declared)

def on_exchange_declared(frame):
  channel.queue_declare(queue="couchstats", durable=True, exclusive=False,
                        auto_delete=False, callback=on_queue_declared)

def on_queue_declared(frame):
  channel.queue_bind(queue="couchstats", exchange="stats",
                     callback=on_queue_bind)

def on_queue_bind(frame):
  channel.basic_consume(handle_delivery, queue="couchstats")

def handle_delivery(channel, method_frame, header_frame, body):
  stat = Stat(couchkit)
  stat.load_or_create(body['author'])
  stat.update(body['timestamp'])
  stat.save()

  line = Line(couchkit)
  line.new(body['author'], body['body'], body['timestamp'])
  line.save()

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
   
