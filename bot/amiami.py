#!/usr/bin/env python
"""
amiami.py - Jenni AmiAmi.com Module
Author: cdsboy
A Jenni Module to recognize AmiAmi.com links and list the item's name and price
"""

from bs4 import BeautifulSoup
from tsun import tsunsay
import urllib2
import re

@tsunsay()
def get_amiami_info(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    req = urllib2.Request(match.group(0))
    try:
      resp = urllib2.urlopen(req)
    except urllib2.HTTPError:
      return
    soup = BeautifulSoup(resp.read())
    try:
      title = re.search(r'<h2 class="heading_10">(.+)<br/>',
                        str(soup.select("h2.heading_10")[0])).group(1)
      price = re.search(r'<li.+>(<span.+>.+</span>)?(.+)</li>',
                        str(soup.select("li.price")[0])).group(2)
    except IndexError:
      return
    print price
    print title
    jenni.say('AmiAmi: %s Price: %s' % (title, price))
get_amiami_info.rule = r'(?u).*((?<!!)https?://www\.amiami\.com/top/detail)'
get_amiami_info.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
