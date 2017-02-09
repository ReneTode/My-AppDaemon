## my sound functions

A general app for sound with AppDaemon.
sometimes its wise to stay a little behind. I needed to stay with an older version from Home Assistant for a while.
In the newer versions there was TTS created. I liked TTS but couldnt use it.
So I created my own Appdaemon functions for that.
Several other soundfunctions are there to that arent supported with Home Assistant, like setting the volume from the RPI.

## installation

you need to install gtts, vlc and mpg321

pip3 install gtts
sudo apt-get update
sudo apt-get install mpg321
sudo apt-get install vlc

then save this app in your app dir with name: sound.py

in the appdaemon configfile you need to set ( i included an example you can copy to your cfg file):                                           
```                                                                                
[soundfunctions]                                                                       
module = sound                                                                         
class = sound                                                                          
soundfilesdir = /an/empty!!/temp/file/dir/
defaultlanguage = en # choose any of the languages mentioned below

---  optional parameters   ---

startdelay = 30 # default = 30
maindelay = 2 # default = 2
restartboolean = input_boolean.yourrestartboolean # set only if you want to be able to reset manually
#extracontrole = false or true # (default = false) checks if mainloop is still running correctly.
extracontrole_repeattime # (default = 900) the amount of seconds between controles                                             

use_radio = false or true # (default = false)
radioboolean = input_boolean.yourboolean # boolean to set radio on or off, only with use_radio = true
radiostreamaddres = http://any.radio.stream # only with use_radio = true

use_volume = false or true # (default = false) sets volume from the RPI
radiovolumeslider = input_slider.yourradiovolumeslider # slider to change radiovolume, only with use_volume = true
clockvolumeslider = input_slider.yourclockvolumeslider # slider to change clockvolume, only with use_volume = true
defaultvoicevolumeslider = input_slider.yourttsvolumeslider # slider to change speech volume, only with use_volume = true

use_clock = false or true # (default = false)
clockfiles = /home/pi/GrandFatherChime # the location and name(without the numbers and extention) from the clock files
clock_constrain_start_time = 00:00:05 # the time you want the clock to start playing
clock_constrain_end_time = 08:00:05 # the time you want the clock to stop playing

keepspeakeralive = false or true # (default = false) some speakers need sound to stay awake
keepspeakeralivetext = uh # any short text you like to be repeated, only with keepspeakersalive = true
keepspeakeralivetime = 600 # time between the repeated sound in seconds, only with keepspeakersalive = true 
keepspeakeralivevolume = 70 # volume that the sound is played with, only with keepspeakersalive = true

logging = false or true # (default = False)
logfile = /path/to/your/log.file # a dedicated sound logfile
```                                                                                       
--------------------------------------------------------------------------------                                                                                         

## then you can use it like this in any app                                               
                                                                                   
sound = self.get_app("soundfunctions")                                                 
sound.say("Any text you like","your_language","your_priority","volume")    

you can also use:
                                                                                       
sound = self.get_app("soundfunctions")                                                 
sound.playsound("any valid mp3 file","your_priority","volume")

to put music in your soundlist (or sounds)

for priority give "1","2","3","4" or "5"


## Supported TTS languages:

supported languages: * 'af' : 'Afrikaans'
                     * 'sq' : 'Albanian'
                     * 'ar' : 'Arabic'
                     * 'hy' : 'Armenian'
                     * 'bn' : 'Bengali'
                     * 'ca' : 'Catalan'
                     * 'zh' : 'Chinese'
                     * 'zh-cn' : 'Chinese (Mandarin/China)'
                     * 'zh-tw' : 'Chinese (Mandarin/Taiwan)'
                     * 'zh-yue' : 'Chinese (Cantonese)'
                     * 'hr' : 'Croatian'
                     * 'cs' : 'Czech'
                     * 'da' : 'Danish'
                     * 'nl' : 'Dutch'
                     * 'en' : 'English'
                     * 'en-au' : 'English (Australia)'
                     * 'en-uk' : 'English (United Kingdom)'
                     * 'en-us' : 'English (United States)'
                     * 'eo' : 'Esperanto'
                     * 'fi' : 'Finnish'
                     * 'fr' : 'French'
                     * 'de' : 'German'
                     * 'el' : 'Greek'
                     * 'hi' : 'Hindi'
                     * 'hu' : 'Hungarian'
                     * 'is' : 'Icelandic'
                     * 'id' : 'Indonesian'
                     * 'it' : 'Italian'
                     * 'ja' : 'Japanese'
                     * 'ko' : 'Korean'
                     * 'la' : 'Latin'
                     * 'lv' : 'Latvian'
                     * 'mk' : 'Macedonian'
                     * 'no' : 'Norwegian'
                     * 'pl' : 'Polish'
                     * 'pt' : 'Portuguese'
                     * 'pt-br' : 'Portuguese (Brazil)'
                     * 'ro' : 'Romanian'
                     * 'ru' : 'Russian'
                     * 'sr' : 'Serbian'
                     * 'sk' : 'Slovak'
                     * 'es' : 'Spanish'
                     * 'es-es' : 'Spanish (Spain)'
                     * 'es-us' : 'Spanish (United States)'
                     * 'sw' : 'Swahili'
                     * 'sv' : 'Swedish'
                     * 'ta' : 'Tamil'
                     * 'th' : 'Thai'
                     * 'tr' : 'Turkish'
                     * 'vi' : 'Vietnamese'
                     * 'cy' : 'Welsh'
                                                                                       


