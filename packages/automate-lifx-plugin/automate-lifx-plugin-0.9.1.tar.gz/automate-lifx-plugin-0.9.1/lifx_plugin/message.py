import copy
import logging
import functools

from typing import List

import home
import lifx

from lifx_plugin import Address


class Description(home.protocol.Description):
    """
    A Lifx LAN protocol message description.

    The description contains those *fields of interest* for a *Trigger* or a *Command* definition.

    >>> definition = {"type": "lifx",
    ...                "name": "SetColor",
    ...                "fields": {"hue": 1, "saturation": 1, "brightness": 1, "kelvin": 3500, "duration": 1000},
    ...                "addresses": [["172.31.10.245", 56700]]}
    >>> description = Description(definition)
    >>> print(description)
    SetColor {hue: 1, saturation: 1, brightness: 1, kelvin: 3500, rgb: (3, 3, 3), duration: 1000}: [172.31.10.245:56700]

    >>> definition = {"name": "SetWaveform",
    ...                "fields": {"hue": 1, "saturation": 90, "brightness": 90, "kelvin": 3500, "duration": 1000,
    ...                           "transient": True, "period": 180000, "cycles": 30, "skew_ratio": 0.5, "waveform": "sine"},
    ...                "addresses": [["172.31.10.245", 56700]]}
    >>> description = Description(definition)
    >>> another_definition = {"name": "SetWaveform",
    ...                "fields": {"hue": 2, "saturation": 20, "brightness": 20, "kelvin": 2500, "duration": 2000,
    ...                           "transient": True, "period": 80, "cycles": 20, "skew_ratio": 0.5, "waveform": "sine"},
    ...                "addresses": [["172.31.10.245", 56700]]}
    >>> another_description = Description(another_definition)
    >>> print(description)
    SetWaveform {hue: 1, saturation: 90, brightness: 90, kelvin: 3500, rgb: (230, 26, 23), transient: 1, period: 180000, cycles: 30.0, skew_ratio 32768, waveform 1}: [172.31.10.245:56700]

    >>> description == another_description
    True

    >>> d = Description.make_from(lifx.lan.Msg.from_bytes([0x31, 0x00, 0x00, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66, 0x00, 0x00, 0x00, 0x00, 0x39, 0x0E, 0x33, 0x33, 0x33, 0x33, 0xAC, 0x0D, 0x00, 0x04, 0x00, 0x00]))
    >>> "SetColor" in str(d)
    True

    >>> Description.State["name"] = "SetColor"
    >>> d = Description.make([["172.31.10.245", 56700]])
    >>> "SetColor" in str(d)
    True
    """

    PROTOCOL = "lifx"

    State = {"name": "Fake", "fields": {}, "addresses": []}

    def __init__(self, data: dict):
        super(Description, self).__init__(data)
        factory = lifx.lan.light.State_Factory()
        fields = data["fields"] if "fields" in data else {}
        self._state = factory.make(data["name"], fields)
        self._state_class = self._state.__class__
        self._addresses = [address for address in data["addresses"]]
        self._label = str(self._state)

        self._logger = logging.getLogger(__name__)

    def __eq__(self, other):
        if self.PROTOCOL == other.PROTOCOL:
            try:
                if self.state.__class__ == other.state.__class__ and [
                    (address, port) for address, port in self.addresses
                ] == [(address, port) for address, port in other.addresses]:
                    return True
            except TypeError as e:
                self._logger.error(e)
        return False

    def __hash__(self):
        return hash("{}{}".format(self.state.__class__.__name__, self._addresses))

    @property
    def state(self) -> home.appliance.State:
        return self._state

    @property
    def addresses(self) -> List[Address]:
        return self._addresses

    @classmethod
    def make(cls, addresses: List[Address]) -> "lifx_plugin.Description":
        description = copy.deepcopy(cls.State)
        description["addresses"] = addresses
        return cls(description)

    @classmethod
    def make_from_yaml(cls, addresses: List[Address]) -> "lifx_plugin.Description":
        return cls.make(addresses)

    @classmethod
    def make_from(cls, msg: lifx.lan.Msg) -> "lifx_plugin.Description":
        header, body = msg.decode()
        dpt_description = lifx.lan.light.Description_Factory.make(body)
        description = {
            "name": dpt_description[0],
            "addresses": [[msg.addr, msg.port]],
            "fields": dpt_description[1],
        }
        d = cls(description)
        return d

    def __str__(self, *args, **kwargs):
        addresses = functools.reduce(
            lambda old_addresses, new_address: "{}, {}".format(
                old_addresses, new_address
            ),
            ["{}:{}".format(address[0], address[1]) for address in self._addresses]
            if len(self._addresses)
            else ["no address"],
        )
        s = "{}: [{}]".format(self.state, addresses)
        return s


