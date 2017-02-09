###########################################################################################
#                                                                                         
#  Rene Tode ( hass@reot.org )                                                            
#                                                                                         
#  version 2.0
#  2017/02/09 Germany                                                                     
#
###########################################################################################                                                                                         
#  you need to install gtts, vlc and mpg321
#  that can be done by:
#  
#  pip3 install gtts
#  sudo apt-get update
#  sudo apt-get install mpg321
#  sudo apt-get install vlc
#
#  save this app in your app dir with name: sound.py
#
###########################################################################################                                                                                         
#  in the appdaemon configfile you need to set:                                           
#                                                                                         
#  [soundfunctions]                                                                       
#  module = sound                                                                         
#  class = sound                                                                          
#  soundfilesdir = /an/empty!!/temp/file/dir/
#  defaultlanguage = en # choose any of the languages mentioned below
#
#  optional parameters
#  ----------------------------------
#
#  startdelay (default = 30)
#  maindelay (default = 2)
#
#  restartboolean = input_boolean.yourrestartboolean # set only if you want to be able to reset manually
#
#  extracontrole = false or true # (default = false) checks if mainloop is still running correctly.
#  extracontrole_repeattime # (default = 900) the amount of seconds between controles                                             
#
#  use_radio = false or true # (default = false)
#  radioboolean = input_boolean.yourboolean # boolean to set radio on or off, only with use_radio = true
#  radiostreamaddres = http://any.radio.stream # only with use_radio = true
#
#  use_volume = false or true # (default = false) sets volume from the RPI
#  radiovolumeslider = input_slider.yourradiovolumeslider # slider to change radiovolume, only with use_volume = true
#  clockvolumeslider = input_slider.yourclockvolumeslider # slider to change clockvolume, only with use_volume = true
#  defaultvoicevolumeslider = input_slider.yourttsvolumeslider # slider to change speech volume, only with use_volume = true
#
#  use_clock = false or true # (default = false)
#  clockfiles = /home/pi/GrandFatherChime # the location and name(without the numbers and extention) from the clock files
#  clock_constrain_start_time = 00:00:05 # the time you want the clock to start playing
#  clock_constrain_end_time = 08:00:05 # the time you want the clock to stop playing
#
#  keepspeakeralive = false or true # (default = false) some speakers need sound to stay awake
#  keepspeakeralivetext = uh # any short text you like to be repeated, only with keepspeakersalive = true
#  keepspeakeralivetime = 600 # time between the repeated sound in seconds, only with keepspeakersalive = true 
#  keepspeakeralivevolume = 70 # volume that the sound is played with, only with keepspeakersalive = true
#
#  logging = false or true # (default = False)
#  logfile = /path/to/your/log.file # a dedicated sound logfile
#                                                                                         
###########################################################################################                                                                                         
#  then you can use it like this in any app                                               
#                                                                                         
#  sound = self.get_app("soundfunctions")                                                 
#  sound.say("Any text you like","your_language","your_priority","volume")    
#                     
#  supported languages: * 'af' : 'Afrikaans'
#                       * 'sq' : 'Albanian'
#                       * 'ar' : 'Arabic'
#                       * 'hy' : 'Armenian'
#                       * 'bn' : 'Bengali'
#                       * 'ca' : 'Catalan'
#                       * 'zh' : 'Chinese'
#                       * 'zh-cn' : 'Chinese (Mandarin/China)'
#                       * 'zh-tw' : 'Chinese (Mandarin/Taiwan)'
#                       * 'zh-yue' : 'Chinese (Cantonese)'
#                       * 'hr' : 'Croatian'
#                       * 'cs' : 'Czech'
#                       * 'da' : 'Danish'
#                       * 'nl' : 'Dutch'
#                       * 'en' : 'English'
#                       * 'en-au' : 'English (Australia)'
#                       * 'en-uk' : 'English (United Kingdom)'
#                       * 'en-us' : 'English (United States)'
#                       * 'eo' : 'Esperanto'
#                       * 'fi' : 'Finnish'
#                       * 'fr' : 'French'
#                       * 'de' : 'German'
#                       * 'el' : 'Greek'
#                       * 'hi' : 'Hindi'
#                       * 'hu' : 'Hungarian'
#                       * 'is' : 'Icelandic'
#                       * 'id' : 'Indonesian'
#                       * 'it' : 'Italian'
#                       * 'ja' : 'Japanese'
#                       * 'ko' : 'Korean'
#                       * 'la' : 'Latin'
#                       * 'lv' : 'Latvian'
#                       * 'mk' : 'Macedonian'
#                       * 'no' : 'Norwegian'
#                       * 'pl' : 'Polish'
#                       * 'pt' : 'Portuguese'
#                       * 'pt-br' : 'Portuguese (Brazil)'
#                       * 'ro' : 'Romanian'
#                       * 'ru' : 'Russian'
#                       * 'sr' : 'Serbian'
#                       * 'sk' : 'Slovak'
#                       * 'es' : 'Spanish'
#                       * 'es-es' : 'Spanish (Spain)'
#                       * 'es-us' : 'Spanish (United States)'
#                       * 'sw' : 'Swahili'
#                       * 'sv' : 'Swedish'
#                       * 'ta' : 'Tamil'
#                       * 'th' : 'Thai'
#                       * 'tr' : 'Turkish'
#                       * 'vi' : 'Vietnamese'
#                       * 'cy' : 'Welsh'
#                                                                                       
#  for priority give "1","2","3","4" or "5"
#
###########################################################################################                                                                                         
#  you can also use:
#                                                                                        
#  sound = self.get_app("soundfunctions")                                                 
#  sound.playsound("any valid mp3 file","your_priority","volume")
#
#  to put music in your soundlist (or sounds)
#
###########################################################################################


