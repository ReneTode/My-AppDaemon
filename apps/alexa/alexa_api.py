import appdaemon.plugins.hass.hassapi as hass
import random
import datetime
import urllib
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class alexa_api(hass.Hass):

    def initialize(self):
        self.register_endpoint(self.api_call)        
        self.tempCardContent = ""

    def api_call(self, data):
        self.my_alexa_interpret_data(data)
        response = ""
        dialogDelegate = False
        endsession = False
        speech = None
        card = None
        logtext = ""     
        if self.dialog == None:
            if self.requesttype == "LaunchRequest":
                speech = self.random_arg(self.args["launchRequest"])
                endSession = False 
                dialogDelegate = False 
                card = None
                self.alexalog("Launch request (activate command)",100,"*")
            elif self.requesttype == "IntentRequest":
                speech = None
                endSession = False 
                dialogDelegate = True
                card = None
                self.alexalog("start dialog",100,"*")
            elif self.requesttype == "SessionEndedRequest":
                speech = None
                endSession = False 
                dialogDelegate = False
                card = None
                self.alexalog("The session has ended",100,"*")
            else:
                self.alexalog("Strange state",100,"*")
        elif self.dialog == "STARTED":
            ############################################
            # conversation started, just response dialogDelegate
            ############################################
            speech = None
            endSession = False 
            dialogDelegate = True
            card = None
            self.alexalog("dialog has been started",100,"*")
        elif self.dialog == "IN_PROGRESS":
            speech = None
            endSession = False 
            dialogDelegate = True
            card = None
            self.alexalog("dialog is in progress",100,"*")
        elif self.dialog == "COMPLETED":
            try:
                intentResponse = eval("self." + self.intentname)()
            except:
                intentResponse = "<p>So wie es ausseht is der moeglichkeit " + self.intentname + " noch nicht in lindon einprogrammiert.</p>"
            if intentResponse == "normalEnd":
                ############################################
                # intent ended without response, just ask for next action
                ############################################
                speech = self.random_arg(self.args["intentEnd"])
                endSession = False 
                dialogDelegate = False
                card = None
                self.tempCardContent = self.tempCardContent + self.intentname + "\n"
                self.alexalog("dialog has been completed, Normal End response send",100,"*")
            elif intentResponse == "error":
                ############################################
                # an error occured, stop conversation
                ############################################
                speech = self.random_arg(self.args["responseError"])
                endSession = True 
                dialogDelegate = False
                card = True
                cardContent = self.tempCardContent
                self.tempCardContent = ""
                self.alexalog("dialog has been completed, Error response send",100,"*")
            elif intentResponse == "stop":
                ############################################
                # user used stop intent, stop conversation
                ############################################
                speech = self.random_arg(self.args["conversationEnd"])
                endSession = True 
                dialogDelegate = False
                card = True
                cardContent = self.tempCardContent
                self.tempCardContent = ""
                self.alexalog("dialog has been completed, Dialog stopped by user",100,"*")
            elif intentResponse == "next":
                ############################################
                # user just responded yes, so just a question
                ############################################
                speech = self.random_arg(self.args["nextConversationQuestion"])
                endSession = False 
                dialogDelegate = False
                card = None
                self.tempCardContent = self.tempCardContent + self.intentname + "\n"
                self.alexalog("dialog has been completed, User just responded yes",100,"*")
            else:
                ############################################
                # Send the response from the Intent + question for next action
                ############################################
                speech = intentResponse + " " + self.random_arg(self.args["intentEnd"])
                endSession = False
                dialogDelegate = False
                card = None
                self.tempCardContent = self.tempCardContent + self.intentname + "\n"
                self.alexalog("dialog has been completed, Response " + speech,100,"*")
        if speech != None:
            speech = self.cleanup_text(speech)
        if card:
            response = self.my_alexa_response(EndSession = endSession, DialogDelegate = dialogDelegate, speech = speech, card = True, title = "Lindon", content = cardContent)
            self.alexalog(" ",100,"X")
            self.alexalog(" ",100,"X")
            self.alexalog(" ",100,"X")
        else:
            response = self.my_alexa_response(EndSession = endSession, DialogDelegate = dialogDelegate, speech = speech, card = None)
        if speech != None:
            if self.intentname == None:
                self.alexaresponselog("No Intent : " + speech)
            else:
                self.alexaresponselog(self.intentname + " : " + speech)
        return response, 200

    def my_alexa_interpret_data(self, data):
        ############################################
        # create vars from the data
        ############################################
        self.allslots = {}
        self.slots = {}
        self.dialog = self.my_alexa_dialog_state(data)
        self.requesttype = self.my_alexa_request_type(data)
        self.alexa_error = self.my_alexa_error(data)
        self.intentname = self.my_alexa_intent_name(data)
        if self.intentname != None:
            if "." in self.intentname:
                splitintent = self.intentname.split(".")
                self.intentname = splitintent[1]
        ############################################
        # get slots out of the data
        ############################################
        if "request" in data and "intent" in data["request"] and "slots" in data["request"]["intent"]:
            self.allslots = data["request"]["intent"]["slots"]
        slottext = "slots: "
        for slot,slotvalue in self.allslots.items():
            if "value" in slotvalue:
                self.slots[slot] = slotvalue["value"].lower()
            else:
                self.slots[slot] = ""
        if self.intentname == "searchYoutubeIntent":
            self.slots["search"] = self.slots["searchfielda"] + self.slots["searchfieldb"] + self.slots["searchfieldc"] + self.slots["searchfieldd"]
        ############################################
        # log that data came in
        ############################################
        self.alexalog("data came in.",100,"#")
        self.alexalog("dialogstate = " + str(self.dialog) + " and requesttype = " + str(self.requesttype))
        self.alexalog("intent = " + str(self.intentname))
        slottext = "slots: "
        for slot,slotvalue in self.slots.items():
            slottext = slottext + slot + "= " + str(slotvalue) + ", "
        self.alexalog(slottext)  
        self.alexalog("error = " + str(self.alexa_error))
        self.alexalog(" ",100,"#")

    def my_alexa_intent_name(self, data):
        ############################################
        # find the intent name in the data
        ############################################
        if "request" in data and "intent" in data["request"] and "name" in data["request"]["intent"]:
            return(data["request"]["intent"]["name"])
        else:
            return None

    def my_alexa_dialog_state(self,data):
        ############################################
        # find the dialog state in the data
        ############################################
        if "request" in data and "dialogState" in data["request"]:
            return(data["request"]["dialogState"])
        else:
            return None

    def my_alexa_intent(self, data):
        ############################################
        # find the requesttype in the data
        ############################################
        if "request" in data and "intent" in data["request"]:
            return(data["request"]["intent"])
        else:
            return None

    def my_alexa_request_type(self, data):
        ############################################
        # find the requesttype in the data
        ############################################
        if "request" in data and "type" in data["request"]:
            return(data["request"]["type"])
        else:
            return None

    def my_alexa_error(self, data):
        ############################################
        # get an error out of the data
        ############################################
        if "request" in data and "error" in data["request"] and "message" in data["request"]["error"]:
            return(data["request"]["error"]["message"])
        else:
            return None

    def my_alexa_slot_value(self, data, slot):
        ############################################
        # get a slot value from the data
        ############################################
        if "request" in data and \
                        "intent" in data["request"] and \
                        "slots" in data["request"]["intent"] and \
                        slot in data["request"]["intent"]["slots"] and \
                        "value" in data["request"]["intent"]["slots"][slot]:
            return(data["request"]["intent"]["slots"][slot]["value"])
        else:
            return ""

    def my_alexa_response(self, EndSession = False, DialogDelegate = False, speech = None, card = None, title = None, content = None):
        ############################################
        # put the speechfield from the response toghether
        ############################################
        response = {"shouldEndSession":EndSession}
        if DialogDelegate:
            response["directives"] = [{"type": "Dialog.Delegate", "updatedIntent": None}]
        if speech is not None:
           response["outputSpeech"] = {"type": "SSML","ssml": "<speak>" + speech + "</speak>"}
        if card is not None:
            response["card"] = {"type": "Simple", "title": title, "content": content}

        speech = \
            {
            "version": "1.0",
            "response": response,
            "sessionAttributes": {}
            }
        return speech

    def random_arg(self,argName):
        ############################################
        # pick a random text from a list
        ############################################
        if isinstance(argName,list):
            text = random.choice(argName)
        else:
            text = argname
        return text

    def floatToStr(self,myfloat):
        ############################################
        # replace . with , for better speech
        ############################################
        floatstr = str(myfloat)
        floatstr = floatstr.replace(".",",")
        return floatstr
        
    def cleanup_text(self, text):
        ############################################
        # replace some text like temperary slots with its value
        ############################################
        #self.log(text)
        for slotname, slotvalue in self.slots.items():
            text = text.replace("{{" + slotname + "}}",slotvalue)
        text = text.replace("_"," ")
        text = text.replace("...","<break time='2s'/>")
        return text

    def alexalog(self,logtext, repeat = 0, surrounding = ""):
        ############################################
        # put an entry in the alexa log
        ############################################
        if self.args["logging"] == "true" or self.args["logging"] == "True": 
            runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
            if repeat > 0:
                surrounding = surrounding * repeat
            try:
                log = open(self.args["logfile"], 'a')
                if logtext == " ":
                    log.write(runtime + ";  " + surrounding + "\n")
                else:
                    if surrounding != "":
                        log.write(runtime + ";  " + surrounding + "\n")
                    log.write(runtime + ";  " + logtext + "\n")
                    if surrounding != "":
                        log.write(runtime + ";  " + surrounding + "\n")
                log.close()
            except:
                self.log("ALEXA LOGFILE CANT BE WRITTEN!!")

    def alexaresponselog(self,logtext):
        ############################################
        # put an entry in the alexa responses log
        ############################################
        if self.args["logging"] == "true" or self.args["logging"] == "True": 
            runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
            try:
                log = open(self.args["responselogfile"], 'a')
                log.write(runtime + ";  " + logtext + "\n")
                log.close()
            except:
                self.log("ALEXA RESPONSELOGFILE CANT BE WRITTEN!!")

