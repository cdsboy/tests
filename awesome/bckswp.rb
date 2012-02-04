#!/usr/bin/env ruby

BACKGROUND_DIR = "/home/cdsboy/Pictures/Backgrounds"
MINUTES_TO_WAIT = 15

def set_wallpaper
  # make sure file exists before reading it
  File.open(BACKGROUND_DIR + "/.curback", 'a')
  cur_background = IO.readlines(BACKGROUND_DIR + "/.curback")[0]
  
  Dir.chdir(BACKGROUND_DIR)
  files = Dir.glob('*')
  
  new_background = ""
  until new_background != cur_background and new_background != ""
    new_background = files[rand(files.length)]
  end

  new_background.gsub!(/[\[\]*! "]/) {|s| s = "\\" + s }
  
  File.open(BACKGROUND_DIR + "/.curback", 'w') {|f| f.write(new_background) }
  system "awsetbg %s/%s" % [BACKGROUND_DIR, new_background]
end

while true
  set_wallpaper
  sleep 60*MINUTES_TO_WAIT
end
