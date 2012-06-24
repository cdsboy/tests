from urlparse import urlparse
from datetime import datetime
import json
import re

def handle_link(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    info = urlparse(match.group(0))
    data = {
        'author': input.sender,
        'site': info.netloc,
        'title': 'blah',
        'link': match.group(0),
        'datetime': datetime.utcnow().isoformat(sep=' '),
        'sfw': True,
    }
    jenni.queue(json.dumps(data))
handle_link.rule = r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*'
handle_link.priority = 'high'