###################################################################################################################
# here come all intents
###################################################################################################################
    def helpIntent(self):
        ############################################
        # help is asked, give a list
        ############################################
        try:
            text = self.random_arg(self.args["helpIntent"]["Start"])
            for helpitem in self.args["helpIntent"]["List"]:
                text = text + helpitem
        except:
            text = self.args["helpIntent"]["Error"]
        return text

    def yesIntent(self):
        ############################################
        # the user just responded with yes, special question required
        ############################################
        text = "next"
        return text

    def commandoIntent(self):
        ############################################
        # a commando list is asked, give a list
        ############################################
        try:
            text = self.random_arg(self.args["commandoIntent"]["Start"])
            for helpitem in self.args["commandoIntent"]["list"]:
                text = text + helpitem
        except:
            text = self.args["commandoIntent"]["Error"]
        return text

    def storyIntent(self):
        ############################################
        # a new story is asked
        ############################################
        try:
            ############################################
            # find out which story number was last told
            ############################################
            storydir = self.args["storyIntent"]["storydir"]
            laststoryfile = open(storydir + "laststory.txt", 'r')
            laststoryfilelines = laststoryfile.readlines()
            lastreadstorynr = int(laststoryfilelines[0])
            newstorynr = lastreadstorynr + 1
            laststoryfile.close()

            ############################################
            # find out the name of the next story
            ############################################
            storylist = open(storydir + "storylist.txt", 'r')
            storylistlines = storylist.readlines()
            storylist.close()

            ############################################
            # get the story from the file and put it in text
            ############################################
            text = "<prosody volume='x-soft'>"
            story = open(storydir + storylistlines[newstorynr].strip(), 'r',encoding="ISO-8859-1")
            for line in story:
                text = text + "<p>" + line + "</p>"
            story.close()
            text = text + "</prosody>"

            ############################################
            # save the told story number for next time
            ############################################
            laststoryfile = open(storydir + "laststory.txt", 'w')
            laststoryfile.write(str(newstorynr))
            laststoryfile.close()
        except:    
            text = self.args["storyIntent"]["Error"]
        return text

    def repeatStoryIntent(self):
        ############################################
        # repeat the story is asked
        ############################################
        try:
            ############################################
            # find out which story number was last told
            ############################################
            storydir = self.args["storyIntent"]["storydir"]
            laststoryfile = open(storydir + "laststory.txt", 'r')
            laststoryfilelines = laststoryfile.readlines()
            lastreadstorynr = int(laststoryfilelines[0])
            newstorynr = lastreadstorynr
            laststoryfile.close()

            ############################################
            # find out the name of the next story
            ############################################
            storylist = open(storydir + "storylist.txt", 'r')
            storylistlines = storylist.readlines()
            storylist.close()

            ############################################
            # get the story from the file and put it in text
            ############################################
            text = "<prosody volume='x-soft'>"
            story = open(storydir + storylistlines[newstorynr].strip(), 'r',encoding="ISO-8859-1")
            for line in story:
                text = text + "<p>" + line + "</p>"
            story.close()
            text = text + "</prosody>"

            ############################################
            # save the told story number for next time
            ############################################
            laststoryfile = open(storydir + "laststory.txt", 'w')
            laststoryfile.write(str(newstorynr))
            laststoryfile.close()
        except:    
            text = self.args["storyIntent"]["Error"]
        return text
        
    def whatDoesSomeoneIntent(self):
        try:
            ############################################
            # get the state from a sensor and if its true
            # get the text for the person
            # when false check if person is part of household
            # and give text for household person or error text
            ############################################
            entityState = self.get_state(self.args["entityID"])
            if entityState == self.get_state(self.args["entityState"]):
                if self.slots["person"] in self.args["whatDoesSomeoneIntent"]["event_" + entityState]: 
                    text = self.random_arg(self.args["whatDoesSomeoneIntent"]["event_" + entityState][self.slots["person"]])
            else:
                if self.slots["person"] in self.args["household"]:
                    text = self.random_arg(self.args["whatDoesSomeoneIntent"]["event_" + entityState]["Household"])
                else:
                    text = self.random_arg(self.args["whatDoesSomeoneIntent"]["event_" + entityState]["notHousehold"])
        except:    
            text = self.args["whatDoesSomeoneIntent"]["Error"]
        return text

    def woIsSomeoneIntent(self):
        try:
            ############################################
            # an example Intent to show how you can change text
            # based on sensor states or time
            ############################################
            if self.slots["person"] in self.args["household"]:
                ############################################
                # decide if a person is guest or not
                ############################################
                if self.get_state("sensor." + self.slots["person"]) == "In bed":
                    ############################################
                    # assumes that there are sensors for every person 
                    # with a state if thet are in Bed
                    ############################################
                    text = self.random_arg(self.args["woIsSomeoneIntent"]["inBed"])
                elif self.get_state("sensor.kellertime") == "ja":
                    ############################################
                    # assumes that there is a sensor thats set to "ja"
                    # for a certain event
                    ############################################
                    text = self.random_arg(self.args["woIsSomeoneIntent"]["kellerTime"])
                elif self.now_is_between("18:00:00","18:30:00"):
                    ############################################
                    # at dinertime give another text
                    ############################################
                    text = self.random_arg(self.args["woIsSomeoneIntent"]["diner"])
                elif self.slots["person"] == "olinde":
                    if self.now_is_between("16:00:00","17:30:00"):
                        ############################################
                        # text for a certain person at a certain time
                        ############################################
                        text = self.random_arg(self.args["woIsSomeoneIntent"]["Olinde"]["couch"])
                    elif self.now_is_between("17:30:00","18:00:00"):
                        ############################################
                        # text for a certain person at a certain time
                        ############################################
                        text = self.random_arg(self.args["woIsSomeoneIntent"]["Olinde"]["cooking"])
                    else:
                        text = self.random_arg(self.args["woIsSomeoneIntent"]["Olinde"]["somethingElse"])
                elif self.slots["person"] == "rene":
                    if self.now_is_between("19:00:00","20:00:00"):
                        ############################################
                        # text for a certain person at a certain time
                        ############################################
                        text = self.random_arg(self.args["woIsSomeoneIntent"]["Rene"]["couch"])
                    else:
                        text = self.random_arg(self.args["woIsSomeoneIntent"]["Rene"]["somethingElse"])
                else:
                    text = self.random_arg(self.args["woIsSomeoneIntent"]["Other"]["somethingElse"])
            else:
                text = self.random_arg(self.args["woIsSomeoneIntent"]["Other"]["somethingElse"])
        except:    
            text = self.args["woIsSomeoneIntent"]["Error"]
        return text

    def sleepIntent(self):
        ############################################
        # if a switch is on give some text, if its off another
        ############################################
        return self.random_arg(self.args["sleepIntent"][self.get_state(self.args["sleepIntent"]["switch"])])

    def setBedOlindeIntent(self):
        ############################################
        # turn a switch on (you could change that for off or toggle)
        ############################################
        self.turn_on(self.args["setBedOlindeIntent"]["switch"])
        return self.random_arg(self.args["setBedOlindeIntent"]["switchedText"])

    def setBedOlindeOffIntent(self):
        ############################################
        # turn a switch off (you could change that for off or toggle)
        # sometimes its more user friendly to have 2 Intents for 1 task
        ############################################
        self.turn_off(self.args["setBedOlindeOffIntent"]["switch"])
        return self.random_arg(self.args["setBedOlindeOffIntent"]["switchedText"])

    def temperatureStateIntent(self):
        ############################################
        # give temperature for a list of temperature sensors
        ############################################
        try:
            if self.args["language"] == "DE":
                temp = self.floatToStr(self.get_state(self.args["temperatureSensors"][self.slots["location"]])) + self.args["TemperatureUnit"]
            else:
                temp = str(self.get_state(self.args["temperatureIntent"]["sensors"][self.slots["location"]])) + self.args["TemperatureUnit"]
            text = self.random_arg(self.args["temperatureStateIntent"]["textLine"]) + temp 
        except:
            text = self.random_arg(self.args["temperatureStateIntent"]["Error"])
        return text

    def StopIntent(self):
        ############################################
        # the user stopped the converation. return stop so you can say goodbye
        ############################################
        text = "stop"
        return text

    def searchYoutubeIntent(self):
        ############################################
        # this intent creates a dashboard with the top 6 from a youtube search
        # it also creates 6 fullscreen dashboards for each part,
        # you can view those dashboards with the showYoutubeIntent
        ############################################
        try:
            x = 0
            textToSearch = self.slots["search"]
            query = urllib.parse.quote(textToSearch)
            url = "https://www.youtube.com/results?search_query=" + query
            url_response = urllib.request.urlopen(url).readlines()
            for line in url_response:
                if "yt-uix-tile-link" in line.decode("utf-8") :
                    start = line.decode("utf-8").find("watch?v=")
                    if line.decode("utf-8")[start+7:start+8] == "=" and line.decode("utf-8")[start+19:start+20] == '"' and x<7:
                        try:
                            widgetfile =  open(self.args["dashboarddir"] + self.args["VideoWidgetsOverviewDash"][x] + ".yaml","w")
                            widgetfile.write("widget_type: iframe\n")
                            widgetfile.write("url_list:\n")
                            widgetfile.write("  - https://www.youtube.com/embed/")
                            widgetfile.write(line.decode("utf-8")[start+8:start+19])
                            widgetfile.close
                        except:
                            self.log("a small youtubewidget could not be created")
                        try:
                            widgetfile2 =  open(self.args["dashboarddir"] + self.args["VideoWidgetsSingleVideoDash"][x] + ".yaml","w")
                            widgetfile2.write("widget_type: iframe\n")
                            widgetfile2.write("url_list:\n")
                            widgetfile2.write("  - https://www.youtube.com/embed/")
                            widgetfile2.write (line.decode("utf-8")[start+8:start+19] + "?autoplay=1")
                            widgetfile2.close
                        except:
                            self.log("a fullscreen youtubewidget could not be created")
                        x = x + 1
                    elif x >= 7:
                        #self.log("stop search")
                        break
            self.dash_navigate("dash_youtube", 60)
            return "normalEnd"
        except:
            return "error"

    def showYoutubeIntent(self):
        ############################################
        # show 1 of the 6 videos from the last youtube search
        ############################################
        self.log(self.args["YoutubeVideoList"][(int(self.slots["videonr"])-1)])
        try:
            self.dash_navigate(self.args["YoutubeVideoList"][(int(self.slots["videonr"])-1)], self.args["VideoShowTime"])
            return "normalEnd"
        except:
            return "error"

    def viewCameraIntent(self):
        ############################################
        # shows 1 of your cameras listed in the yaml on the dashboard
        # expects a dashboard created for each camera
        # can also be used to show any dashboard you like on the devices where a dashboard is running
        ############################################
        try:
            if self.slots["location"] in self.args["CameraList"]:        
                self.dash_navigate(self.args["CameraList"][self.slots["location"]], self.args["CamShowTime"])
                return "normalEnd"
        except:
            return "error"

    def goodmorningIntent(self):
        ############################################
        # this intent sets a sensor when called, unless its already set
        # it also collects some sensor states for temperature and riverwaterlevels
        # and it looks at a last motion sensor, all that gets spoken as a report
        # because this intent is quite specific, its hard to get the text out to the yaml
        ############################################
        if self.slots["person"] == "rene" or self.slots["person"] == "":
            if self.get_state("sensor.rene") == "Thuis":
                ############################################
                # if the sensor says home this text is added
                ############################################
                starttext = "<p><say-as interpret-as='interjection'>ist nicht dein ernst</say-as>. <say-as interpret-as='interjection'>hipp hipp hurra</say-as>. <say-as interpret-as='interjection'>war nur ein scherz</say-as>. ich hatte es ihm schoen vorher gesagt.</p> <p>Aber hier bekommst du trotzdem dein information.</p>"
            else:
                ############################################
                # not home so coming out of bed set the state to home
                ############################################
                starttext = "<p>ok ich habe lindon gesagt das renee wach ist.<prosody rate='x-slow'> aber ich habe nichts zu Olinde gesagt.</prosody></p>"
                self.set_state("sensor.rene", state = "Thuis")
            ############################################
            # get the river waterlevel and add to text
            ############################################
            wasserstand = str(self.get_state("sensor.waterstand_trier"))
            waterstandtext = "<p>Der wasserstand in Trier, ist im moment " + wasserstand[0] + " meter und " + wasserstand[1:] + " centimeter.</p>"
            ############################################
            # get 2 outside temperatures and add to text
            ############################################
            tempbuiten = self.floatToStr(self.get_state("sensor.vijver_repeater_7_1"))
            tempvijver = self.floatToStr(self.get_state("sensor.vijver_repeater_7_0"))
            temptext = "<p>aussen ist es im moment " + tempbuiten + " grad<break time='1s'/> und der temperatur von der teich ist " + tempvijver + " grad.</p>"
            ############################################
            # get the last motion from a detector and add to text
            ############################################
            bewegingmar = str(self.get_state("sensor.frietkeuken_101_100_lu"))
            uur = bewegingmar[11:13]
            minuten = bewegingmar[14:16]
            martext = "<p>Der letzte bewegung, der bei Marjolein registriert ist war<break time='1s'/> " + uur + " uhr " + minuten + ".</p>"
            ############################################
            # combine the textparts
            ############################################           
            text = starttext + waterstandtext + temptext + martext
        else:
            ############################################
            # the person that woke up wasnt rene, no report or action just a goodmorning
            # here could be actions and text for other persons.
            ############################################
            text = "gutemorgen, " + self.slots["person"]
        return text
       
    def lightStateIntent(self):
        ############################################
        # an Intent to give back the state from a light.
        # but it also can be any other kind of entity
        ############################################           
        try:
            entityname = self.args["lightStateIntent"]["entities"][self.slots["device"]]
            state = self.get_state(entityname)
            if isinstance(state,float):
                if self.args["language"] == "DE":
                    state = self.floatToStr(state)
                else:
                    state = str(state)
            elif isinstance(state,str):
                state = state
            else:
                state = self.args["lightstateIntent"]["unreadableState"]
            text = self.random_arg(self.args["lightStateIntent"]["textLine"]) + state            
        except:
            text = self.random_arg(self.args["lightStateIntent"]["Error"])
        return text
