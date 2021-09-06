## YAML and JSON lists in appdaemon

When you didnt read part 1, 2 and 3 then you might not know how apps are configured by YAML. then i suggest reading those parts.  
If You already read that, then you know you can get variables from the app-yaml into your code by using self.args  
And at that point it starts to get confusing for a lot of people.  
The same thing happens when people get some info from a website or a device and that sends json.  
This part will explain how YAML and JSON relate to python lists.  

## YAML list 

lets take the yaml from a simple app

```
test_app:
  module: test # refers to test.py
  class: your_class_name # thats where the app lives
  entities:
    - sensor.a
    - sensor.b
    - switch.a
    - light.a
```

So in the first tutorial parts we did learn that you can use self.args["entities"] to get the yaml from the app.  
What not everyone knows is that yaml is actually noting more then a collection from lists, dicts, strings, floats, integers and booleans.  
So what happens when we use:
```
my_variable = self.arg["entities"]
```
in our code?
After that moment my_variable is a list from entities.
In python we write such a list like:

```
my_variable = ["sensor.a", "sensor.b", "switch.a", "light.a"]
```

you can also look at that in another way:

```
my_variable[0] = "sensor.a"
my_variable[1] = "sensor.b"
my_variable[2] = "switch.a"
my_variable[3] = "light.a"
```

And as you see its indeed a list from things (in this case entities)  
Also in YAML you can write that different, so you might see the connection better:

```
test_app:
  module: test # refers to test.py
  class: your_class_name # thats where the app lives
  entities: ["sensor.a", "sensor.b", "switch.a", "light.a"]
```

That YAML is exactly the same as the YAML before, just written differently.  

So i guess now you want to know, how can we use that in our apps, right?  
Lets assume we still use that same YAML, and we write a simple test.py  

```
import appdaemon.plugins.hass.hassapi as hass
 
class your_class_name(hass.Hass):
 
    def initialize(self): 
        for entity in self.args["entities"]:
            self.listen_state(self.what_we_want_to_do, entity)
	
    def what_we_want_to_do (self, entity, attribute, old, new, kwargs):
        self.log("{} has a new state: {}".format(entity, new))
```

Because we already made some apps before in the tutorial im not explaining line by line.  
This app will cause that you would see the state changes from all 4 entities in the log.  

There is 1 other thing in here that this tutorial didnt use before: .format  
.format() is a python function it moves the values from the variables you give into the string before it.  
There are more ways to put things together in python, older ways and newer ways.  
Nowadays most people use f-strings, I however already needed to take a big step from the oldest most simple way to format.  
You could also write:
```
self.log(entity + " has a new state: " + str(new))
```

because thats just python, im not going deeper into that, I just explained this line a bit more.  
So know you know how a YAML list relates to a python list, and how we get from YAML to the python code in appdaemon.  

## JSON list

Sometimes our appdaemon communicates with other devices and then we get info from such a device in JSON.  
What is the difference, you might want to know, right?  
actually there is no real difference, only the name. In JSON they call a list an array.  
  
lets say you get this JSON file from a device:  

```
'["color", "brightness", "state"]'
```

That could be the options you could use for a light.  
How do we get that into appdaemon?  
Lets look at this simple app:  

```
import appdaemon.plugins.hass.hassapi as hass
import json
import some_library

class your_class_name(hass.Hass):
 
    def initialize(self): 
        imported_json = some_library.get_the_json_values()
	      my_list = json.loads(imported_json)
```

Wow, can an app get any shorter?? (actually yes ;) )  
What would that app do?  
We got 2 more import lines.  
I explained about libraries briefly in the first part, remember.  
Its helpfull in python, because we can use functions that other people already have written, but that are not default in python.  
The first import is the json library. We use that because we want to get the json into appdaemon, so that we can work with it in a python way.  
The second library i made up!! :P   
I could have created a complete app that would get some info from a device that you dont know. But that would be way more complex to explain.  
If you run into the case where you get data from a device, website or anything else into appdaemon, then that part would be different every time.  
But the data part is always the same. And thats what i was explaining right?  
So whats more there?  
First I invented a function in my made up library. That is the part that gets the data.  
Then i use:  

```
	      my_list = json.loads(imported_json)
```

and thats the important part. it translates the json data we got to dicts and lists in appdaemon.  
so after that we could use things like:  

```
        for option in my_list:
            self.log("my device has the option: {}".format(option))
```

or

```
        self.log(option[0])
        self.log(option[1])
```

as you see after the json.loads there is no difference anymore then after we did use self.args  

I cant think of anything more to tell about lists in appdaemon. Next part will be about dicts.  
Do you have more questions about it? Then just come and ask me on the appdaemon discord: https://discord.gg/pHsjADY
