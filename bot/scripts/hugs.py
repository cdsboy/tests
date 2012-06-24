#!/usr/bin/env python
"""
hugs.py - Jenni Hugs Module
Author: cdsboy
A Jenni Module to hand out hugs and other fun things
"""

from sayings import MOLEST_SAYINGS # a list of responses for molest
from tsun import tsunsay
import random
import re

@tsunsay()
def give_hug(jenni, input):
  if input.owner:
    jenni.me('gives %s a hug and a little something extra' % input.nick)
  else:
    jenni.me('hugs %s' % input.nick)
give_hug.commands = ['gimme hug']
give_hug.priority = 'high'

def give_kiss(jenni, input):
  if input.owner:
    jenni.me('kisses %s' % input.nick)
  else:
    jenni.say('%s my master told me to stay away from people like you.' % input.nick)
give_kiss.commands = ['gimme kiss', 'gimme kissu']
give_kiss.priority = 'high'

def molest(jenni, input):
  match = re.search(r'ACTION molests %s' % jenni.nick, input)
  if match:
    jenni.say(random.choice(MOLEST_SAYINGS))
molest.rule = r'(?u).*(molests)'
molest.priority = 'medium'

if __name__ == '__main__':
  print __doc__.strip()
