#!/usr/bin/env python
"""
niconico.py - Jenni NicoNico Module
Author: cdsboy
A Jenni Module to recognize niconico.jp links and print their titles
"""

from xml.etree.ElementTree import ElementTree
import urllib2
import re

def niconico_link_title(jenni, input):
  match = re.search(r'http://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    id = match.group(0).split('/')[-1]
    url = 'http://ext.nicovideo.jp/api/getthumbinfo/%s' % id
    req = urllib2.Request(url)
    try:
      resp = urllib2.urlopen(req)
      data = resp.read()
    except urllib2.HTTPError:
      return
    title = data[data.index('<title>')+len('<title>'):data.index('</title>')]
    jenni.say('NicoNico: %s' % title)
niconico_link_title.rule = r'(?u).*((?<!!)http://www\.nicovideo\.jp/watch/sm)|((?<!!)http://video\.niconico\.com/watch/sm)'
niconico_link_title.priority = 'high'

if __name__ = '__main__':
  print __doc__.strip()
