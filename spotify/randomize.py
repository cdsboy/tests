#!/usr/bin/env python

import cmd
import readline
import sys
import traceback
import time
import threading
import os
import random

import spotify
from spotify.manager import SpotifySessionManager, SpotifyPlaylistManager, \
    SpotifyContainerManager
try:
    from spotify.alsahelper import AlsaController
except ImportError:
    from spotify.osshelper import OssController as AlsaController
from spotify import Link, SpotifyError, ToplistBrowser

class Jukebox(SpotifySessionManager):

    queued = False
    playlist = 2
    track = 0
    appkey_file = os.path.join(os.path.dirname(__file__), 'spotify_appkey.key')

    def __init__(self, list, *a, **kw):
        SpotifySessionManager.__init__(self, *a, **kw)
        self.audio = AlsaController()
        self.ctr = None
        self.playing = False
        self._queue = []
        self.to_random = list
        print "Logging in, please wait..."


    def logged_in(self, session, error):
        if error:
            print error
            return
        self.session = session
        try:
            self.ctr = session.playlist_container()
            self.starred = session.starred()
            self.randomize(self.to_random)
        except:
            traceback.print_exc()

    def logged_out(self, session):
        self.ui.cmdqueue.append("quit")

    def load_track(self, track):
        if self.playing:
            self.stop()
        self.session.load(track)
        print "Loading %s" % track.name()

    def load(self, playlist, track):
        if self.playing:
            self.stop()
        if 0 <= playlist < len(self.ctr):
            pl = self.ctr[playlist]
        elif playlist == len(self.ctr):
            pl = self.starred
        self.session.load(pl[track])
        print "Loading %s from %s" % (pl[track].name(), pl.name())

    def queue(self, playlist, track):
        if self.playing:
            self._queue.append((playlist, track))
        else:
            self.load(playlist, track)
            self.play()

    def play(self):
        self.session.play(1)
        print "Playing"
        self.playing = True

    def stop(self):
        self.session.play(0)
        print "Stopping"
        self.playing = False

    def music_delivery(self, *a, **kw):
        return self.audio.music_delivery(*a, **kw)

    def next(self):
        self.stop()
        if self._queue:
            t = self._queue.pop()
            self.load(*t)
            self.play()
        else:
            self.stop()

    def end_of_track(self, sess):
        print "track ends."
        self.next()

    def search(self, *args, **kwargs):
        self.session.search(*args, **kwargs)

    def browse(self, link, callback):
        if link.type() == link.LINK_ALBUM:
            browser = self.session.browse_album(link.as_album(), callback)
            while not browser.is_loaded():
                time.sleep(0.1)
            for track in browser:
                print track
        if link.type() == link.LINK_ARTIST:
            browser = self.session.browse_artist(link.as_artist(), callback)
            while not browser.is_loaded():
                time.sleep(0.1)
            for album in browser:
                print album.name()
        callback(browser)

    def toplist(self, tl_type, tl_region):
        print repr(tl_type)
        print repr(tl_region)
        def callback(tb, ud):
            for i in xrange(len(tb)):
                print '%3d: %s' % (i+1, tb[i].name())

        tb = ToplistBrowser(tl_type, tl_region, callback)

    def shell(self):
        import code
        shell = code.InteractiveConsole(globals())
        shell.interact()

    def randomize(self, name):
      playlist = None
      dup_playlist = None
    
      for play in self.ctr:
        print play.name()
        if name == play.name():
          playlist = play
        #elif name + " - Random" == play.name():
        #  print "dup_playlist"
        #  dup_playlist = play
      
      if not playlist:
        print "Playlist not found"
        return
    
      if not dup_playlist:
        self.ctr.add_new_playlist(name + " - Random")
        for play in self.ctr:
          if name + " - Random" == play.name():
            dup_playlist = play
      else:
        to_remove = []
        for i, track in enumerate(dup_playlist):
          to_remove.append(i)
        dup_playlist.remove_tracks(to_remove)
    
      copied = []
      while len(copied) < len(playlist):
        i = random.randint(0, len(playlist) - 1)
        if not i in copied:
          copied.append(i)
          dup_playlist.add_tracks(0, [playlist[i]])


if __name__ == '__main__':
    import optparse
    op = optparse.OptionParser(version="%prog 0.1")
    op.add_option("-u", "--username", help="spotify username")
    op.add_option("-p", "--password", help="spotify password")
    op.add_option("-l", "--list", help="spotify playlist name")
    (options, args) = op.parse_args()
    print random.randint(0, 10)
    session_m = Jukebox(options.list, options.username, options.password, True)
    session_m.connect()
