import math
import re

def parse(input_string):
  """ Returns a tuple of (amps, volts, watts, ohms) where any value that is not
      found will be None. """

  input_string = ' '.join(input_string.lower().split(' ')[1:])

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

def amps(jenni, input):
  data = parse(input)
  
  val = None
  if data[1] and data[2]:
    val = data[2] / data[1]
  elif data[1] and data[3]:
    val = data[1] / data[3]
  elif data[2] and data[3]:
    val = math.sqrt(data[2] / data[3])

  if val:
    jenni.say("Amps: %.2fa" % val)
amps.commands = ['amps']
amps.example = '!amps 4.2v 1.8o'

def volts(jenni, input):
  data = parse(input)
  
  val = None
  if data[0] and data[2]:
    val = data[0] / data[2]
  elif data[0] and data[3]:
    val = data[0] * data[3]
  elif data[2] and data[3]:
    val = math.sqrt(data[2] * data[3])

  if val:
    jenni.say("Volts: %.2fv" % val)
volts.commands = ['volts']
volts.example = '!volts 12w 1.8o'

def watts(jenni, input):
  data = parse(input)

  val = None
  if data[0] and data[1]:
    val = data[0] * data[1]
  elif data[0] and data[3]:
    val = (data[0] ** 2) * data[3]
  elif data[1] and data[3]:
    val = (data[1] ** 2) / data[3]

  if val:
    jenni.say("Watts: %.2fw" % val)
watts.commands = ['watts']
watts.example = '!watts 4.2v 1.8o'

def ohms(jenni, input):
  data = parse(input)
 
  val = None
  if data[0] and data[1]:
    val = data[1] / data[0]
  elif data[0] and data[2]:
    val = data[2] / (data[0] ** 2)
  elif data[1] and data[2]:
    val = (data[1] ** 2) / data[2]

  if val:
    jenni.say("Ohms: %.2fo" % val)
ohms.commands = ['ohms']
ohms.example = '!ohms 4.2v 2a'
