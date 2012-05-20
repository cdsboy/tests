#!/usr/bin/env python
"""
mal.py - Jenni MyAnimeList Module
Author: cdsboy
A Jenni Module to search MyAnimeList.Net
"""

from tsun import tsunsay
import urllib2
import urllib
import json

DISPLAY_NUM = 4

def mal_url(id):
  return 'http://myanimelist.net/anime/%s/' % id

@tsunsay()
def mal_search(jenni, input):
  title = input[len('.malsearch '):]
  data = urllib.urlencode({'q' : title})
  req = urllib2.Request('http://mal-api.com/anime/search?%s' % data)
  try:
    resp = urllib2.urlopen(req)
    info = json.loads(resp.read())

    if not info:
      jenni.say('No matching anime found.')
      return

    match = False
    for anime in info:
      if anime['title'] == title:
        print anime['title']
        match = anime

    print match

    if match:
      jenni.say('%s: %s' % (match['title'], mal_url(match['id'])))
    else:
      for anime in info[:DISPLAY_NUM]:
        jenni.say('%s: %s' % (anime['title'], mal_url(anime['id'])))
  except urllib2.HTTPError:
    jenni.say('Sorry, there was an error performing your search.')
mal_search.commands = ['malsearch']
mal_search.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
