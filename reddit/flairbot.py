from urlparse import urlparse
import cookielib
import urllib2
import urllib
import json

REDDIT = "http://www.reddit.com"
SUBREDDIT = "anime"
CREDENTIALS = {'user': "botusernamegoeshere", 'passwd': "botpassgoeshere"}
USER_AGENT = "Simple Reddit Flair Bot"

ACCEPTED_SITES = ["www.myanimelist.net", "myanimelist.net"]
SITE_CSS = {
    "www.myanimelist.net": "flair-MAL",
    "myanimelist.net": "flair-MAL",
}

def reddit_api(action, params=None): 
  if params:
    req = urllib2.Request(REDDIT + action, urllib.urlencode(params))
  else:
    req = urllib2.Request(REDDIT + action)
  response = urllib2.urlopen(req)
  return json.loads(response.read())

def main():
  cookies = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
  opener.addheaders = [('User-agent', USER_AGENT)]
  urllib2.install_opener(opener)
  # Login to Reddit API
  reddit_api("/api/login", CREDENTIALS)
  successful = False
  for cookie in cookies:
    if cookie.name == 'reddit_session':
      successful = True
  if not successful:
    print "Login failure"
    exit(1)
  # Obtain unread messages
  unread = reddit_api("/message/unread/.json")
  modhash = unread['data']['modhash']
  read = []
  csv = ""
  # Iterate though messages
  messages = unread['data']['children']
  cmp_by_time = lambda x, y: cmp(x['data']['created'], y['data']['created'])
  for message in sorted(messages, cmp_by_time):
    read.append(message['data']['name'])
    # Determine if valid flair
    if message['data']['subject'].lower() == "flair":
      user = message['data']['author']
      url = message['data']['body']
      if not url.startswith("http://") or not url.startswith("https://"):
        url = "http://" + url
      parsed = urlparse(url)
      if parsed.netloc in ACCEPTED_SITES:
        csv += "%s,%s,%s\n" % (user, parsed.geturl(), SITE_CSS[parsed.netloc])
  # Update flairs
  if csv != "":
    reddit_api("/api/flaircsv.json",
                 {'r': SUBREDDIT, 'flair_csv': csv, 'uh': modhash})
  # Mark messages as read
  reddit_api("/api/read_message", {'id': ','.join(read), 'uh': modhash})

if __name__ == "__main__":
    main()
