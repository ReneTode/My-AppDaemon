## these are custom widgets for HADashboard


place the files in the directory /conf/custom_widgets

important! you need to use my custom skin waterdrops (to be found in custom css) or edit variables.yaml in your own skin or the default skin.   
the lines to add to the variables.yaml can be found on this github in custom_css/default/variables.yaml


usage in your dashboards:

```
title: Test dashboard
widget_dimensions: [120, 120]
widget_margins: [5, 5]
columns: 7

your_light:
  widget_type: light_with_brightness
  entity: light.any_light
  title: Just a
  title2: Light
your_light2:
  widget_type: light_with_colorpicker
  entity: light.any_light
  title: Just a
  title2: Light
your_vertical_slider:
  widget_type: vertical_input_slider
  entity: input_number.your_slider
  title: Just a
  title2: slider


layout:
    - your_light, your_light2, your_vertical_slider
    
```


