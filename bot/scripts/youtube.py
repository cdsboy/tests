#!/usr/bin/env python
"""
youtube.py - Jenni Youtube Module
Author: cdsboy
A Jenni Module to recognize youtube links and print their titles
"""

from gdata.service import RequestError
from tsun import tsunsay
import gdata.youtube.service
import urlparse
import re

yt_service = gdata.youtube.service.YouTubeService()

EXCLUSION_CHAR = '!'

@tsunsay()
def youtube_link_title(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    try:
      url_data = urlparse.urlparse(match.group(0))
      query = urlparse.parse_qs(url_data.query)
      try:
        entry = yt_service.GetYouTubeVideoEntry(video_id=query["v"][0])
      except:
        return
      jenni.say("Youtube: %s" % entry.media.title.text)
    except RequestError:
      pass
youtube_link_title.rule = r'(?u).*((?<!!)https?://www\.youtube\.com)'
youtube_link_title.priority = 'high'

@tsunsay()
def youtube_shortlink_title(jenni, input):
  match = re.search(r'https?://youtu.be/[A-Za-z0-9\-_]*', input)
  if match:
    try:
      id = match.group(0).split('/')[-1]
      entry = yt_service.GetYouTubeVideoEntry(video_id=id)
      jenni.say("Youtube: %s" % entry.media.title.text)
    except RequestError:
      pass
youtube_shortlink_title.rule = r'(?u).*((?<!!)https?://youtu\.be)'
youtube_shortlink_title.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
