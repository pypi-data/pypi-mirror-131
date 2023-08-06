from lifx_plugin import Mixin
from lifx_plugin.message import Command as Parent


class SetColor(Parent):
    """Set the right color when turned on. When off it is not able to listen new commands.

    Use when the command is called time after the state is changed and the old_state is not different from new_state.
    Lifx Bulb takes almost 7 seconds to start and be able to listen new commands.

    >>> import home
    >>> import lifx
    >>> import lifx_plugin
    >>> old_state = home.appliance.light.indoor.hue.state.off.State()
    >>> new_state = old_state.next(home.appliance.light.event.hue.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.saturation.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.brightness.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.temperature.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.circadian_rhythm.hue.Event(40))
    >>> new_state = new_state.next(home.appliance.light.event.circadian_rhythm.saturation.Event(40))
    >>> new_state = new_state.next(home.appliance.light.event.circadian_rhythm.brightness.Event(40))
    >>> new_state = new_state.next(home.appliance.light.event.circadian_rhythm.temperature.Event(40))
    >>> new_state = new_state.next(home.appliance.light.event.lux_balancing.brightness.Event(50))
    >>> new_state = new_state.next(home.appliance.light.event.show.starting_brightness.Event(60))
    >>> new_state = new_state.next(home.appliance.light.event.show.starting_hue.Event(60))
    >>> new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> command = SetColor.make([["172.31.10.245", 56700], ])
    >>> msgs = command.make_msgs_from(old_state, new_state)
    >>> "brightness: 30" in str(lifx_plugin.Description.make_from(msgs[0]))
    True
    >>> new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.Not)
    >>> new_new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.CircadianRhythm)
    >>> msgs = command.make_msgs_from(new_state, new_new_state)
    >>> "brightness: 40" in str(lifx_plugin.Description.make_from(msgs[0]))
    True
    >>> new_new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.LuxBalance)
    >>> msgs = command.make_msgs_from(new_state, new_new_state)
    >>> "brightness: 50" in str(lifx_plugin.Description.make_from(msgs[0]))
    True
    >>> new_new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.Show)
    >>> msgs = command.make_msgs_from(new_state, new_new_state)
    >>> "brightness: 60" in str(lifx_plugin.Description.make_from(msgs[0]))
    True
    """

    State = {
        "type": "lifx",
        "name": "SetColor",
        "fields": {
            "hue": 0,
            "saturation": 0,
            "brightness": 100,
            "kelvin": 3500,
            "duration": 1024,
        },
        "addresses": [],
    }

    def make_msgs_from(
        self,
        old_state: Mixin,
        new_state: Mixin,
    ):
        result = []
        if new_state.is_on:
            self.state.kelvin = new_state.temperature
            self.state.duration = self.State["fields"]["duration"]
            if new_state.is_showing:
                self.state.hue = new_state.starting_hue
                self.state.brightness = new_state.starting_brightness
                self.state.saturation = new_state.starting_saturation
            else:
                self.state.saturation = new_state.saturation
                self.state.hue = new_state.hue
                self.state.brightness = new_state.brightness
            result = self.execute()
        return result


class SetWaveform(Parent):
    """Always set waveform when showing.

    Use when the command is called time after the state is changed and the old_state is not different from new_state.
    Lifx Bulb takes almost 7 seconds to start and be able to listen new commands.

    >>> import home
    >>> import lifx
    >>> import lifx_plugin
    >>> old_state = home.appliance.light.indoor.hue.state.off.State()
    >>> new_state = old_state.next(home.appliance.light.event.hue.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.saturation.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.brightness.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.temperature.Event(30))
    >>> new_state = new_state.next(home.appliance.light.event.show.starting_brightness.Event(60))
    >>> new_state = new_state.next(home.appliance.light.event.show.ending_brightness.Event(80))
    >>> new_state = new_state.next(home.appliance.light.event.show.starting_hue.Event(60))
    >>> new_state = new_state.next(home.appliance.light.event.show.ending_hue.Event(80))
    >>> new_state = new_state.next(home.appliance.light.event.show.cycles.Event(60))
    >>> new_state = new_state.next(home.appliance.light.event.show.period.Event(60))
    >>> new_state = new_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.Show)
    >>> command = SetWaveform.make([["172.31.10.245", 56700], ])
    >>> msgs = command.make_msgs_from(old_state, new_state)
    >>> "brightness: 80" in str(lifx_plugin.Description.make_from(msgs[0]))
    True
    """

    State = {
        "type": "lifx",
        "name": "SetWaveform",
        "fields": {
            "hue": 335,
            "saturation": 90,
            "brightness": 90,
            "kelvin": 3500,
            "duration": 1000,
            "transient": True,
            "period": 180000,
            "cycles": 30,
            "skew_ratio": 0.5,
            "waveform": "sine",
        },
        "addresses": [],
    }

    def make_msgs_from(
        self,
        old_state: Mixin,
        new_state: Mixin,
    ):
        result = []
        if new_state.is_showing:
            self.state.kelvin = new_state.temperature
            self.state.hue = new_state.ending_hue
            self.state.brightness = new_state.ending_brightness
            self.state.saturation = new_state.ending_saturation
            self.state.cycles = new_state.cycles
            self.state.period = new_state.period
            self.state.waveform = new_state.waveform.value.lower()
            self.state.duration = self.State["fields"]["duration"]
            self.state.transient = self.State["fields"]["transient"]
            self.state.skew_ratio = self.State["fields"]["skew_ratio"]
            result = self.execute()
        return result
