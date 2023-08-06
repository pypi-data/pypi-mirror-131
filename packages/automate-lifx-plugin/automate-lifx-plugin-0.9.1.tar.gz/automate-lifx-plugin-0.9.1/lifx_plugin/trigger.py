import home

from lifx_plugin import Mixin
from lifx_plugin.message import Trigger, Description


class Always(Trigger, home.protocol.Trigger):
    def __init__(self, *args, **kwargs):
        super(Always, self).__init__(*args, **kwargs)

    def is_triggered(self, another_description: Description):
        if super(Always, self).is_triggered(another_description):
            if self == another_description:
                self._logger.info("triggered {}".format(another_description))
                return True


class State(Always):
    """
    >>> import io
    >>> import json
    >>> import home
    >>> import lifx_plugin
    >>> bus_event = '''
    ...                {
    ...                    "name": "State",
    ...                    "fields": {"hue": 8, "saturation": 88, "brightness": 88, "kelvin": 8888, "duration": 88888},
    ...                    "addresses": [["172.31.10.245", 56700]]
    ...                }
    ... '''
    >>> fd = io.StringIO(bus_event)
    >>> description = lifx_plugin.Description(json.load(fd))
    >>> trigger = lifx_plugin.trigger.State.make([["172.31.10.245", 56700]], [home.appliance.light.event.forced.Event.On])
    >>> trigger.is_triggered(description)
    True
    >>> old_state = home.appliance.light.indoor.hue.state.on.State()
    >>> state = trigger.make_new_state_from(description, old_state)
    >>> "8" in str(state)
    True
    >>> "88" in str(state)
    True
    >>> "8888" in str(state)
    True
    """

    State = {"type": "lifx", "name": "State", "addresses": [], "fields": {}}

    def make_new_state_from(
        self, another_description: Description, old_state: Mixin
    ) -> home.appliance.State:
        new_state = super(State, self).make_new_state_from(
            another_description, old_state
        )
        new_state.hue = another_description.state.hue
        new_state.brightness = another_description.state.brightness
        new_state.saturation = another_description.state.saturation
        new_state.temperature = another_description.state.kelvin

        return new_state
