import home
from typing import NewType, Sequence, TypeVar, Tuple

Address = NewType("Address", Sequence[Tuple[str, int]])


Mixin = TypeVar(
    "Mixin",
    home.appliance.light.indoor.hue.state.on.State,
    home.appliance.light.indoor.hue.state.off.State,
    home.appliance.light.indoor.hue.state.forced.on.State,
    home.appliance.light.indoor.hue.state.forced.circadian_rhythm.State,
    home.appliance.light.indoor.hue.state.forced.lux_balance.State,
    home.appliance.light.indoor.hue.state.forced.show.State,
)


from lifx_plugin.client import Client
from lifx_plugin.gateway import Gateway
from lifx_plugin.message import Command, Trigger, Description
from lifx_plugin import command, trigger
