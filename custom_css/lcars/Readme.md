# The LCARS skin for HADashboard

![Alt text](lcars12.jpg)

using this skin is really easy if you have appdaemon/hadashboard installed.
all you need is a directory named custom_css in your conf(iguration) directory
there you create the lcars directory.
in the lcars directory you need to place all files.
- dashboard.css
- variables.yaml
- the subdir font with everything in it
- the subdir img with everything in it

if you want to use a calculated stardate the read how to do it below.

the skin has a background that can be used with different resolutions.
i created example dashboards for 3 different resolutions, but you also can change the settings yourself.

here are the settings you need to change for different resolutions

## 800 x 480 (untested size)
- in variables.yaml set **screenwidth: 1024** to 800
- in dashboard.css change   **background-size: 1024px;** to 800
- in the dashboard use the settings:
```
  widget_dimensions: [93, 18]
  widget_margins: [5, 2]
```
  and you might need to change
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```
to get the stardate at the right position

## 1024 x 600 (default size)
- in the dashboard use the settings:
```
  widget_dimensions: [119, 23]
  widget_margins: [7, 3]
```
  and use
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```

## 1280 x 768
- in variables.yaml set **screenwidth: 1024** to 1280
- in dashboard.css change   **background-size: 1024px;** to 1280
- in the dashboard use the settings:
```
  widget_dimensions: [149, 29]
  widget_margins: [9, 4]
```
  and change
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```
to get the stardate at the right position

## 1600 x 900
- in variables.yaml set **screenwidth: 1024** to 1600
- in dashboard.css change   **background-size: 1024px;** to 1600
- in the dashboard use the settings:
```
  widget_dimensions: [186, 35]
  widget_margins: [11, 5]
```
  and change
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```
to get the stardate at the right position

## 1920 x 1080 (untested)
- in variables.yaml set **screenwidth: 1024** to 1920
- in dashboard.css change   **background-size: 1024px;** to 1920
- in the dashboard use the settings:
```
  widget_dimensions: [223, 41]
  widget_margins: [21, 8]
```
  and you might need to change
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```
to get the stardate at the right position

## 2560 x 1600 (untested)
- in variables.yaml set **screenwidth: 1024** to 2560
- in dashboard.css change   **background-size: 1024px;** to 2560
- in the dashboard use the settings:
```
  widget_dimensions: [298, 61]
  widget_margins: [23, 11]
```
  and you might need to change
  ```
stardate:
  container_style: "top: 6px" #6px for 1024, 18px for 1280, 28px for 1600
```
to get the stardate at the right position

# Calculated Stardate

i created an app that calculates the stardate. there is no exact way to calculate it because it was never a formula.
but i did some research and created a formula that comes close to how it was used.
if you want to use the calculated stardate then do this:
- add the stardate.py to your apps directory
- add these lines to your apps.yaml:
```
stardate:
  module: stardate
  class: stardate
```
if your appdaemon is configured right you now will get a sensor called sensor.stardate in homeassistant
dont mind the warning that appdaemon gives that that sensor doesnt exist. thats because we create it.

now you can use that sensor in any dashboard or in home assistant or in apps.

# supported widgets

at this moment i cant create all widgets that the dashboard has. that would only be possible if i change some basic parts from the widgets. it could very well be that other widgets also will be included as soon as this skin becomes a basic skin from hadashboard.
right now you can use:
- sensor (you can also show every state from any entity, like devicetrackers, switches,inputselects, etc)
- switch (it can switch lights,switches,input_booleans, or anything with on and off state)
- camera
- label
- iframe
- navigate

please take a look at the examples how to use them. i give the basic possibilities here.

you can use 9 different default colors
- $lcar_color_1 (default text color), $lcar_color_2, ... $lcar_color_8
- $transparant (mainly for background)

## sensor (2x1)
- the specific stardate sensor
```
stardate:
  widget_type: sensor
  entity: sensor.stardate
  text_style: "$sensor_text_stardate"
  container_style: "top: 6px"
  widget_style: "background-color:$transparant"
```
- normal sensors
```
sensorname:
  widget_type: sensor
  entity: switch.your_sensor
  title: the text before the value
  title_style: "$title_left"
  container_style: "$sensor_container_right"
  units: ""
```
## switch (1x2)
- use button_title_left or button_title_right
- use button_widget_right or button_widget_left
- use button_icon_active_right or button_icon_active_left
```
switchname:
  widget_type: switch
  entity: switch.your_switch
  title: halllight
  title_style: "$button_title_left"
  widget_style: "$button_widget_right;background-color:$lcar_color_4"
  icon_style_active: "$button_icon_active_right"
```
## camera
actualy not real different from the default skin
```
mycamera:
  widget_type: camera
  title: Captains seat
  entity_picture: http://yourip:8123/api/camera_proxy/camera.yourcam?api_password=yourpassword
  widget_style: "background-image: none"
  refresh: 60
```  
## label (menusize (1x2))
there are 2 default labels:
```
Dashboard_title:
  widget_type: label
  title: DASHBOARD
  title_style: "$label_title_dashname"
  widget_style: "background-color:$transparant"
menutop:
  widget_type: label
  title: Menu
  title_style: "$label_title_menu"
  widget_style: "background-color:$lcar_color_7"
```
## iframe
also use for the logo
```
logo:
  widget_type: iframe
  widget_style: "border-bottom-left-radius: 30px;border-bottom-right-radius: 30px"
  img_list: 
    - http://yourip:5050/custom_css/lcars/img/acces_granted.jpg
```
## navigate (menusize(1x2))
used for the menu
```
menu1:
  widget_type: navigate
  title: Livingroom
  dashboard: your_dashname
  title_style: "$label_title_menu"
  widget_style: "background-color:$lcar_color_5"
```

# Basic layout
the layout needs to be created for the background.
you can find examples for the most ordinairy resolutions.

this is the most basic frame:
```
layout:
  - spacer(1x2),  spacer(1x2),  spacer(1x2),  spacer(1x2),  spacer(1x2),  spacer(1x2),  Dashboard_title(2x2)
  -
  -
  -
  - menutop(1x2)       
  -
  - menu1(1x2)
  - 
  - menu2(1x2)
  -
  -
  -
  - 
  -
  - 
  -
  - 
  -
  - 
  - 
  - 
  - spacer(1x2),  spacer(1x2),  stardate(1x2)
  ```
  
  # support and ideas
  
  if you come to any problems, have any suggestions or if you have other questions:
  https://community.home-assistant.io/t/skin-lcars-star-trek-beta/31386
  




