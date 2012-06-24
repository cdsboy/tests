from sayings import TSUN_SAYINGS
import random

def tsunsay(chance=20):
  def wrap(f):
    def wrapped_f(*args, **kwargs):
      f(*args, **kwargs)
      if random.randint(0, chance) == 0:
        args[0].say(random.choice(TSUN_SAYINGS))
    return wrapped_f
  return wrap
