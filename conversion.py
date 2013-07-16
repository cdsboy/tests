import re

are = re.compile(r'(?!-)([0-9.]+)a(mps)?')
vre = re.compile(r'(?!-)([0-9.]+)v(olts)?')
wre = re.compile(r'(?!-)([0-9.]+)w(atts)?')
ore = re.compile(r'(?!-)([0-9.]+)o(hms)?')

def parse(input_string):
  """ Returns a tuple of (amps, volts, watts, ohms) where any value that is not
      found will be None. """

  asearch = are.search(input_string)
  amps = None
  if asearch:
    amps = float(asearch.group(1))
  
  vsearch = vre.search(input_string)
  volts = None
  if vsearch:
    volts = float(vsearch.group(1))

  wsearch = wre.search(input_string)
  watts = None
  if wsearch:
    watts = float(wsearch.group(1))

  osearch = ore.search(input_string)
  ohms = None
  if osearch:
    ohms = float(osearch.group(1))

  return amps, volts, watts, ohms

def test():
  print parse("!watts 4.2volts .8o")
  print parse("!volts 5a .8o")
  print parse("!amps 12w .8v")

if __name__ == '__main__':
  test()
