## AppDaemon for beginner part 2
## Sunrise and sunset

I guess I got you interested in this programming thing. That's great. So let's make another App.   

Google is my biggest friend when I am programming. I am not a professional programmer (anymore) and in the last few years I had to learn a lot off new things.  I don't know about you, but I get older every year.  
So sometimes I need some help, because I forget something or I haven't learned it yet. The API from AppDaemon is always opened so I can look up how to do it correctly, and many other things using google.

But don't start googling yet, you might find a better tutorial then this one :wink:

Ok, let's get back to our topic before we wander off to far.  
In HA one off the first things you find are the automations for sunset and sunrise. They are nice and fun. You can make you outside lights shine during the night or dim your inside lights during the evening.  
I can tell you that I haven't turned on a light in my living room since I started using HA.  
Andrew has given us some nice and easy functions for using the sunset and sunrise in AppDaemon.  
The first 2 are **self.sunset() :one:** and **self.sunrise() :one:**  
They are really what they seem to be. Just the time that the sun will set or rise. At least when you did everything right in HA :blink:
We can use that anywhere in our pythonscripts to compare to your local time for instance.  

But wait there is even more!  
Andrew also created **self.runatsunset(The_function_you want_to_start, offset, kwargs) :one:** and **self.run_at_sunrise(The_function_you want_tostart, offset, kwargs) :one:**  
I think you understand that this could be used as trigger, so in our initialize function.  
Don't be scared from the word **kwargs (2)**. It is not klingon language or so (yeah I am a startrek fan) Kwargs is a python word that is used on a place where you can use several variables you want to pass to the function.  
So at that place you can give something to your function. Maybe you like to give a description or a color for your lights. I don't use it a lot actually, but it is there.  
Do you think that's all? Not in AppDaemon. We also have: **self.sunup() :one:** and **self.sun_down() :one:** So we can check if the sun is up or down without calculating or thinking.  

## Args

Oke, that's about it for sunrise and sunset. We will use it in a few minutes, but first I want to tell you about another very important thing in AppDaemon.  
Args! No again its not klingon language ;) Args is short for arguments. Good arguments are a base for a conversation (Bad arguments actually also) but in this case it is nothing more the something we pass on.  
Just to give you an example: x + 1 = ?  
I guess you cant give the answer right now. but you can if I tell you that x is 4, and also when I say that x = 67.  
That's what we do with args.  
In our python script we use **self.args["your_arg_name"] :one:** and then we can put those args in our cfg file.  
Note that this is not a function. A function would have the variables between () and here you use []. Actually that's not really important, but now you know why we don't use ()
In our cfg file we could then put your_arg_name = Mr. Bean and in another part we could place your_argname = Queen Elisabeth.
Off course we don't want to automate those people, but I learned that it sometimes helps to think of something weird to remember easy things.
In our case we could use it to write a small script (like our first app) and use it over and over.

Remember this line?

```
      self.turnon("light.somelight")
```

we could rewrite that to:

```
      self.turnon(self.args["lightID"])
```

And then we would add

```
lightID = light.some_light
```

to our cfg file.
And after that we could also use some_other_light without changing our app.
In our cfg file we just make it like this:

```
[some_light_on]  
module = some_app  
class = your_class_name  
lightID = light.some_light  

[some_other_light_on]  
module = some_app  
class = your_class_name  
lightID = light.some_other_light  
```

And later on you could add another light, and another...
Nice isn't it? I think we have learned enough now to make a second app, don't you think so?

So let's do that.

## Our second app

Ok now let's make a light go on based on sunset and let it go out based on sunrise. But lets us do it so that we can use any light we have in HA, and we want to be able to switch every light on and off with another offset.
Here is the full app (we could make 2 apps out of this 1 for sunset and 1 for sunrise, but let's keep this together):

```
import appdaemon.appapi as appapi

class sun_down_lights(appapi.AppDaemon):

  def initialize(self):
    self.runatsunset(self.light_on_function, ,offset = int(self.args["sunset_offset"])
    self.runatsunrise(self.light_off_function, ,offset = int(self.args["sunrise_offset"])

  def light_onfunction (self, kwargs):
      self.turnon(self.args["lightID"])

  def light_offfunction (self, kwargs):
      self.turnoff(self.args["lightID"])
```

That's all it is. So let's break it down again:

The first 3 lines are already in our first app, so just copy/paste.
Then we get:

```
    self.runatsunset(self.light_on_function, ,offset = int(self.args["sunset_offset"])
    self.runatsunrise(self.light_off_function, ,offset = int(self.args["sunrise_offset"])
```

Actually there is only 1 thing that I haven't talked about already and that is the part **int() :two:**  
As you see it has brackets. So it is a function that is standard python. All that it does is convert a **string (text) :two:** to an **integer (number) :two:**.  
All arguments you get with self.args are variables of the type string. And for the functions run_at_sunset and run_at_sunrise we need a variable from the type integer. So we convert the string to an integer.  
Obviously that only works if the variable actually contains numbers and not just characters.  
I used **'offset=' :one:** in our lines. The keyword offset is important because we can also give on other variables to our function. For instance **random=... :one:**
The arguments sunset_offset and sunrise_offset we can later set in our cfg file.

The next line:

```
  def light_onfunction (self, kwargs):
```
Is where we name our function. Do you remember that I told you that there are a few ways we use the part between the brackets?
(self, kwargs) is what we use for all time based functions (callbacks).

Then we get:

```
      self.turnon(self.args["lightID"])
```

Not much to say about that anymore. We talked about that when I explained about args.
And off course I can also tell nothing more than you know already about the last 2 lines.

That was easy, wasn't it?

Only 1 thing more to do. Edit our cfg file again.  
So lets make to lights go on when the sun is down.  
The first 1 hour before sunset until 1 hour after sunrise and the second from sunset to sunrise.

O boy, I forgot something. We haven't saved our app yet. and therefor it hasn't got a name. Lets save it before we lose it and give it the name sun_lights.py

So now edit our cfg file and add these lines:

```
[sun_down_some_light_on]
module = sun_lights
class = sun_down_lights
sunset_offset = -3600
sunrise_offset = 3600
lightID = light.some_light

[sun_down_some_other_light_on]
module = sun_lights
class = sun_down_lights
sunset_offset = 0
sunrise_offset = 0
lightID = light.some_other_light
```

Just one small remark: offset is given in seconds.

So now you know how to let your lights go on in the evening and let them go out in the morning again.  
I hope you don't turn on to many light, because then you could have problems sleeping. :smile:

Have fun trying it out.

**:one: these words are AppDaemon specific. you can find them in the API**   
**:two: these words you can lookup by googling for "python this_word"**
