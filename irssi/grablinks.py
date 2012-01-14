from flask import Flask, render_template
import re

app = Flask(__name__)

LOG_FILE = "/home/cdsboy/irclogs/Freenode/#reddit-anime.log"

def parse_lines(lines):
  links = []
  for line in lines:
    if re.match(r'\d{2}:\d{2} -!-', line):
      continue

    match = re.search(r'http://[-a-zA-Z0-9.?$%&/=_~#.,:;+]*', line)
    if match:
      timestamp = re.match(r'\d{2}:\d{2}', line).group(0)
      search = re.search(r'<.([^>]+)>', line)
      if search:
        username = search.group(1)
      else:
        username = None
      links.append({
        'timestamp' : timestamp,
        'user' : username,
        'link' : match.group(0)})
  return links

@app.route("/")
def show_links():
  links = []
  with open(LOG_FILE, 'r') as f:
    f.seek(0, 2)
    fsize = f.tell()
    f.seek(max(fsize-4000, 0), 0)

    links = parse_lines(f.readlines()[::-1])

  return render_template('show_links.html', links=links)

if __name__ == '__main__':
  app.run()
