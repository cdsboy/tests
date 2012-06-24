#!/usr/bin/env python
"""
nyaa.py - Jenni Nyaa.eu Module
Author: cdsboy
A Jenni Module to recognize nyaa.eu links and list their torrent titles
"""

from bs4 import BeautifulSoup
from tsun import tsunsay
import urllib2
import re

@tsunsay()
def get_nyaa_info(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    req = urllib2.Request(match.group(0))
    try:
      resp = urllib2.urlopen(req)
    except urllib2.HTTPError:
      return
    soup = BeautifulSoup(resp.read())
    try:
      raw = str(soup.select(".tinfotorrentname")[0])
      title = re.search(r'<td class="tinfotorrentname">(.+)</td>', raw).group(1)
    except IndexError:
      return
    jenni.say('Nyaa: %s' % title)
get_nyaa_info.rule = r'(?u).*((?<!!)https?://(www\.)?nyaa.eu/\?page=torrentinfo)'
get_nyaa_info.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
