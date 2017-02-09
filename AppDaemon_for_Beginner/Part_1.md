## AppDaemon for beginner
 
## Introduction
 
Any automation you can think off in HomeAssistant can be done with AppDaemon.
The first question that could probably be asked is: "Why use AppDaemon when it is all possible in HomeAssistant itself?"
 
For me the answer is: "I have some experience in python (not all that much, but some) and very little experience with yaml, jinja, json and all other things that are used to configure Home Assistant.
And although things like yaml, jinja, etc. are not very hard to get to know, I think they are not very easy to use to create slightly more complicated automations and scripts.
 
So if you know your way around in yaml, jinja, etc. there is no actual need to start using AppDaemon unless you run into some boundaries.
 
Now you know why I use AppDaemon, so let’s start with some basic understanding.
 
## Our first App
 
Let us first start with thinking about what an app actually is. In the "old days" we had only programs, and then came apps. Apps are nothing more and nothing less than a program.
You can have a program or app to write a document, to make a photo, to edit a picture, and so on. Our apps in AppDaemon are nothing else. It is just a few lines of code which lead to a chosen action.
When comparing apps to a part from HA, apps are the automations. But it is a bit more than that. Maybe you would like to record every temperature change from 1 single sensor and log that into a file, or maybe you would like to make calculations with all kinds of sensors and create another sensor with that calculation.
With apps the sky is the limit. Do you like to have your sensor values in a spreadsheet? It’s possible. Do you like to know the highest temperature yesterday outside your door or in your living room? It’s possible.
Do you like to record how much time your heating is on, so you can calculate how much energy you used? It’s possible also. Like I said anything you can think of can be achieved.
 
So let’s start now.
I guess you use Home Assistant or else there would be no need to read this. ;) And you are probably making automations in Home assistant too (if not you should start :wink: )
In HA (Home Assistant) your automation would look something like this:
 
```  
automation:
  - alias: " Turn on light when input boolean is switched on and someone is home"
  trigger:
    platform: state
    entity_id: input_boolean.some_choice
    state: 'on'
  condition:
    condition: state
    entity_id: device_tracker.some_mobile
    state: 'home'
action:
    service: light.turn_on
    entity_id: light.some_light
```

This is an easy automation which makes the device labeled "some_light" turn on when you switch on the input boolean named "some_choice", but only if the device "some_mobile" is home at the time.
 
I think you can’t get any more basic then that, do you?
So let’s try to translate that to AppDaemon.
 
```
import appdaemon.appapi as appapi
 
class your_class_name(appapi.AppDaemon):
 
  def initialize(self): 
    self.listen_state(self.what_we_want_to_do,"input_boolean.some_choice", new="on")
  def what_we_want_to_do (self, entity, attribute, old, new, kwargs):
    a_variabele_with_a_usable_name = self.get_state("device_tracker.some_mobile")
    if  a_variabele_with_a_usable_name == "home":
      self.turn_on("light.some_light")
 ```
 
That is the whole app. Don’t get frightened by all the things you don’t know and understand in this part. I will take all the time you need to explain every line separately if you read on.
And I know you think that programming is difficult, but it actually isn’t. It is like learning to speak in another language. If you go to another country and they don’t speak your language you still want to order that beer, so you learn how to do that.
The next parts are nothing more than learning to order a beer and maybe something to eat also. When we can feed ourselves maybe we can also learn how to ask direction, and before you know it you will be able to give someone directions in that other language.
And before you think: "learning languages is nothing for me, I am terrible at that", let me tell you that languages were always my weakest part in high school. Now I live in a different country and speak 3 languages. Not by learning from a book, but by using it.
And you are probably going to make a whole lot of mistakes. Don’t think that’s not normal. Everyone makes them all the time. The clue is to learn to recognize your mistakes and to learn how to avoid them.
But enough now with the psychology, back to our app.
 
## General part:
 
First we start with some parts that are in all apps:

```
import appdaemon.appapi as appapi
 
class your_class_name(appapi.AppDaemon):
 
  def initialize(self): 
 ```
 
