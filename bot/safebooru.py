#!/usr/bin/env python
"""
safebooru.py - Jenni Safebooru Module
Author: cdsboy
A Jenni Module to do various things with safebooru
"""

from bs4 import BeautifulSoup
import urllib2
import urllib
import random

TAGS = {
    'loli' : 'loli',
    'oppai' : 'cleavage',
    'pantsu' : 'pantsu',
}

def get_tag(jenni, input):
  tag = input[len('.gimmie '):]
  url = 'http://safebooru.org/index.php?page=post&s=list&tags=%s&pid=%d' % (TAGS[tag], random.randint(0,2500))
  req = urllib2.Request(url)
  try:
    resp = urllib2.urlopen(req)
  except urllib2.HTTPError:
    jenni.say("No %s for you!" % tag)

  soup = BeautifulSoup(resp.read())
  url = random.choice(soup.select("span.thumb a")).get("href")
  jenni.say('Your %s: http://safebooru.org/%s' % (tag, url))
get_tag.commands = ['gimmie %s' % tag for tag in TAGS.keys()]
get_tag.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
