## AppDaemon for beginner
 

## Finding out what you did wrong.

So we have made 2 apps already. Did anything go wrong when you tried it out?  
If you are anything like me for sure. I would love to get a buck for every time I made an error typing or just any kind off error. :wink:

But I guess that's just a part off being human. When we make mistakes, we would like to know what we do wrong right?
For 2 reasons.

1) They always told me that we can learn from our mistakes and
2) When we don't correct our mistakes, our app won't do what we want it to do.

I know that there are always several ways to do things, but I like to tell you how I do it.  
First off all I make sure I always see the output from my Appdaemon.  
Untill a short while ago I had Appdaemon running on my PC and I always had an Commandprompt window open with Appdaemon running. 
Now it is running on my raspberry pi, but absolutely not as daemon. And thats because I want to see the output from Appdaemon directly.

So I have my settings in the appdaemon.yaml file like this:
```
  logfile: STDOUT
  errorfile: /home/pi/.homeassistant/error.log
```
 
That gets my log entries to the screen and my errors to the file. If nothing goes wrong, the errorlog stays empty.

Oke, lets take another look at our second app.

```
import appdaemon.appapi as appapi

class sun_down_lights(appapi.AppDaemon):

  def initialize(self):  
    self.run_at_sunset(self.light_on_function, ,offset = int(self.args["sunset_offset"])
    self.run_at_sunrise(self.light_off_function, ,offset = int(self.args["sunrise_offset"])

  def light_on_function (self, kwargs):
      self.turn_on(self.args["lightID"])

  def light_off_function (self, kwargs):
      self.turn_off(self.args["lightID"])
```
 

If we did nothing wrong on screen we would get something like:
```
2016-12-14 01:54:25.3456747 INFO Loading Module /ourappdir/lights.py
2016-12-14 01:54:25.3456921 INFO Loading Object Some_lights_on using class sun_down_lights from module lights
```
 
Oke it has loaded it. But did everything go right? Lets look at the errorlog. Is it still empty?  
Oke then i guess we didnt make any indentionerrors or typo's.  
This app is a simple one, but we will built more complex apps soon. With functions that calculate for example.  
How to know if our calculations are right?  

That's why we use **self.log():one:**  


more questions? Then just come and ask me on the appdaemon discord: https://discord.gg/pHsjADY