import appdaemon.appapi as appapi
import datetime
import tempfile
import subprocess
import os
import time as timelib
from gtts import gTTS
import threading

class sound(appapi.AppDaemon):

  def initialize(self):
############################################
# setting variabele startvalues
############################################
    self.soundlog("============================================================")
    self.soundlog("initialize; started soundfunctions")
    self.lasttime = datetime.datetime.now()
    self.totaltime = datetime.timedelta(seconds=1)
    self.loopamount = 1
    self.minutesrunning = 0
    self.restarts = 0
    self.lastsound = datetime.datetime.now()
    runtime = datetime.datetime.now() + datetime.timedelta(minutes=15)
    startdelay = 30
    self.maindelay = 2

############################################
# check the config for optional settings
############################################
    if "startdelay" in self.args:
      startdelay = int(self.args["startdelay"])
    if "maindelay" in self.args:
      self.maindelay = int(self.args["maindelay"])  

    if "restartboolean" in self.args:
      self.soundlog("initialize; listening to restart boolean")
      self.listen_state(self.extrastart,self.args["restartboolean"])
    if self.args["extracontrole"] == "True" or self.args["extracontrole"] == "true": 
      if "extracontrole_repeattime" in self.args:
        repeattime = int(self.args["extracontrole_repeattime"])
      else:
        repeattime = 900
      self.soundlog("initialize; extra controle started")
      self.run_every(self.autorestart,runtime,repeattime)
    
    if self.args["use_volume"] == "True" or self.args["use_volume"] == "true":
      self.soundlog("initialize; use volume")
      self.usevolume = True
    else:
      self.usevolume = False

    if self.args["use_radio"] == "True" or self.args["use_radio"] == "true":
      if self.usevolume:
        self.listen_state(self.setradiovolume,self.args["radiovolumeslider"])
      self.soundlog("initialize; use radio")
      self.useradio = True
      self.listen_state(self.radio,self.args["radioboolean"])
    else:
      self.useradio = False

    if self.args["use_clock"] == "True" or self.args["use_clock"] == "true":
      clocktime = datetime.time(12, 0, 2)
      self.run_hourly(self.clock, clocktime,constrain_start_time=self.args["clock_constrain_start_time"],constrain_end_time=self.args["clock_constrain_end_time"])
   
############################################
# start the mainloop with a delay
############################################
    self.soundlog("initialize; mainloop started")
    self.sound_handle = self.run_in(self.main_loop,startdelay,normal_loop="running")
    

  def autorestart(self, kwargs):   
############################################
# restart function starts only if set in
# options. it controls periodicly if the
# mainloop still runs correct.
############################################
    self.soundlog("autorestart; start restart controle")
    counter = 0
    counter2 = 1
    handletest = "empty"
    while handletest == "empty" and counter < 30:
      self.soundlog("autorestart; restartloop: " + str(counter))
      try:
        time, interval, kwargs = self.info_timer(self.sound_handle)
        handletest = kwargs["normal_loop"]
        counter = 60
      except:
        handletest="empty"
        counter = counter + 1
        counter2 = counter
        timelib.sleep(1)
    if handletest != "running":
############################################
# reset main loop settings
############################################
      self.cancel_timer(self.sound_handle)
      self.lasttime = datetime.datetime.now()
      self.totaltime = datetime.timedelta(seconds=1)
      self.minutesrunning = 0
      self.restarts = self.restarts + 1
############################################
# restart main loop
############################################
      self.sound_handle = self.run_in(self.main_loop,self.maindelay,normal_loop="restarted")
      self.soundlog("autorestart; restart done") 
    else:
      self.soundlog("autorestart; restart not needed")

  def extrastart(self, entity, attribute, old, new, kwargs):
