here you find the apps i created

some apps are not up to date with the latest appdaemon version.
the apps that have a cfg file type need to be updated.
changing cfg to yaml is like this:

in appdaemon.cfg
```
[some_app_name]
module = any_module
class = some_class
any_arg = arg_value
```
goes to
in apps.yaml
```
some_app_name:
  module: any_module
  class: some_class
  any_arg: arg_value
```
