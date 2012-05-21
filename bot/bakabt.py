#!/usr/bin/env python
"""
bakabt.py - Jenni bababt.me Module
Author: cdsboy
A Jenni Module to recognize bakabt.me links and list their torrent titles
"""

from bs4 import BeautifulSoup
from tsun import tsunsay
import urllib2
import re

@tsunsay()
def get_bakabt_info(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    req = urllib2.Request(match.group(0))
    try:
      resp = urllib2.urlopen(req)
    except urllib2.HTTPError:
      return
    soup = BeautifulSoup(resp.read())
    try:
      title = str(soup.select("#description_title")[0].contents[1])
      title = re.sub(r'<.+>', r'', title)
    except IndexError:
      return
    jenni.say('Bakabt: %s' % title)
get_bakabt_info.rule = r'(?u).*((?<!!)https?://(www\.)?bakabt\.(me)|(com)/[0-9]+-)'
get_bakabt_info.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
