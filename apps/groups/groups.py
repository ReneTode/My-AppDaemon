###########################################################################################
#                                                                                         #
#  Rene Tode ( hass@reot.org )                                                            #
#  2017/11/29 Germany                                                                     #
#                                                                                         #
#  wildcard groups                                                                        #
#                                                                                         #
#  arguments:                                                                             #
#  name: your_name                                                                        #
#  device_type: sensor # or any devicetype                                                #
#  entity_part: "any_part"                                                                #
#  entities: # list of entities                                                           #
#    - sensor.any_entity                                                                  #
#  hidden: False # or True                                                                #
#  view: True # or False                                                                  #
#  assumed_state: False # or True                                                         #
#  friendly_name: Your Friendly Name                                                      #
#  nested_view: True # or False                                                           #
#                                                                                         #
###########################################################################################

import appdaemon.appapi as appapi

class create_group(appapi.AppDaemon):

  def initialize(self):
    all_entities = self.get_state(self.args["device_type"])
    entitylist = []
    for entity in all_entities:
      if self.args["entity_part"] in entity:
        entitylist.append(entity.lower())
    if "entities" in self.args:
      for entity in self.args["entities"]:
        entitylist.append(entity.lower())
    hidden = self.args["hidden"]
    view = self.args["view"]
    assumed_state = self.args["assumed_state"]
    friendly_name = self.args["friendly_name"]
    name = "group." + self.args["name"]    
    if not self.args["nested_view"]:
      self.set_state(name,state="on",attributes={"view": view,"hidden": hidden,"assumed_state": assumed_state,"friendly_name": friendly_name,"entity_id": entitylist})
    else:
      self.set_state(name + "2",state="on",attributes={"view": "false","hidden": hidden,"assumed_state": assumed_state,"friendly_name": friendly_name,"entity_id": entitylist})
      self.set_state(name,state="on",attributes={"view": "true","hidden": hidden,"assumed_state": assumed_state,"friendly_name": friendly_name,"entity_id": [name + "2"]})
