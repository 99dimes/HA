import appdaemon.plugins.hass.hassapi as hass

class Button_Toggle(hass.Hass):
    def initialize(self):
        self.entity_list = list()
        self.hass_util = self.get_app("HassUtil")

        self.sensor = self.args["button"]
        self.light = self.args["single"]
        self.single_entity_list = self.hass_util.split_group(entity=self.light)

        self.double_light = self.args["double_light"]
        self.double_entity_list = self.hass_util.split_group(entity=self.double_light)

        self.long_light = self.args["long_light"]
        self.long_entity_list = self.hass_util.split_group(entity=self.long_light)

        self.listen_state(self.long_callback4, self.sensor, new="long")
        self.listen_state(self.double_callback, self.sensor, new="double")
        self.listen_state(self.single_callback, self.sensor, new="single")

    # changed 10/6/19 as a reset for the lights state. In case one doesn't turn off
    def long_callback4(self, *args):
        self.log("I read a long")
        for l in self.long_entity_list:
            self.turn_off(l)

    def long_callback2(self, *args):
        self.log("I read a long")
        for l in self.long_entity_list:
            self.turn_on(l, rgb_color=[81, 255, 81])

    def long_callback1(self, *args):
        self.log("I read a long 1")
        duration = self.get_state(self.sensor, attribute="duration")
        if (duration >= 400):
            for l in self.long_entity_list:
                self.turn_on(l, rgb_color=[81, 82, 255])
        if (duration > 200 and duration < 400):
            for l in self.long_entity_list:
                self.turn_on(l, rgb_color=[81, 255, 81])
        if (duration > 100 and duration < 200):
            for l in self.long_entity_list:
                self.turn_on(l, rgb_color=[255, 82, 81])

    def double_callback(self, *args):
        for l in self.double_entity_list:
            self.toggle(l)

    def single_callback(self,*args):
        self.log("I read a single")
        for l in self.single_entity_list:
            self.toggle(l)

    def split_group(self, entity):
        if ("group" in entity):
            self.log("I found a group")
            self.entity_list = self.hass_util.get_entities_from_group(entity)
            return self.entity_list
        else:
            self.log("I found a single entity")
            self.entity_id_list = list()
            self.entity_id_list.append(entity)
            return self.entity_id_list


