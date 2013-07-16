import re

are = re.compile(r'([0-9.\-]+)a(mps)?')
vre = re.compile(r'([0-9.\-]+)v(olts)?')
wre = re.compile(r'([0-9.\-]+)w(atts)?')
ore = re.compile(r'([0-9.\-]+)o(hms)?')

def parse(input_string):
  """ Returns a tuple of (amps, volts, watts, ohms) where any value that is not
      found will be None. """
  
  data = {
      'amps': are.search(input_string),
      'volts': vre.search(input_string),
      'watts': wre.search(input_string),
      'ohms': ore.search(input_string)
  }
  for key, val in data.iteritems():
    if val:
      val = float(val.group(1))
      if val > 0:
        data[key] = val
      else:
        data[key] = None
  
  return data['amps'], data['volts'], data['watts'], data['ohms']

def test():
  print parse("!watts 4.2volts .8o")
  print parse("!volts 5a .8o")
  print parse("!amps 12w .8v")
  print parse("!amps -12w .8v")

if __name__ == '__main__':
  test()
