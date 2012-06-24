#!/usr/bin/env python
"""
reddit.py - Jenni Reddit Module
Author: cdsboy
A Jenni Module to recognize reddit links and print their titles
"""

from tsun import tsunsay
from reddit.objects import Submission
from reddit import Reddit
import re

r = Reddit(user_agent="Jenni Irc Bot")

@tsunsay()
def reddit_link_title(jenni, input):
  match = re.search(r'https?://[-a-zA-Z0-9.?$!%&/=_~#.,:;+]*', input)
  if match:
    try:
      info = Submission.get_info(r, match.group(0))
    except ValueError:
      return
    jenni.say('Reddit: %s' % info.title)
reddit_link_title.rule = r'(?u).*((?<!!)https?://www\.reddit\.com/r/[A-Za-z0-0]+/comments/)'
reddit_link_title.priority = 'high'

if __name__ == '__main__':
  print __doc__.strip()
