import re

def parse(input_string):
  """ Returns a tuple of (amps, volts, watts, ohms) where any value that is not
      found will be None. """
  
  data = {
      'amps':  re.search(r'([0-9.\-]+)a(mps)?', input_string),
      'volts': re.search(r'([0-9.\-]+)v(olts)?', input_string),
      'watts': re.search(r'([0-9.\-]+)w(atts)?', input_string),
      'ohms':  re.search(r'([0-9.\-]+)o(hms)?', input_string)
  }
  for key, val in data.iteritems():
    if val:
      val = float(val.group(1))
      data[key] = val if val > 0 else None
  
  return data['amps'], data['volts'], data['watts'], data['ohms']

def test():
  print parse("!watts 4.2volts .8o")
  print parse("!volts 5a .8o")
  print parse("!amps 12w .8v")
  print parse("!amps -12w .8v")

if __name__ == '__main__':
  test()
