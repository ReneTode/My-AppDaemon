###########################################################################################
#                                                                                         #
#  Rene Tode ( hass@reot.org )                                                            #
#                                                                                         #
#  2017/10/10 Germany                                                                     #
#                                                                                         #
#  an app to control a foscam camera.                                                     #
#  dependecies:                                                                           #
#    untangle (pip install untangle)                                                      #
#                                                                                         #
#  args:                                                                                  #
#  see the readme on                                                                      #
#  https://github.com/ReneTode/My-AppDaemon/tree/master/apps/foscam_app_v2                #
#                                                                                         #
###########################################################################################

import appdaemon.appapi as appapi
import datetime
import untangle
from urllib.request import urlopen
import urllib.request
from socket import timeout
import time

class foscam(appapi.AppDaemon):

  def initialize(self):
    runtime = datetime.datetime.now() + datetime.timedelta(seconds=5)
    self.loglevels = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0
    }
    self.logsettings = self.args["logsettings"]
    if "loglevel" in self.logsettings:
      self.loglevel = self.logsettings["loglevel"]
    else:
      self.loglevel = "INFO"
    if "logsensorlevel" in self.logsettings:
      self.logsensorlevel = self.logsettings["logsensorlevel"]
    else:
      self.logsensorlevel = "INFO"

    self.knowntype = 0
    self.knowntypes1 = ["F19828P","F19828P V2","R2","F19928P"]
    self.knowntypes2 = ["C1 lite","C1"]
    self.knowntypes3 = ["F18918","F18918W"]
    self.camsettings = self.args["camsettings"]
    self.picsettings = self.args["picsettings"]
    self.ptzsettings = self.args["ptzsettings"]
    self.alarmsettings = self.args["alarmsettings"]
    self.recordsettings = self.args["recordsettings"]
    self.dashboardsettings = self.args["dashboardsettings"]

    self.type = self.camsettings["camera_type"]
    if self.type in self.knowntypes1:
      self.PTZ = True
      self.infraredcam = True
    elif self.type in self.knowntypes2:
      self.PTZ = False
      self.infraredcam = False
    else:
      self.log("unknown camera type. try 1 of the known types, and if it works please report back on the forum")
      return

    try:
      self.camhost = self.camsettings["host"]
      self.portnr = str(self.camsettings["port"])
      self.user = self.camsettings["user"]
      self.password = self.camsettings["password"]
      self.last_error_sensor = self.logsettings["last_error_sensor"]
      self.camera_name = self.camsettings["camera_name"]
 
      repeat = int(self.alarmsettings["sensor_update_time"])
      self.motion_sensor = self.alarmsettings["motion_sensor"]
      self.soundalarm_sensor = self.alarmsettings["soundalarm_sensor"]
      self.motion_switch = self.alarmsettings["motion_switch"]

      self.brightness_slider = self.picsettings["brightness_slider"]
      self.contrast_slider = self.picsettings["contrast_slider"]
      self.hue_slider = self.picsettings["hue_slider"]
      self.saturation_slider = self.picsettings["saturation_slider"]
      self.sharpness_slider = self.picsettings["sharpness_slider"]
      self.default_pic_settings_switch = self.picsettings["default_pic_settings_switch"]
      self.mirror_switch = self.picsettings["mirror_switch"]
      self.flip_switch = self.picsettings["flip_switch"]

      self.recording_sensor = self.recordsettings["recording_sensor"]
      self.snap_picture_switch = self.recordsettings["snap_picture_switch"]
      self.save_snap_dir = self.recordsettings["save_snap_dir"]
    except:
      self.log("some arguments are not given or wrong", level = "ERROR")
      return
    if self.infraredcam:
      try:
        self.infrared_switch = self.picsettings["infrared_switch"]
        self.auto_infrared_switch = self.picsettings["auto_infrared_switch"]
      except:
        self.log("some infrared arguments are not given or wrong and you selected an infraredcam", level = "ERROR")
        return
    if self.PTZ:
      try:
        self.up_down_slider = self.ptzsettings["up_down_slider"]
        self.left_right_slider = self.ptzsettings["left_right_slider"]
        self.zoom_slider = self.ptzsettings["zoom_slider"]
        self.preset_points_select = self.ptzsettings["preset_points_select"]
        self.start_cruise_select = self.ptzsettings["start_cruise_select"]
        self.stop_cruise_switch = self.ptzsettings["stop_cruise_switch"]
      except:
        self.log("some PTZ arguments are not given or wrong and you selected a PTZ cam", level = "ERROR")
        return

    self.run_every(self.get_sensors,runtime,repeat)        

    self.listen_state(self.snap_picture,self.snap_picture_switch)
    self.url = "http://"+ self.camhost + ":" + str(self.portnr) + "/cgi-bin/CGIProxy.fcgi?&usr=" + self.user + "&pwd=" + self.password + "&cmd="
    self.listen_state(self.input_boolean_changed, self.mirror_switch, on_command="mirrorVideo&isMirror=1", off_command="mirrorVideo&isMirror=0", reset=False)
    self.listen_state(self.input_boolean_changed, self.flip_switch, on_command="flipVideo&isFlip=1", off_command="flipVideo&isFlip=0", reset=False)
    self.listen_state(self.pic_setting_input_slider_changed,self.brightness_slider,settingstype = "Brightness")
    self.listen_state(self.pic_setting_input_slider_changed,self.contrast_slider,settingstype = "Contrast")
    self.listen_state(self.pic_setting_input_slider_changed,self.hue_slider,settingstype = "Hue")
    self.listen_state(self.pic_setting_input_slider_changed,self.saturation_slider,settingstype = "Saturation")
    self.listen_state(self.pic_setting_input_slider_changed,self.sharpness_slider,settingstype = "Sharpness")
    self.listen_state(self.pic_setting_input_slider_changed,self.default_pic_settings_switch,settingstype = "Default")
    self.pic_setting_input_slider_changed("","","","",{"settingstype":"JustCheck"})
    if self.PTZ:
      self.listen_state(self.input_select_changed, self.preset_points_select, on_command="ptzGotoPresetPoint&name=")
      self.listen_state(self.input_select_changed, self.start_cruise_select, on_command="ptzStartCruise&mapName=")
      self.listen_state(self.input_slider_changed, self.zoom_slider, stop_command="zoomStop", speed_command="setZoomSpeed&speed=", left_command="zoomOut", right_command="zoomIn")
      self.listen_state(self.input_slider_changed, self.up_down_slider, stop_command="ptzStopRun", speed_command="setPTZSpeed&speed=", left_command="ptzMoveDown", right_command="ptzMoveUp")
      self.listen_state(self.input_slider_changed, self.left_right_slider, stop_command="ptzStopRun", speed_command="setPTZSpeed&speed=", left_command="ptzMoveLeft", right_command="ptzMoveRight")
      self.listen_state(self.input_boolean_changed, self.stop_cruise_switch, on_command="ptzStopCruise", reset=True)
    if self.infraredcam:
      self.listen_state(self.input_boolean_changed, self.infrared_switch, on_command="openInfraLed", off_command="closeInfraLed", reset=False)
      self.listen_state(self.input_boolean_changed, self.auto_infrared_switch, on_command="setInfraLedConfig&mode=0", off_command="setInfraLedConfig&mode=1", reset=False)

    if self.dashboardsettings["use_dashboard"]:
      self.fullscreenalarm = self.dashboardsettings["full_screen_alarm_switch"]
      if self.dashboardsettings["show_full_screen_dashboard"]:
        self.lastshown = datetime.datetime.now()
        self.listen_state(self.toondash,self.motion_sensor,constrain_input_boolean=self.fullscreenalarm)
      if self.dashboardsettings["create_dashboard"]:
        self.create_dashboard()
      if self.dashboardsettings["create_alarm_dashboard"]:
        self.create_alarm_dashboard()
    self.log(" App started without errors", "INFO")
    self.set_state(self.last_error_sensor, state = self.time().strftime("%H:%M:%S") + " App started without errors")

  def get_sensors(self, kwargs):
    data = self.send_command("getDevState")
    if data == "":
      return
    DevState = untangle.parse(data)
    try:
      motion_alarm = DevState.CGI_Result.motionDetectAlarm.cdata  
      if motion_alarm == "0":
        motion_alarm_text = "Disabled"
      elif motion_alarm == "1":
        motion_alarm_text = "No Alarm"
      elif motion_alarm == "2":
        motion_alarm_text = "Alarm!"

      sound_alarm = DevState.CGI_Result.soundAlarm.cdata  
      if sound_alarm == "0":
        sound_alarm_text = "Disabled"
      elif sound_alarm == "1":
        sound_alarm_text = "No Alarm"
      elif sound_alarm == "2":
        sound_alarm_text = "Alarm!"

      recording = DevState.CGI_Result.record.cdata  
      if recording == "0":
        recording_text = "No"
      elif recording == "1":
        recording_text = "Yes"
      infrared = DevState.CGI_Result.infraLedState.cdata  

      self.set_state(self.motion_sensor,state = motion_alarm_text)
      self.set_state(self.soundalarm_sensor,state = sound_alarm_text)
      self.set_state(self.recording_sensor,state = recording_text)
      if motion_alarm == "0":
        self.turn_off(self.motion_switch)
      else:
        self.turn_on(self.motion_switch)
      if infrared == "0":
        self.turn_off(self.infrared_switch)
      else:
        self.turn_on(self.infrared_switch)
    except:
      self.my_log(" Unexpected error", "WARNING")
      self.log(data, level = "WARNING")
    data = self.send_command("getInfraLedConfig")
    if data == "":
      return
    DevState = untangle.parse(data)
    infraredstate = DevState.CGI_Result.mode.cdata  
    if infraredstate == "1":
      self.turn_off(self.auto_infrared_switch)
    else:
      self.turn_on(self.auto_infrared_switch)
    data = self.send_command("getMirrorAndFlipSetting")
    if data == "":
      return
    DevState = untangle.parse(data)
    mirrorstate = DevState.CGI_Result.isMirror.cdata  
    if mirrorstate == "0":
      self.turn_off(self.mirror_switch)
    else:
      self.turn_on(self.mirror_switch)
    flipstate = DevState.CGI_Result.isFlip.cdata  
    if flipstate == "0":
      self.turn_off(self.flip_switch)
    else:
      self.turn_on(self.flip_switch)


  def input_boolean_changed(self, entity, attribute, old, new, kwargs):   
    if new == "on":
      data = self.send_command(kwargs["on_command"])
    else:
      if "off_command" in kwargs:
        data = self.send_command(kwargs["off_command"])
      else:
        return
    if "<result>0</result>" in data:
      self.my_log(" Changed " + self.friendly_name(entity), "INFO")
    else: 
      self.my_log("Failed to change " + self.friendly_name(entity), "WARNING")
    if kwargs["reset"]:
      self.turn_off(entity)


  def input_select_changed(self, entity, attribute, old, new, kwargs):   
    data = self.send_command(kwargs["on_command"] + new)
    if "<result>0</result>" in data:
      self.my_log("Changed " + self.friendly_name(entity),"INFO")
    else: 
      self.my_log("Failed to change " + self.friendly_name(entity), "WARNING")


  def input_slider_changed(self, entity, attribute, old, new, kwargs):
    data0 = ""
    data1 = ""
    data2 = ""
    if float(new) == 0:
      data0 = self.send_command(kwargs["stop_command"])
      if "<result>0</result>" in data0:
        self.my_log("Stopped" + self.friendly_name(entity), "INFO")
      elif data0 == "": 
        self.my_log("Failed to stop " + self.friendly_name(entity), "WARNING")
      else:
        self.log(data0, "WARNING")
    elif float(new) > 0:
      data1 = self.send_command(kwargs["speed_command"] + str((float(new)-1))[:-2])
      data2 = self.send_command(kwargs["right_command"])
      self.run_in(self.reset_after_a_second,1,entityname=entity)
    elif float(new) < 0:
      data1 = self.send_command(kwargs["speed_command"] + str((-float(new)-1))[:-2])
      data2 = self.send_command(kwargs["left_command"])
      self.run_in(self.reset_after_a_second,1,entityname=entity)

    if float(new) != 0:
      if "<result>0</result>" in data1:
        self.my_log("Speed set", "INFO")
      elif data1 == "": 
        self.my_log("Failed to set speed", "WARNING")
      else:
        self.log(data1)
      if "<result>0</result>" in data2:
        self.my_log("Started " + self.friendly_name(entity), "INFO")
      elif data2 == "": 
        self.my_log("Failed to start " + self.friendly_name(entity), "WARNING")
      else:
        self.log(data2)


  def pic_setting_input_slider_changed(self, entity, attribute, old, new, kwargs):
    if kwargs["settingstype"] != "Default" and  kwargs["settingstype"] != "JustCheck":
      if kwargs["settingstype"] == "Contrast":
        data = self.send_command("setContrast&constrast=" + new)
      else:
        data = self.send_command("set" + kwargs["settingstype"] + "&" + kwargs["settingstype"].lower() + "=" + new)
    else:
      if  kwargs["settingstype"] == "Default":     
        data = self.send_command("resetImageSetting")
        self.turn_off(self.default_pic_settings_switch)
      data = self.send_command("getImageSetting")
      if data == "":
        self.my_log("Failed to get settingsdata", "WARNING")
        return
      try:     
        pic_settings = untangle.parse(data)
        brightness = pic_settings.CGI_Result.brightness.cdata 
        contrast = pic_settings.CGI_Result.contrast.cdata  
        hue = pic_settings.CGI_Result.hue.cdata 
        saturation = pic_settings.CGI_Result.saturation.cdata  
        sharpness = pic_settings.CGI_Result.sharpness.cdata
        self.call_service("input_slider/select_value", entity_id=(self.brightness_slider), value=brightness)
        self.call_service("input_slider/select_value", entity_id=(self.contrast_slider), value=contrast)
        self.call_service("input_slider/select_value", entity_id=(self.hue_slider), value=hue)
        self.call_service("input_slider/select_value", entity_id=(self.saturation_slider), value=saturation)
        self.call_service("input_slider/select_value", entity_id=(self.sharpness_slider), value=sharpness)  
      except:
        self.my_log("image setting got wrong data", "WARNING")


  def snap_picture(self, entity, attribute, old, new, kwargs):
    if new == "on":
      savetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
      try:
        urllib.request.urlretrieve(self.url + "snapPicture2",self.save_snap_dir + savetime + ".jpg")
      except:
        self.my_log("Failed to snap picture", "WARNING")
      self.turn_off(entity)


  def reset_after_a_second(self, kwargs):
    self.call_service("input_slider/select_value", entity_id=kwargs["entityname"], value="0")


  def send_command(self, command):
    try:
      with urlopen(self.url + command, timeout=10) as response:
        data = response.read().decode()
    except timeout:
      self.my_log(" Camera took more then 10 seconds", "WARNING")
      return ""
    if "<result>0</result>" in data:
      self.my_log(" Camera state ok", "INFO")
      return data
    elif "<result>-1</result>" in data:
      self.my_log(" String format error", "WARNING")
      self.log(self.url + command)
      return ""
    elif "<result>-2</result>" in data:
      self.my_log(" Username or password error", "WARNING")
      return ""
    elif "<result>-3</result>" in data:
      self.my_log(" Access denied", "WARNING")
      return ""
    elif "<result>-4</result>" in data:
      self.my_log(" CGI execute failed", "WARNING")
      return ""
    elif "<result>-5</result>" in data:
      self.my_log(" Timeout", "WARNING")
      return ""
    else:
      self.my_log(" Unknown error", "WARNING")
      return ""

        
  def toondash(self, entity, attribute, old, new, kwargs):
    timegoneby = datetime.datetime.now() - self.lastshown
    if new == "Alarm!" and timegoneby > datetime.timedelta(seconds=self.dashboardsettings["time_between_shows"]):
      self.dash_navigate(self.dashboardsettings["alarm_dashboard_file_name"], self.dashboardsettings["show_time"])
      self.lastshown = datetime.datetime.now()


  def my_log(self, message, level = "INFO"):
    self.last_error = message
    if self.loglevels[level] >= self.loglevels[self.loglevel]:
      self.log(self.last_error, level = level)
    if self.loglevels[level] >= self.loglevels[self.logsensorlevel]:
      self.set_state(self.last_error_sensor, state = self.time().strftime("%H:%M:%S") + self.last_error)



  def create_dashboard(self):
    try:
      with open(self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["dashboard_file_name"] + ".dash", 'w') as dashboard:
        screenwidth = self.dashboardsettings["screen_width"]
        screenheight = self.dashboardsettings["screen_height"]
        widgetwidth = round((screenwidth - 22) / 10)
        widgetheight = round((screenheight - 14) / 6)
        dashboardlines = [
          'title: camera',
          'widget_dimensions: [' + str(widgetwidth) + ', ' + str(widgetheight) + ']',
          'widget_size: [1,1]',
          'widget_margins: [2, 2]',
          'columns: 10',
          'global_parameters:',
          '    use_comma: 1',
          '    precision: 0',
          '    use_hass_icon: 1',
          '',
          'layout:',
          '    - my_camera(7x4), ' + self.saturation_slider + '(2x1), ' + self.flip_switch,
          '    - ' + self.contrast_slider + '(2x1), ' + self.mirror_switch,
          '    - ' + self.brightness_slider + '(2x1), ' + self.auto_infrared_switch,
          '    - ' + self.hue_slider + '(2x1), ' + self.infrared_switch,
          '    - ' + self.left_right_slider + '(2x1), ' + self.zoom_slider + '(1x2), ' + self.preset_points_select + '(2x1), ' + self.motion_sensor + ', ' + self.default_pic_settings_switch + ',' + self.sharpness_slider + '(2x1), ' + self.motion_switch,
          '    - ' + self.up_down_slider + '(2x1), ' + self.start_cruise_select + '(2x1),' + self.recording_sensor + ', ' + self.soundalarm_sensor + ', ' + self.last_error_sensor + '(2x1), ' + self.snap_picture_switch,
          '',
          'my_camera:',
          '    widget_type: camera',
          '    entity_picture: ' + self.config["HASS"]["ha_url"] + '/api/camera_proxy_stream/camera.' + self.camera_name + '?api_password=' + self.config["HASS"]["ha_key"],
          '    title: ' + self.camera_name,
          '    refresh: 120',
          self.recording_sensor + ':',
          '    widget_type: sensor',
          '    entity: ' + self.recording_sensor,
          '    title: Recording',
          self.motion_sensor + ':',
          '    widget_type: sensor',
          '    entity: ' + self.motion_sensor,
          '    title: Motion',
          self.soundalarm_sensor + ':',
          '    widget_type: sensor',
          '    entity: ' + self.soundalarm_sensor,
          '    title: Sound alarm',
          self.saturation_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.saturation_slider,
          '    title: Saturation',
          self.contrast_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.contrast_slider,
          '    title: Contrast',
          self.brightness_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.brightness_slider,
          '    title: Brightness',
          self.hue_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.hue_slider,
          '    title: Hue',
          self.sharpness_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.sharpness_slider,
          '    title: Sharpness',
          self.left_right_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.left_right_slider,
          '    title: Move Left',
          '    title2: Move Right',
          self.up_down_slider + ':',
          '    widget_type: new_input_slider',
          '    entity: ' + self.up_down_slider,
          '    title: Move Up(right)',
          '    title2: Move Down(left)',
          self.zoom_slider + ':',
          '    widget_type: vertical_input_slider',
          '    entity: ' + self.zoom_slider,
          '    title: Zoom',
        ]
        for line in dashboardlines:
          dashboard.write(line + '\n')
    except IOError as e:
      self.log("I/O error({0}): {1} : dashboard couldnt be written".format(e.errno, e.strerror),"ERROR")
      self.log("tried to write: " + self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["dashboard_file_name"] + ".dash","ERROR")
    except TypeError:
      self.log("one of the arguments has the wrong type","ERROR")
    except ValueError:
      self.log("width or height isnt given as a correct integer","ERROR")
    except:
      self.log("unexpected error: dashboard couldnt be written", "ERROR")
      self.log("tried to write: " + self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["dashboard_file_name"] + ".dash","ERROR")


  def create_alarm_dashboard(self):
    try:
      with open(self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["alarm_dashboard_file_name"] + ".dash", 'w') as dashboard:
        screenwidth = self.dashboardsettings["screen_width"]
        screenheight = self.dashboardsettings["screen_height"]
        widgetwidth = round((screenwidth - 22) / 10)
        widgetheight = round((screenheight - 14) / 6)
        dashboardlines = [
          'title: camera',
          'widget_dimensions: [' + str(widgetwidth) + ', ' + str(widgetheight) + ']',
          'widget_size: [1,1]',
          'widget_margins: [2, 2]',
          'columns: 10',
          'global_parameters:',
          '    use_comma: 1',
          '    precision: 0',
          '    use_hass_icon: 1',
          '',
          'layout:',
          '    - my_camera(10x6)',
          '',
          'my_camera:',
          '    widget_type: camera',
          '    entity_picture: ' + self.config["HASS"]["ha_url"] + '/api/camera_proxy_stream/camera.' + self.camera_name + '?api_password=' + self.config["HASS"]["ha_key"],
          '    title: ' + self.camera_name,
        ]
        for line in dashboardlines:
          dashboard.write(line + '\n')
    except IOError as e:
      self.log("I/O error({0}): {1} : dashboard couldnt be written".format(e.errno, e.strerror),"ERROR")
      self.log("tried to write: " + self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["alarm_dashboard_file_name"] + ".dash")
    except TypeError:
      self.log("one of the arguments has the wrong type","ERROR")
    except ValueError:
      self.log("width or height isnt given as a correct integer","ERROR")
    except:
      self.log("unexpected error: dashboard couldnt be written", "ERROR")
      self.log("tried to write: " + self.config["HADashboard"]["dash_dir"] + "/" + self.dashboardsettings["alarm_dashboard_file_name"] + ".dash")
