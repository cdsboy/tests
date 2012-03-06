#!/usr/bin/env ruby

BACKGROUND_DIR = "/home/cdsboy/Pictures/Backgrounds"
MINUTES_TO_WAIT = 15

def set_wallpaper
  # make sure file exists before reading it
  File.open(BACKGROUND_DIR + "/.curback", 'a')
  cur_background = IO.readlines(BACKGROUND_DIR + "/.curback")[0]
  cur_background = cur_background.split(/ /)
  
  Dir.chdir(BACKGROUND_DIR)
  files = Dir.glob('*')
  
  new_background_a = ""
  new_background_b = ""
  until new_background_a != cur_background[0] and
        new_background_a != cur_background[1] and 
        new_background_b != cur_background[0] and
        new_background_b != cur_background[1] and
        new_background_a != new_background_b and
        new_background_a != "" and new_background_b != ""
    new_background_a = files[rand(files.length)]
    new_background_b = files[rand(files.length)]
  end

  new_background_a.gsub!(/[\[\]*! &"]/) {|s| s = "\\" + s }
  new_background_b.gsub!(/[\[\]*! &"]/) {|s| s = "\\" + s }
  
  File.open(BACKGROUND_DIR + "/.curback", 'w') {|f| f.write([new_background_a, new_background_b].join(' ')) }
  system "feh --bg-fil %s/%s %s/%s" % [BACKGROUND_DIR, new_background_a,
                                       BACKGROUND_DIR, new_background_b]
end

while true
  set_wallpaper
  sleep 60*MINUTES_TO_WAIT
end