############################################
# restart function starts only if set in
# options. it restarts the mainloop if the  
# boolean set to on.
############################################
    self.cancel_timer(self.sound_handle)
    self.sound_handle2 = self.run_in(self.main_loop,self.maindelay,normal_loop="restarted")
    self.turn_off(self.args["restartboolean"])
    self.soundlog("manualrestart; restart done")


  def main_loop(self, kwargs):
############################################
# mainloop
# checks if there is a sound in the list
# if so it plays it
############################################
    radioonagain = False
    volumechanged = False
    priority = self.read_prioritylist()
    fname = priority["fname"]
    tempfile = priority["tempfile"]
    tempfname = priority["tempfilename"]
    volume = str(priority["volume"])
    if fname != "":
############################################
# a sound is found, lets try to play it
# check if radio is on and set it of if 
# needed. check if volume should be changed
############################################
      self.soundlog("mainloop; found: " + fname)  
      if self.useradio and self.get_state(self.args["radioboolean"])=="on":
        self.soundlog("mainloop; radio is on")
        radioonagain = True
        self.radiooff()
        self.soundlog("mainloop; did set radio off")
      if self.usevolume:
        self.setvolume(volume)
        volumechanged = True
        self.soundlog("mainloop; volume changed")
      self.play(fname)
      self.soundlog("mainloop; sound played")
      if tempfile == "1":
        os.remove(fname)
        self.soundlog("mainloop; temp mp3 file removed")
      os.remove(tempfname)
      self.soundlog("mainloop; tempfile removed")
      self.lastsound = datetime.datetime.now()

    if self.useradio and self.get_state(self.args["radioboolean"])=="on":
      self.lastsound = datetime.datetime.now()
    actualtime = datetime.datetime.now()
    timesincelastsound = actualtime - self.lastsound

    if self.args["keepspeakeralive"] == "True" or self.args["keepspeakeralive"] == "true":
      if timesincelastsound > datetime.timedelta(seconds=int(self.args["keepspeakeralivetime"])):
############################################
# keep speakers alive function delay time
# has gone by without sound played, so play
# the keepspeakersalivetext.
############################################
        self.say(self.args["keepspeakeralivetext"],self.args["defaultlanguage"],"5",self.args["keepspeakeralivevolume"])
        self.soundlog("mainloop; heartbeat to keep speaker alive")
    timedifference = actualtime - self.lasttime
    self.lasttime = actualtime
    if timedifference < datetime.timedelta(seconds=1):
       self.soundlog("mainloop; LOOP RUNNING MORE THEN ONCE")
       self.loopamount = 2
    else:
       self.totaltime = self.totaltime + timedifference
    minutesrunning = self.totaltime.seconds//60
    if minutesrunning > (self.minutesrunning + 5):
      self.minutesrunning = minutesrunning
      self.soundlog("mainloop; SOUNDFILE RUNS CORRECTLY SINCE: " + str(self.minutesrunning) + " MINUTES, RESTARTED: " + str(self.restarts) + " TIMES. LOOPAMOUNT: " + str(self.loopamount))
    if self.loopamount > 1:
############################################
# more then 1 loop is running. so dont
# start a new 1
############################################
      self.loopamount = 1
      self.soundlog("mainloop; A MAINLOOP IS CLOSED")
    else:
      self.sound_handle = self.run_in(self.main_loop,self.maindelay,normal_loop="running")
      #self.soundlog("mainloop; normal loop ended")
    if radioonagain:
      if self.usevolume:
        self.setvolume(self.get_state(self.args["radiovolumeslider"]))
      self.soundlog("mainloop; set radio on again")
      self.radioon()
      self.soundlog("mainloop; radio is on again")
    elif volumechanged:
      if self.usevolume:
        self.setvolume(self.get_state(self.args["defaultvoicevolumeslider"]))


  def say(self,text,lang,priority,volume="00"):
############################################
# the TTS function. make a mp3 from the text
# and put a file in the prioritylist
############################################
    self.soundlog("say; put text in waitingrow: " + text)
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        fname = f.name
    tts = gTTS(text=text, lang=lang)
    tts.save(fname)
    self. write_in_prioritylist(priority,fname,"1",volume)
  

  def playsound(self,file,priority,volume="00"):
############################################
# set in the prioritylist which sound to play
############################################
    self.soundlog("playsound; put sound in waitingrow: " + file)
    self. write_in_prioritylist(priority,file,"2",volume)


  def play(self,filename):
