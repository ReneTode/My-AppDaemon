###########################################################################################
#                                                                                         #
#  Rene Tode ( hass@reot.org )                                                            #
#                                                                                         #
#  2016/04/28 Germany                                                                     #
#                                                                                         #
#  an app to control a foscam PTZ camera.                                                 #
#  dependecies:                                                                           #
#    untangle (pip install untangle)                                                      #
#                                                                                         #
#  args:                                                                                  #
#    host = "host_ip"                                                                     #
#    port = "88"                                                                          #
#    user = "cam_user_name"                                                               #
#    password = "cam_password"                                                            #
#    save_snap_dir = "/home/pi/foscam_snap/" # dir where you save the snapshots           #
#                                                                                         #
#    sensor_update_time = 10                                                              #
#    motion_sensor = "sensor.foscam_motion"             # sensors are created automaticly #
#    recording_sensor = "sensor.foscam_recording"                                         #
#    soundalarm_sensor = "sensor.foscam_sound_alarm"                                      #
#                                                                                         #
#    up_down_slider = "input_slider.foscam_up_down"        # create these sliders in HA   #
#    left_right_slider = "input_slider.foscam_left_right"                                 #
#    zoom_slider = "input_slider.foscam_zoom"                                             #
#    brightness_slider = "input_slider.foscam_brightness"                                 #
#    contrast_slider = "input_slider.foscam_contrast"                                     #
#    hue_slider = "input_slider.foscam_hue"                                               #
#    saturation_slider = "input_slider.foscam_saturation"                                 #
#    sharpness_slider = "input_slider.foscam_sharpness"                                   #
#                                                                                         #
#    infrared_switch = "input_boolean.foscam_infrared"             # create these         #
#    auto_infrared_switch = "input_boolean.foscam_auto_infrared"   # input_booleans in HA #
#    stop_cruise_switch = "input_boolean.foscam_stop_cruise"                              #
#    motion_switch = "input_boolean.foscam_motion_detect"                                 #
#    default_pic_settings_switch = "input_boolean.foscam_default_picture_settings"        #
#    mirror_switch = "input_boolean.foscam_mirror"                                        #
#    flip_switch = "input_boolean.foscam_flip"                                            #
#    snap_picture_switch = "input_boolean.foscam_snap_picture_now"                        #
#                                                                                         #
#    preset_points_select = "input_select.foscam_preset_points" # create these input      #
#    start_cruise_select = "input_select.foscam_preset_cruise"  # selects in HA           #
#                                                                                         #
#                                                                                         #
###########################################################################################

import appdaemon.appapi as appapi
import datetime
import untangle
from urllib.request import urlopen
import urllib.request
import time

