version 1 is only for the new type foscam cameras.
I am working on version 2 which also has support for older types.

points i am working on:
1) better feedback for known problems (if the cam is busy, some functions dont work for a short moment)
2) implementing older cam types.
3) reparing some small problems
4) Dashboard for HAdashboard.

expected time: oktober.

to use this version:
1) install Appdaemon (if you havent already)
2) place the foscam.py in your Appdirectory
3) edit the appdaemon.cfg with the parts i provided in appdaemon.cfg
4) edit your HomeAssistant YAML files and add the things you find in the YAML file i provided.

when finished it should look like:

![screenshot](foscam2.jpg)

note: this version was created for older versions from Appdaemon
in the newer versions the cfg file is replaced with an yaml file.
for the newest version from Appdaemon replace step 3 with

3) edit the app.yaml with the parts i provided in app.yaml
