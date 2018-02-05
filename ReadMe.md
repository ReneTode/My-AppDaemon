# My-AppDaemon
My apps, my helpfiles, all about AppDaemon for Home Assistant

## Apps

my apps are still written for appdaemon version 2. There have been some changes in appdaemon 3.
That doesnt effect much from my apps, but 2 things should be changed if you use version 3:
when you read the line:
```
import appdaemon.appapi as appapi
```
replace that with:
```
import appdaemon.plugins.hass.hassapi as hass
```
and when you see:
```
appapi.AppDaemon
```
replace that with:
```
hass.Hass
```
in the near future i will change my apps to version 3


1) Foscam V1 (an app for controlling a  foscam camera) for older versions from appdaemon and homeassistant
2) Foscam V2 (the new version with automatic generated dashboards and better errors)
3) Sound (tts and soundcontrol directly in the app)
4) lightschedule (a clear view on when you turn on and off your lights)
5) google assistant as app controlable drom home assistant
6) groups 2.0 (an app to use wildcards for groups)
7) alexa (an app to let alexa communicate with appdaemon)(already version 3!)

## custom Widgets for HADashboard

1) input_select (default in appdaemon version 3)
2) horizontal slider (default in appdaemon version 3)
3) vertical slider
4) lightswitch with brightness slider
5) lightswitch with colorpicker
6) thermometer (fully customisable) (default in appdaemon version 3)
7) radial (fully customisable) (default in appdaemon version 3)
8) combination from switch and input_slider (heater)
9) icon sensor

## custom css

1) waterdrops skin
2) variables.yaml extra variables for custom widgets 
3) LCARS skin



