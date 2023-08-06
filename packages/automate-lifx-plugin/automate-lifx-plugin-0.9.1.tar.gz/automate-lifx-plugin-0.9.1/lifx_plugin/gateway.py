import asyncio
import logging

from typing import List, Type, Callable

import home
import lifx
from lifx_plugin import Client
from lifx_plugin.message import Description, Trigger


class Gateway(home.protocol.Gateway):
    """
    >>> import asyncio
    >>> import lifx_plugin

    >>> loop = asyncio.get_event_loop()

    >>> description = {"type": "lifx",
    ...                 "name": "SetColor",
    ...                 "fields": {},
    ...                 "addresses": [["127.0.0.1", 56701]]}
    >>> command = lifx_plugin.Command(description)
    >>> trigger = lifx_plugin.Trigger(description)
    >>> gateway = Gateway(lifx_plugin.Client, "127.0.0.1", 56700)
    >>> gateway.associate_commands([command])
    >>> gateway.associate_triggers([trigger])
    >>> async def a_task(msgs):
    ...     print(msgs)
    ...     loop.stop()
    >>> t = loop.create_task(gateway.run([a_task]))

    >>> description = {"type": "lifx",
    ...                 "name": "State",
    ...                 "fields": {},
    ...                 "addresses": [["127.0.0.1", 56700]]}
    >>> command = lifx_plugin.Command(description)
    >>> lifx_lamp = Gateway(lifx_plugin.Client, "127.0.0.1", 56701)
    >>> lifx_lamp.associate_commands([command])
    >>> t = loop.create_task(lifx_lamp.run([]))
    >>> msgs = command.execute()
    >>> t = loop.create_task(lifx_lamp.writer(msgs))
    >>> loop.run_forever()
    Trigger State {power: 0, hue: 0, saturation: 0, brightness: 0, kelvin: 0, rgb: (0, 0, 0), label: } from [127.0.0.1:56701]
    """

    PROTOCOL = Description.PROTOCOL

    def __init__(
        self, client: Type[Client], address: str = "0.0.0.0", port: int = 56700
    ):
        self._transport = None
        self._protocol = None
        self._client = client
        self._address = address
        self._port = port
        self._triggers = set()
        self._commands = set()
        self._loop = asyncio.get_event_loop()

        self.logger = logging.getLogger(__name__)

    async def disconnect(self):
        if self._transport:
            self._transport.close()

    def associate_commands(self, descriptions: List[Description]):
        for command in descriptions:
            for address in command.addresses:
                self._commands.add((address[0], address[1]))

    def associate_triggers(self, descriptions: List[Description]):
        for trigger in descriptions:
            for address in trigger.addresses:
                self._triggers.add((address[0], address[1]))

    async def run(self, other_tasks: List[Callable]):
        while True:
            on_con_lost = self._loop.create_future()
            try:
                self._transport, self._protocol = await self._loop.create_datagram_endpoint(
                    lambda: self._client(on_con_lost,
                        self._wrap_tasks(other_tasks), self._triggers, self._commands
                    ),
                    local_addr=(self._address, self._port),
                )
                try:
                    await on_con_lost
                finally:
                    self._transport.close()
            except (TimeoutError, OSError) as e:
                self.logger.fatal(e)
                await asyncio.sleep(60)

    async def writer(self, msgs: List[lifx.lan.Msg], *args):
        while not self._protocol:
            await asyncio.sleep(0.1)
        for msg in msgs:
            if isinstance(msg, lifx.lan.Msg) and self._transport:
                data = bytes(msg)
                try:
                    self._transport.sendto(data, (msg.addr, msg.port))
                    self.logger.info("written {}".format(msg))
                except ConnectionRefusedError as e:
                    self.logger.error(str(e))
                except OSError as e:
                    self.logger.error(str(e))
                await asyncio.sleep(3)

    @staticmethod
    def make_trigger(msg: lifx.lan.Msg):
        trigger = Trigger.make_from(msg)
        return trigger
