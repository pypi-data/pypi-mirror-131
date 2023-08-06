import asyncio
import logging

import lifx


class Client(asyncio.DatagramProtocol):
    def __init__(self, on_con_lost, tasks, triggers, commands):
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._tasks = set(tasks)
        self._listening_addresses = triggers
        self._writing_addresses = commands
        self._on_con_lost = on_con_lost

        self.logger = logging.getLogger(__name__)

    @property
    def addresses(self):
        return self._listening_addresses.union(self._writing_addresses)

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._on_con_lost.set_result(True)
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        if addr in self._listening_addresses:
            msg = lifx.lan.Msg.from_bytes(data, addr=addr[0], port=addr[1])
            self.logger.info("read    {}".format(str(msg)))
            header, body = msg.decode()
            if header.type != lifx.lan.Header.State.acknowledgement:
                for task in self._tasks:
                    self._loop.create_task(task(msg))
        else:
            self.logger.debug(
                "read    {} not processed for address {}".format(data, addr)
            )


class ClientExample(Client):
    @asyncio.coroutine
    def send_cmds_to(self, addr, protocol):
        header = lifx.lan.Header()
        header.type = lifx.lan.Header.State.set_color_light
        header.field.tagged = 1
        header.field.addressable = 1
        header.field.res_required = 1
        # header.field.source = 1234
        body = lifx.lan.light.SetColor()
        body.field.color.rgb = (0, 255, 0)
        body.field.color.kelvin = 3500
        body.field.duration = 1024
        # header.field.sequence = 3
        msg = lifx.lan.Msg.encode(header, body, addr=addr, port=56700)
        yield from protocol.send_msg(msg)
        yield from asyncio.sleep(1)
        body.field.color.rgb = (0, 0, 255)
        header.field.sequence = 4
        msg = lifx.lan.Msg.encode(header, body, addr=addr, port=56700)
        yield from protocol.send_msg(msg)
        yield from asyncio.sleep(1)
        body.field.color.rgb = (255, 0, 0)
        header.field.sequence = 5
        msg = lifx.lan.Msg.encode(header, body, addr=addr, port=56700)
        yield from protocol.send_msg(msg)


@asyncio.coroutine
def create_datagram_endpoint():
    transport, protocol = yield from loop.create_datagram_endpoint(
        lambda: ClientExample(
            [], [("172.31.10.245", 56700)], [("172.31.10.245", 56700)]
        ),
        local_addr=("0.0.0.0", 56700),
    )
    return transport, protocol


if __name__ == "__main__":
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    loop = asyncio.get_event_loop()
    transport, protocol = loop.run_until_complete(
        loop.create_task(create_datagram_endpoint())
    )
    loop.run_until_complete(loop.create_task(protocol.send_cmds_to("172.31.10.245")))