class Trigger(home.protocol.Trigger, Description):
    """
    >>> import io
    >>> import json
    >>> json_trigger = '''
    ...                {
    ...                    "name": "SetColor",
    ...                    "fields": {"hue": 20, "saturation": 20, "brightness": 20, "kelvin": 3500, "duration": 1024},
    ...                    "addresses": [["172.31.10.245", 56700]]
    ...                }
    ... '''
    >>> another_trigger = '''
    ...                {
    ...                    "name": "SetColor",
    ...                    "fields": {"hue": 20, "saturation": 20, "brightness": 20, "kelvin": 3500, "duration": 1024},
    ...                    "addresses": [["172.31.10.166", 56700]]
    ...                }
    ... '''
    >>> match_trigger = '''
    ...                {
    ...                    "name": "SetColor",
    ...                    "fields": {"hue": 40, "saturation": 50, "brightness": 60, "kelvin": 3500, "duration": 1024},
    ...                    "addresses": [["172.31.10.245", 56700]]
    ...                }
    ... '''
    >>> fd = io.StringIO(json_trigger)
    >>> trigger_data = json.load(fd)
    >>> trigger = Trigger(trigger_data)
    >>> trigger.state.hue
    20
    >>> trigger.state.saturation
    20
    >>> trigger.state.brightness
    20
    >>> fd = io.StringIO(another_trigger)
    >>> another_trigger_data = json.load(fd)
    >>> another_trigger = Trigger(another_trigger_data)
    >>> trigger.is_triggered(another_trigger)
    False
    >>> fd = io.StringIO(match_trigger)
    >>> match_trigger_data = json.load(fd)
    >>> match_trigger = Trigger(match_trigger_data)
    >>> trigger.is_triggered(match_trigger)
    True
    >>> print(match_trigger)
    Trigger SetColor {hue: 40, saturation: 50, brightness: 60, kelvin: 3500, rgb: (154, 128, 77), duration: 1024} from [172.31.10.245:56700]

    >>> Trigger.State["name"] = "SetColor"
    >>> d = Trigger.make([["172.31.10.245", 56700]], [1, 2, 3])
    >>> print(d)
    Trigger SetColor {hue: 0, saturation: 0, brightness: 0, kelvin: 0, rgb: (0, 0, 0), duration: 0} from [172.31.10.245:56700]
    >>> d.events
    [1, 2, 3]
    """

    def is_triggered(self, another_description: Description) -> bool:
        if super(Trigger, self).is_triggered(another_description):
            try:
                if set(
                    [(addr, port) for addr, port in another_description.addresses]
                ).intersection(set([(addr, port) for addr, port in self.addresses])):
                    self._logger.info("triggered {}".format(another_description))
                    return True
                else:
                    return False
            except TypeError as e:
                self._logger.error(
                    "err: %s from list %s and %s",
                    e,
                    another_description.addresses,
                    self.addresses,
                )

    @classmethod
    def make(
        cls, addresses: List[Address], events: List[home.Event] = None
    ) -> "lifx_plugin.Trigger":
        description = copy.deepcopy(cls.State)
        description["addresses"] = addresses
        return cls(description, events)

    @classmethod
    def make_from_yaml(
        cls, addresses: List[Address], events: List[home.Event] = None
    ) -> "lifx_plugin.Trigger":
        return cls.make(addresses, events)

    def __str__(self, *args, **kwargs):
        addresses = functools.reduce(
            lambda old_addresses, new_address: "{}, {}".format(
                old_addresses, new_address
            ),
            ["{}:{}".format(address[0], address[1]) for address in self._addresses]
            if len(self._addresses)
            else ["no address"],
        )
        s = "Trigger {} from [{}]".format(self.state, addresses)
        return s


class Command(Description, home.protocol.Command):
    """
    >>> import io
    >>> import json
    >>> import lifx
    >>> import home
    >>> command_data = '''
    ...                {
    ...                    "name": "SetColor",
    ...                    "fields": {"hue": 20, "saturation": 20, "brightness": 20, "kelvin": 3500, "duration": 1024},
    ...                    "addresses": [["172.31.10.245", 56700]]
    ...                }
    ... '''
    >>> fd = io.StringIO(command_data)
    >>> command_data = json.load(fd)
    >>> command = Command(command_data)
    >>> command.execute()
    [[0x31, 0x00, 0x00, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66, 0x00, 0x00, 0x00, 0x00, 0x39, 0x0E, 0x33, 0x33, 0x33, 0x33, 0xAC, 0x0D, 0x00, 0x04, 0x00, 0x00]]

    >>> print(command)
    Command SetColor {hue: 20, saturation: 20, brightness: 20, kelvin: 3500, rgb: (51, 44, 41), duration: 1024} to [172.31.10.245:56700]
    """

    def execute(self) -> List[lifx.lan.Msg]:
        req_msgs = []
        for address in self._addresses:
            msg = lifx.lan.Msg.encode(
                lifx.lan.header.make(self.state.state),
                self.state,
                addr=address[0],
                port=address[1],
            )
            if msg:
                req_msgs.append(msg)
        self._logger.info("execute {}".format(self.state))
        return req_msgs

    def make_msgs_from(
        self, old_state: home.appliance.State, new_state: home.appliance.State
    ) -> List[lifx.lan.Msg]:
        return []

    def __str__(self, *args, **kwargs):
        addresses = functools.reduce(
            lambda old_addresses, new_address: "{}, {}".format(
                old_addresses, new_address
            ),
            ["{}:{}".format(address[0], address[1]) for address in self._addresses]
            if len(self._addresses)
            else ["no address"],
        )
        s = "Command {} to [{}]".format(self.state, addresses)
        return s