At the start of any python script you start with importing some **libraries.:two:**
That is like when you want to start writing a document about a certain topic and you start by collecting some books which might help you write about your topic. You might want to use some parts from those books later on.
Of course you only collect those books which are helpful with your topic. If you collect some other books later on, while writing, you can put those by the others.
In python it is the same. We won’t use any other libraries in this app, but maybe later we use another one like datetime and then we would set "import datetime" beneath the other import.
 
In the second line we start a **class:two:**. And in this case I have given the class the name “your_class_name”. You can use any name there that you like. The most important thing about naming things is that it makes sense to you (and maybe later also for others).
After that part, we find between the brackets, **appapi.AppDaemon:one:**. In every class we use in AppDaemon we use that. It would be too much to explain classes in python, but you can search for "python classes" on Google if you would like to learn more about it.
 
In the third line we create a function. I hear you think: "what is a function?"
In short a function is a tiny action from your app. let’s say you want to add 2 figures over and over. Then you could write a function called addup which returns that value. You call it by writing "addup(5,7)".
In programming we use functions every time we want something to be used over and over. Sometimes our functions may be called from different places. All the libraries you import contain functions that you can use.
You might want to talk about how functions are also used to help organize your code and how apps may require functions with certain names so other programs know how to interface with them.  But keep it simple like you have been, it’s great so far.
It is like when you are writing that document and you put a link to a part from another book and that part gets displayed to the user, without you writing that part over and over.  The well known functions would be like a table of contents or an index.  They are parts of a book we expect to find.  Chapters are like functions that organize our book even though they are referenced multiple times.
In this app alone we are going to make 2 functions (and use a lot more). The First to start our app and the second which contains our action.
 
All functions start with a line like this: **def:two:** any_name(some, variables, you, want, to, pass, to, the, function):
This function (initialize) is a special one that we use in all apps.
Anything you create in this function will be done at the moment you start your app.
 
So that part is easy. You can copy/paste those three lines and put them in the beginning of all your apps and all you have to do is change the class name.
 
## The Trigger:
 
Now we come to the part where things start to get interesting.
``` 
self.listen_state(self.what_we_want_to_do,"input_boolean.some_choice", new="on")
```

Wait a moment before you start copying this! Before you do that I have to tell you that like in yaml it is also important to check out indentions. But it is not as difficult as in yaml. If something belongs to something else ( a function(def) belongs to a class, this statement belongs to the initialize function) then you have to indent. Everything else with the same indention is seen as grouped together. You can use any amount of white space that you like, but for every next statement the same amount)
 
So this comes beneath the initialize line with an indention.
Oh, you also want to know what it means? O well, because it’s you.
 
We start with the **self:two:** part. Well that's a little hard to explain but in basic it says that it belongs to the class. but just lets say, you need the self part if you want something created in AppDaemon. The **listen_state:one:** is a call to another function(def) which is somewhere in AppDaemon. And because you have connected this class to AppDaemon you can use "self" to call all functions created in AppDaemon.
 
Yeah you heard it right. Listen_state is a function. Like our initialize and many more we are going to use. So between the brackets we find some variables.
The first variable that listen_state likes to have is the name from the function we like to get executed when something happens.
In the API from AppDaemon this is called a **callback:one:**.
Besides setting what we want to be done, we need to set when we want it to be done.
You could listen to any kind of change in HA. A switch that is turned, a sensor which changes value, a device that comes home.
In our example we wanted to listen to input_boolean.some_choice.
You can listen to any change from the entity if you don’t put anything behind it. In that case the function "self.what_we_want_to_do" would be triggered if you set the input Boolean to on, as well as when you set it to off.
In this case we chose to give the setting that the function only gets called if the "new" state is on.
 
This was the whole part from the trigger in yaml. You can set lots off triggers in the same app pointing to the same function, or you can choose to make more apps or use more functions.
I like to divide my triggers as much as possible in more apps.
 
## The Action:
 
In the trigger we already did choose a name for our action. Remember that we used self.what_we_want_to_do?
 
