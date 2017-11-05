###########################################################################################
#                                                                                         #
#  Rene Tode ( hass@reot.org )                                                            #
#  2017/11/06 Germany                                                                     #
#                                                                                         #
###########################################################################################

import appdaemon.appapi as appapi
import datetime

class stardate(appapi.AppDaemon):

  def initialize(self):
    self.run_at_sunrise(self.set_stardate)
    self.set_stardate(self)

  def set_stardate(self, kwargs):
    century="1"
    today = datetime.datetime.now()
    startdate = datetime.datetime(2000, 1, 1, 0, 0)
    daysgone=today-startdate   
    days_gone = round((daysgone.days/10)*2.73785,1)
    self.log("STARDATE:"+ century + str(days_gone))
    self.set_state("sensor.stardate",state="STARDATE:"+ century + str(days_gone))