class foscam(appapi.AppDaemon):

  def initialize(self):
    self.host = self.args["host"]
    self.port = self.args["port"]
    self.user = self.args["user"]
    self.password = self.args["password"]
    repeat = int(self.args["sensor_update_time"])
    self.motion_sensor = self.args["motion_sensor"]
    self.recording_sensor = self.args["recording_sensor"]
    self.soundalarm_sensor = self.args["soundalarm_sensor"]
    self.up_down_slider = self.args["up_down_slider"]
    self.left_right_slider = self.args["left_right_slider"]
    self.infrared_switch = self.args["infrared_switch"]
    self.auto_infrared_switch = self.args["auto_infrared_switch"]
    self.motion_switch = self.args["motion_switch"]
    self.zoom_slider = self.args["zoom_slider"]
    self.preset_points_select = self.args["preset_points_select"]
    self.start_cruise_select = self.args["start_cruise_select"]
    self.stop_cruise_switch = self.args["stop_cruise_switch"]
    self.brightness_slider = self.args["brightness_slider"]
    self.contrast_slider = self.args["contrast_slider"]
    self.hue_slider = self.args["hue_slider"]
    self.saturation_slider = self.args["saturation_slider"]
    self.sharpness_slider = self.args["sharpness_slider"]
    self.default_pic_settings_switch = self.args["default_pic_settings_switch"]
    self.mirror_switch = self.args["mirror_switch"]
    self.flip_switch = self.args["flip_switch"]
    self.snap_picture_switch = self.args["snap_picture_switch"]
    self.save_snap_dir = self.args["save_snap_dir"]

    self.url = "http://"+ self.host + ":" + self.port + "/cgi-bin/CGIProxy.fcgi?&usr=" + self.user + "&pwd=" + self.password + "&cmd="
    runtime = datetime.datetime.now()
    
    self.run_every(self.get_sensors,runtime,repeat)        
    self.listen_state(self.move_up_down,self.up_down_slider)
    self.listen_state(self.move_left_right,self.left_right_slider)
    self.listen_state(self.zoom,self.zoom_slider)
    self.listen_state(self.move_to,self.preset_points_select)
    self.listen_state(self.start_cruise,self.start_cruise_select)
    self.listen_state(self.stop_cruise,self.stop_cruise_switch)
    self.listen_state(self.set_pic_setting,self.brightness_slider,settingstype = "Brightness")
    self.listen_state(self.set_pic_setting,self.contrast_slider,settingstype = "Contrast")
    self.listen_state(self.set_pic_setting,self.hue_slider,settingstype = "Hue")
    self.listen_state(self.set_pic_setting,self.saturation_slider,settingstype = "Saturation")
    self.listen_state(self.set_pic_setting,self.sharpness_slider,settingstype = "Sharpness")
    self.listen_state(self.set_pic_setting,self.default_pic_settings_switch,settingstype = "Default")
    self.listen_state(self.flip_it,self.flip_switch)
    self.listen_state(self.mirror_it,self.mirror_switch)
    self.listen_state(self.use_infrared,self.infrared_switch)
    self.listen_state(self.auto_infrared,self.auto_infrared_switch)
    self.listen_state(self.snap_picture,self.snap_picture_switch)


  def get_sensors(self, kwargs):
    #self.log(self.url + "getDevState")
    try:
      DevState = untangle.parse(self.url + "getDevState")
      motion_alarm = DevState.CGI_Result.motionDetectAlarm.cdata  # 0-Disabled, 1-No Alarm, 2-Detect Alarm
      self.set_state(self.motion_sensor,state = motion_alarm)
      if motion_alarm == "0":
        self.turn_off(self.motion_switch)
      else:
        self.turn_on(self.motion_switch)
      sound_alarm = DevState.CGI_Result.soundAlarm.cdata  # 0-Disabled, 1-No Alarm, 2-Detect Alarm
      self.set_state(self.soundalarm_sensor,state = sound_alarm)
      recording = DevState.CGI_Result.record.cdata  # 0-not recording, 1-recording
      self.set_state(self.recording_sensor,state = recording)
      infrared = DevState.CGI_Result.infraLedState.cdata  # 0-Off, 1-On
      if infrared == "0":
        self.turn_off(self.infrared_switch)
      else:
        self.turn_on(self.infrared_switch)
    except:
      self.log("devstate gaf foute data")
    try:
      pic_settings = untangle.parse(self.url + "getImageSetting")
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
      self.log("image setting gaf foute data")


  def move_up_down(self, entity, attribute, old, new, kwargs):
    if float(new) == 0:
      data = urlopen(self.url + "ptzStopRun").read().decode()
    elif float(new) > 0:
      data = urlopen(self.url + "setPTZSpeed&speed=" + str(5-(float(new)-1))).read().decode()
      data = urlopen(self.url + "ptzMoveUp").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.up_down_slider), value="0")
    elif float(new) < 0:
      data = urlopen(self.url + "setPTZSpeed&speed=" + str(5-(-float(new)-1))).read().decode()
      data = urlopen(self.url + "ptzMoveDown").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.up_down_slider), value="0")
 

  def move_left_right(self, entity, attribute, old, new, kwargs):
    if float(new) == 0:
      data = urlopen(self.url + "ptzStopRun").read().decode()
    elif float(new) > 0:
      data = urlopen(self.url + "setPTZSpeed&speed=" + str(5-(float(new)-1))).read().decode()
      data = urlopen(self.url + "ptzMoveRight").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.left_right_slider), value="0")
    elif float(new) < 0:
      data = urlopen(self.url + "setPTZSpeed&speed=" + str(5-(-float(new)-1))).read().decode()
      data = urlopen(self.url + "ptzMoveLeft").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.left_right_slider), value="0")


  def zoom(self, entity, attribute, old, new, kwargs):
    if float(new) == 0:
      data = urlopen(self.url + "zoomStop").read().decode()
    elif float(new) > 0:
      data = urlopen(self.url + "setZoomSpeed&speed=" + str(5-(float(new)-1))).read().decode()
      data = urlopen(self.url + "zoomIn").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.zoom_slider), value="0")
    elif float(new) < 0:
      data = urlopen(self.url + "setZoomSpeed&speed=" + str(5-(-float(new)-1))).read().decode()
      data = urlopen(self.url + "zoomOut").read().decode()
      time.sleep(1)
      self.call_service("input_slider/select_value", entity_id=(self.zoom_slider), value="0")

  
  def move_to(self, entity, attribute, old, new, kwargs):
    data = urlopen(self.url + "ptzGotoPresetPoint&name=" + new).read().decode()


  def start_cruise(self, entity, attribute, old, new, kwargs):
    data = urlopen(self.url + "ptzStartCruise&mapName=" + new).read().decode()


  def stop_cruise(self, entity, attribute, old, new, kwargs):
    data = urlopen(self.url + "ptzStopCruise").read().decode()
    self.turn_off(entity)

  def set_pic_setting(self, entity, attribute, old, new, kwargs):
    if kwargs["settingstype"] != "Default":
      data = urlopen(self.url + "set" + kwargs["settingstype"] + "&" + kwargs["settingstype"].lower() + "=" + new).read().decode()
    else:
      data = urlopen(self.url + "resetImageSetting").read().decode()
      self.turn_off(self.default_pic_settings_switch)


  def flip_it(self, entity, attribute, old, new, kwargs):
    if new == "on":
      data = urlopen(self.url + "flipVideo&isFlip=1").read().decode()
    else:
      data = urlopen(self.url + "flipVideo&isFlip=0").read().decode()


  def mirror_it(self, entity, attribute, old, new, kwargs):
    if new == "on":
      data = urlopen(self.url + "mirrorVideo&isMirror=1").read().decode()
    else:
      data = urlopen(self.url + "mirrorVideo&isMirror=0").read().decode()


  def use_infrared(self, entity, attribute, old, new, kwargs):
    if new == "on":
      data = urlopen(self.url + "openInfraLed").read().decode()
    else:
      data = urlopen(self.url + "closeInfraLed").read().decode()


  def auto_infrared(self, entity, attribute, old, new, kwargs):
    if new == "on":
      data = urlopen(self.url + "setInfraLedConfig&mode=0").read().decode()
    else:
      data = urlopen(self.url + "setInfraLedConfig&mode=1").read().decode()


  def snap_picture(self, entity, attribute, old, new, kwargs):
    if new == "on":
      savetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
      urllib.request.urlretrieve(self.url + "snapPicture2",self.save_snap_dir + savetime + ".jpg")
      self.turn_off(entity)
    