So now we make a function with that name.
``` 
def what_we_want_to_do (self, entity, attribute, old, new, kwargs):
```

We already talked about def and the name after that. So what comes behind?
First there is that self again. It is there in all function (defs) we make, let’s say that is to let python know that we want to have something in AppDaemon. And your app is now part of AppDaemon.
Then we see entity, attribute, old and new. This are all parts from the "thing" that we are listening to. In our case entity is the Boolean we are listening to. Attribute is the attributes from the input Boolean (friendly name for instance). Old is the previous state from our Boolean and new is the new state.
Off course in our case we only pulled the trigger if new = "on" so we can predict all the values from this variables ourselves.
The part between the brackets is just copy paste for all listen_state we use. In one of the next parts I will show that there are one or two other ways according to different situations.
 
By the way don’t forget the “:” !! It states the beginning from a block off commands that will be indented the same way. So after the “:” everything that has more indention than this line will be considered part of the function.
 
Slowly we are getting there. We named our action, now let’s make some.
``` 
self.turn_on("light.some_light")
```

That’s all folks. The action is taken. So that means? Again self! Then a function. In this case we will use the **turn_on:two:** function. And all we need to do is tell that function what we want to turn on.
Our great friend Andrew has made a lot off those easy functions like **turn_off:one:**, **toggle:one:** and many more. I will use a few off them later on, but you can find them all in the API from AppDaemon.
 
I guess we are ready to run our app.
 
 
## The condition.
 
O boy, I forgot I had that part in my yaml to. Ok, you don’t need conditions, but I guess we want to use them anyway.
Let’s go back to our yaml and find out what condition we had.
We wanted our light only to go on if some_mobile was home. For that we need two things.
1) We need to know in what state our mobile is and
2) We need to check if that state is the state we like.
 
To know what state any entity is, is easy. Andrew has made another function for that: **get_state:one:**.
If you have paid attention you probably can write the next line yourself or at least a part from it.
```
a_variabele_with_a_usable_name = self.get_state("device_tracker.some_mobile")
```

Do I really need to tell you about the part behind the = ???
I guess not. It is just another function and we give it the variable which it needs.
What else do we have? Just the name of a variable we want to store the returned from the function, in. You can use any name there. Like in the function naming, make it useful. If you start reading about programming you will probably find a lot of examples from people and they use names like fo, foo, bar, etc. don’t use things like that. Later on if you read back your code you want to know what your variable is used for.
 
So that was part 1. Now part 2.
We are going to use a very common statement in any kind of programming. It can differ how it’s written, but it does the same: **"if ... then ...":two:**
In python it goes like this:
``` 
if  a_variabele_with_a_usable_name == "home":
``` 
That’s all. We don’t need "then" at all. The “:” takes care of that. We put the state from our device in the variable and now we compare that to what we want it to be. If the statement is true the lines indented below it get done.
 
So let’s put it all together again:
```
import appdaemon.appapi as appapi
 
class your_class_name(appapi.AppDaemon):
 
  def initialize(self): 
    self.listen_state(self.what_we_want_to_do,"input_boolean.some_choice", new="on")
 
  def what_we_want_to_do (self, entity, attribute, old, new, kwargs):
    a_variabele_with_a_usable_name = self.get_state("device_tracker.some_mobile")
    if  a_variabele_with_a_usable_name == "home":
      self.turn_on("light.some_light")
```
 
Our app is ready to go. there is only 1 thing we need to do.
We need to tell AppDaemon to use the app. For that we copy our app in the appdirectory we have set in the cfg file and we give it a name, lets say some_app.py
Then we make a part in the cfg file to tell AppDaemon to use the app like this:
```
[our_automation_name] any name you like.
module = some_app that was the name we used for our app
class = your_class_name and this was the name from our class
```
 
That's it. We made an app and we let AppDaemon use it. So go on! Make an input boolean in HA and let it put 1 of your lights on, but only if your mobile is home.
 
In the next part we will make things a little more complicated.
 You should also probably go through how to setup a debug environment and how to debug your code.  It wasn’t really obvious, especially to people who may be coming from an IDE of some type.
 
