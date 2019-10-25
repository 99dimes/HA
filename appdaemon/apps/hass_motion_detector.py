import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timedelta

class Motion_Detector(hass.Hass):
    def initialize(self):
        # initialize external hass modules
        self.broadcast = self.get_app("GoogleBroadcast")
        self.hass_util = self.get_app("HassUtil")
        self.timer = self.get_app("TimerUtilities")
        self.emailutil = self.get_app("EmailUtil")
        # initialize app parameters
        self.sensor = self.args["sensor"]
        self.entity = self.args["entity"]

        # finds duration param, if filled
        if("duration" in self.app_config[self.name]):
            self.duration = self.args["duration"]
            self.log("The duration parameter was " + str(self.duration))
        else:
            self.duration = 240
            self.log("I did not find duration param")

        # finds constrain_end_time param, if filled
        if ("constrain_end_time" in self.app_config[self.name]):
            self.end_time = str(self.args['constrain_end_time'])
            self.datetime_end_time = datetime.strptime(self.end_time, '%H:%M:%S').time()
            self.turn_off_time = datetime.combine(datetime.now(), self.datetime_end_time)
        else:
            self.turn_off_time = datetime.combine(datetime.now(), datetime.strptime('23:59:59', '%H:%M:%S').time())

        # If constrain end time is before now a day will be added to avoid an error at runtime
        if (self.turn_off_time < datetime.now()):
            self.turn_off_time = self.turn_off_time + timedelta(days=1)

        # turn on all lights in the designated group
        self.entity_id_list = self.hass_util.split_group(self.entity)
        self.handle = self.listen_state(self.light_handler_callback, self.sensor, new="on", old="off")

        # If constrain end time is before now plus self.duration then the lights will turn off at constrain end time
        if (self.turn_off_time < datetime.now() + timedelta(seconds=self.duration)):
            self.log("time is less than app cutoff date, lights will turn off at constrain end time")
            self.set_off_time_handle = self.run_at(self.light_handler_off_callback, self.turn_off_time)
        else:
            self.handle_off = self.listen_state(self.light_handler_off_callback, self.sensor, new="off",
                                                old="off", duration=self.duration)
        
    def light_handler_callback(self, entity, attribute, old, new, *args):
        for light in self.entity_id_list:
            self.turn_on(light)

    def light_handler_off_callback(self, entity, *args):
        for light in self.entity_id_list:
            self.log("Its supposed to be turning off")
            self.log(self.turn_off_time)
            self.turn_off(light)
            ##
            #self.cancel_listen_state(self.handle_off)


#self.set_state(light, state="on", attributes={"brightness": self.isLateBrightness})
#self.turn_on(light, brightness = self.isLateBrightness)
#self.handle_off = self.run_in(self.light_handler_off_callback, 2) #self.duration)