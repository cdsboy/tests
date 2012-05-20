#!/usr/bin/env python
"""
gelbooru.py - Jenni Gelbooru Module
Author: cdsboy
A Jenni Module to reconginze Gelbooru links and warn users if they contain certain tags
"""

from tsun import tsunsay
import urllib2
import re

WARN_TAGS = ['futanari', 'guro', 'yaoi', 'moth']

@tsunsay()
def get_gelbooru_tags(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    req = urllib2.Request(match.group(0))
    try:
      resp = urllib2.urlopen(req)
    except urllib2.HTTPError:
      return
    data = resp.read()
    found_tags = []
    for tag in WARN_TAGS:
      try:
        if data.index(tag) != -1:
          found_tags.append(tag)
      except ValueError:
        pass

    if found_tags:
      jenni.say('Warning: %s!' % ', '.join(found_tags))
get_gelbooru_tags.rule = r'(?u).*((?<!!)https?://(www\.)?gelbooru\.com/index\.php\?page=post)'
get_gelbooru_tags.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
