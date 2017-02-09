###########################################################################################
#                                                                                         #
#  Rene Tode ( hass@reot.org )                                                            #
#  ( with a lot off help from andrew cockburn (aimc) )                                    #
#  2016/11/28 Germany                                                                     #
#  verlichtingsfile veranderd op: 11-01-17                                                #
###########################################################################################

import appdaemon.appapi as appapi
import datetime
import time

class switches(appapi.AppDaemon):

  def initialize(self):
    file_name = self.args["settingsfile"]
    sunriseon = False
    sunseton = False
    sunriseoff = False
    sunsetoff = False
    try:
      settings_file = open(file_name, "r")
      for line in settings_file:
        splitline = line.split(";")
        if not "#" in splitline[0]:
          switch = splitline[0]
          constraindays = splitline[3].rstrip('\n')
          sunseton = False
          sunriseon = False
          sunriseoff = False
          sunsetoff = False
          ontime = ""
          if splitline[1]!="":
            if "sunset" in splitline[1]:
              sunsetparts =splitline[1].split(":")
              offset1 = int(sunsetparts[1])
              sunseton = True
            elif "sunrise" in splitline[1]:
              sunsetparts =splitline[1].split(":")
              offset1 = int(sunsetparts[1])
              sunriseon = True
            else:
              ontime = self.parse_time(splitline[1])             
          else:
            ontime = ""
          if splitline[2]!="":
            if "sunset" in splitline[2]:
              sunsetparts =splitline[2].split(":")
              offset2 = int(sunsetparts[1])
              sunsetoff = True
            elif "sunrise" in splitline[2]:
              sunsetparts =splitline[2].split(":")
              offset2 = int(sunsetparts[1])
              sunriseoff = True
            else:
              offtime = self.parse_time(splitline[2])
          else:
            offtime = ""

          if sunriseon:
            self.log(switch + " tijd: sunrise " + str(offset1) + " dag: " + constraindays + " aan")
            self.run_at_sunrise(self.set_lights_on,offset=offset1,constrain_days=constraindays,switch=switch)
          if sunriseoff:
            self.log(switch + " tijd: sunrise " + str(offset2) + " dag: " + constraindays + " uit")
            self.run_at_sunrise(self.set_lights_off,offset=offset2,constrain_days=constraindays,switch=switch)
          if sunseton:
            self.log(switch + " tijd: sunset " + str(offset1) + " dag: " + constraindays + " aan")
            self.run_at_sunset(self.set_lights_on,offset=offset1,constrain_days=constraindays,switch=switch)
          if sunsetoff:
            self.log(switch + " tijd: sunset " + str(offset2) + " dag: " + constraindays + " uit")
            self.run_at_sunset(self.set_lights_off,offset=offset2,constrain_days=constraindays,switch=switch)            
          if type(ontime) is datetime.time:
            self.log(switch + " tijd: " + ontime.strftime("%H:%M:%S") + " dag: " + constraindays + " aan")
            self.run_daily(self.set_lights_on,ontime,constrain_days=constraindays,switch=switch)
          if type(offtime) is datetime.time:
            self.log(switch + " tijd: " + offtime.strftime("%H:%M:%S") + " dag: " + constraindays + " uit")
            self.run_daily(self.set_lights_off,offtime,constrain_days=constraindays,switch=switch)            
    except:
      self.log( "fout in lezen van verlichtingsfile")
        
  def set_lights_on(self, kwargs):
    #self.log(kwargs["switch"] + " aangedaan")
    self.light_action_log("automatisch aan",kwargs["switch"],"on")
    self.turn_on(kwargs["switch"])
      
  def set_lights_off(self, kwargs):
    #self.log(kwargs["switch"] + " uitgedaan")
    self.light_action_log("automatisch uit",kwargs["switch"],"off")
    self.turn_off(kwargs["switch"])

  def light_action_log(self,description, entity1, value1):
    runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
      log = open(self.args["logfile"], 'a')
      log.write(runtime + ";" + description + ";" + entity1 + ";" + value1 + "\n")
      log.close()
    except:
      self.log("VERLICHTINGSLOGFILE NIET BEREIKBAAR!!")

class alllightsout(appapi.AppDaemon):

  def initialize(self):
    self.listen_state(self.lights_out,self.args["lightswitch"], new = "on")

  def lights_out(self, entity, attribute, old, new, kwargs):
    self.log("alle verlichting uit","INFO")
    
    for counter in range(1,int(self.args["total_switches"])+1):
      if self.get_state(self.args["switch"+str(counter)])=='off':
        self.turn_on (self.args["switch"+str(counter)])
        time.sleep(2)
      self.turn_off(self.args["switch"+str(counter)])      
      time.sleep(2)
    self.turn_off(self.args["lightswitch"])
    self.light_action_log("alle verlichting","","off")

  def light_action_log(self,description, entity1, value1):
    runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
      log = open(self.args["logfile"], 'a')
      log.write(runtime + ";" + description + ";" + entity1 + ";" + value1 + "\n")
      log.close()
    except:
      self.log("VERLICHTINGSLOGFILE NIET BEREIKBAAR!!")

class lightcheck(appapi.AppDaemon):

  def initialize(self):
    self.listen_state(self.lights_change,self.args["lightsensor"])

  def lights_change(self, entity, attribute, old, new, kwargs):
    if float(new)<float(self.args["onvalue"]) and float(old)<float(self.args["onvalue"]) and self.get_state(self.args["controleswitch"])=="off":      
      self.log("donkere dag verlichting aan","INFO")
      for counter in range(1,int(self.args["total_switches"])+1):
        if self.get_state(self.args["switch"+str(counter)])=='off':
          self.turn_on (self.args["switch"+str(counter)])
          time.sleep(2)
      self.turn_on(self.args["controleswitch"])
      self.light_action_log("donkere dag verlichting","","on")
    elif float(new)>float(self.args["offvalue"]) and float(old)>float(self.args["offvalue"]) and self.get_state(self.args["controleswitch"])=="on":      
      self.log("donkere dag verlichting uit","INFO")
      for counter in range(1,int(self.args["total_switches"])+1):
        if self.get_state(self.args["switch"+str(counter)])=='on':
          self.turn_off (self.args["switch"+str(counter)])
          time.sleep(2)
      self.turn_off(self.args["controleswitch"])
      self.light_action_log("donkere dag verlichting","","off")

  def light_action_log(self,description, entity1, value1):
    runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
      log = open(self.args["logfile"], 'a')
      log.write(runtime + ";" + description + ";" + entity1 + ";" + value1 + "\n")
      log.close()
    except:
      self.log("VERLICHTINGSLOGFILE NIET BEREIKBAAR!!")