############################################
# play a mp3 with mpg321
############################################
    self.soundlog("play; play sound: " + filename)
    cmd = ['mpg321',filename]
    with tempfile.TemporaryFile() as f:
      subprocess.call(cmd, stdout=f, stderr=f)
      f.seek(0)
      output = f.read()
    self.lastsound = datetime.datetime.now()
    self.soundlog("play; sound played: " + filename)
    
  def setvolume(self, volume):
############################################
# change the volume from the RPI with amixer
############################################
    self.soundlog("setvolume; volume to: " + volume)
    if "." in volume:
      volumeparts = volume.split(".")
      volume = volumeparts[0]
    cmd = ['amixer','cset','numid=1',volume + '%']
    with tempfile.TemporaryFile() as f:
      subprocess.call(cmd, stdout=f, stderr=f)
      f.seek(0)
      output = f.read()

  def setradiovolume(self, entity, attribute, old, new, kwargs):
############################################
# radiovolume is changed with inputslider
############################################
    if self.get_state("input_boolean.swr3")=="on":
      self.setvolume(new)

  def write_in_prioritylist(self,priority,file,tempfile,volume="00"):
############################################
# set a file in the prioritylist
############################################
    self.soundlog("write_in_prioritylist; file in list: " + file)
    try:
      if volume == "00":
        volume = str(self.get_state("input_slider.ttsvolume"))      
      runtime = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S.%f")
      log = open(self.args["soundfilesdir"] + priority + "_" + tempfile + "_" + volume + "_" + file[-10:], 'w')
      log.write(runtime + ";" + file)
      log.close()
    except:
      self.log("SOUNDFILEDIR PROBLEM!!")


  def read_prioritylist(self):
############################################
# check if there are files in the list.
# if so give back the 1 with the highest
# priority that is the oldest
############################################
    toppriority = 0
    activefile = ""
    firsttime = datetime.datetime.strptime("31-12-2050","%d-%m-%Y")
    activetemp = ""
    activefnamefile = ""
    activevolume = 0
    filelist = os.listdir(self.args["soundfilesdir"])
    if filelist:
      for file in filelist:
        priority = int(file[0])
        tempfile = file[2]
        volume = int(file[4:6])
        tempfilename = self.args["soundfilesdir"] + file
        fnamefile = open(tempfilename, 'r')
        for line in fnamefile:
          splitline = line.split(";")
          fname = splitline[1]
          fdate = datetime.datetime.strptime(splitline[0],"%d-%m-%y %H:%M:%S.%f")
        fnamefile.close()
        if priority >= toppriority:
          if firsttime > fdate:
            firsttime = fdate
            toppriority = priority
            activefile = fname
            activetemp = tempfile
            activefnamefile = tempfilename
            activevolume = volume
    return {"fname":activefile,"tempfilename":activefnamefile,"tempfile":activetemp,"volume":activevolume}    

  def radio(self, entity, attribute, old, new, kwargs):
############################################
# radio inputboolean is set on or off
############################################
    if new=="on":
      self.radioon()
    elif new=="off":
      self.radiooff()

  def radioon(self):
############################################
# set the radion to on in a seperate thread
############################################
    self.soundlog("radioon; change radio volume")
    self.setvolume(self.get_state("input_slider.radiovolume"))
    self.soundlog("radioon; radio on")
    t = threading.Thread(target=self.radiothread)
    t.start()
    self.soundlog("radioon; radio is on")

  def radiothread(self):
############################################
# play radio with cvlc
############################################
    cmd = ['cvlc',self.args["radiostreamaddres"]]
    with tempfile.TemporaryFile() as f:
      subprocess.call(cmd, stdout=f, stderr=f)
      f.seek(0)
      output = f.read()

  def radiooff(self):
############################################
# radio off, kill all vlc threads
############################################
    self.soundlog("radiooff; radio off")
    cmd = ['killall','vlc']
    with tempfile.TemporaryFile() as f:
      subprocess.call(cmd, stdout=f, stderr=f)
      f.seek(0)
      output = f.read()
    self.soundlog("radiooff; radio is off")

  def clock(self, kwargs):
############################################
# sound the clock hourly
############################################
    runhour = datetime.datetime.now().hour
    if runhour > 12:
      runhour = runhour - 12
    volume = str(self.get_state(self.args["clockvolumeslider"]))
    self.soundlog("clock; hourly sound")
    self.playsound(self.args["clockfiles"] + str(runhour) + ".mp3","5",volume)

  def soundlog(self,logtext):
############################################
# put an entry in the soundlog
############################################
    if self.args["logging"] == "true" or self.args["logging"] == "True": 
      runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
      try:
        log = open(self.args["logfile"], 'a')
        log.write(runtime + ";" + logtext + "\n")
        log.close()
      except:
        self.log("SOUNDLOGFILE CANT BE WRITTEN!!")

    