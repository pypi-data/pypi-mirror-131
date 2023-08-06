#!/usr/bin/env python3

import sys
import asyncio
import logging.config
import socket
import time

import home
import graphite_feeder


sys.path.append("..")


class OnRedisMsg(home.builder.listener.OnRedisMsg):
    def __init__(self, home_resources, graphite_host, graphite_port):
        self._home_resources = home_resources
        self._graphite_host = graphite_host
        self._graphite_port = graphite_port
        self._logger = logging.getLogger(__name__)

    def send_to_graphite(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        try:
            sock.connect((self._graphite_host, int(self._graphite_port)))
        except Exception as e:
            self._logger.critical(e)
            raise e
        sock.sendall(data.encode("ascii"))
        sock.send(b"\n")
        sock.close()
        self._logger.info("{} to graphite".format(data))

    async def on_appliance_updated(self, new_appliance):
        appliance_handler = None
        event_handler = None

        now = time.time()
        appliance = self._home_resources.appliances.find(new_appliance.name)
        old_state, new_state = appliance.update(new_appliance)
        try:
            appliance_handler = graphite_feeder.handler.appliance.registry.mapper[
                appliance.__class__
            ]
            appliance_handler = appliance_handler(self._home_resources, appliance)
        except KeyError:
            self._logger.warning("appliance {} not mapped".format(appliance))

        for event in new_state - old_state:
            try:
                event_handler = graphite_feeder.handler.event.registry.mapper[
                    event.__class__
                ]
                event_handler = event_handler(self._home_resources, event)
            except KeyError:
                self._logger.warning("event {} not mapped".format(event))

            if appliance_handler and event_handler:
                data = "{}.{} {} {}".format(
                    appliance_handler.target_name,
                    event_handler.metric,
                    event_handler.get_datapoint(),
                    int(now),
                )
                await asyncio.get_event_loop().run_in_executor(
                    None, self.send_to_graphite, data
                )

        if appliance_handler and appliance_handler.get_datapoint() is not None:
            data = "{}.{} {} {}".format(
                appliance_handler.target_name,
                appliance_handler.metric,
                appliance_handler.get_datapoint(),
                int(now),
            )
            await asyncio.get_event_loop().run_in_executor(
                None, self.send_to_graphite, data
            )

    async def on_performer_updated(self, performer, old_state, new_state):
        self._logger.debug("{} {}".format(old_state, new_state))
        performer.execute(old_state, new_state)


if __name__ == "__main__":
    (options, _) = home.options.parser().parse_args()
    if options.configuration_file:
        options = home.configs.parse(vars(options), options.configuration_file)

    if options.knx_usbhid or options.knxnet_ip:
        import knx_plugin
    if options.lifx:
        import lifx_plugin
    if options.sonos:
        import soco_plugin
    if options.somfy_sdn:
        import somfy_sdn_plugin
    if options.home_assistant:
        import home_assistant_plugin

    configuration = graphite_feeder.conf.default_logging_configuration(
        options.logging_dir, logging_level=options.graphite_feeder_logging_level
    )
    logging.config.dictConfig(configuration)

    loop = asyncio.get_event_loop()
    resources = home.builder.listener.Resources(
        options.project_dir,
        options.redis_host,
        options.redis_port,
        options.graphite_feeder_node_name,
        options.graphite_feeder_other_nodes_names,
    )

    on_redis_msg = OnRedisMsg(
        resources,
        options.graphite_feeder_server_host,
        options.graphite_feeder_data_port,
    )
    loop.run_until_complete(resources.redis_gateway.connect())
    resources.redis_gateway.create_tasks(
        loop, on_redis_msg.on_appliance_updated, on_redis_msg.on_performer_updated
    )
    loop.run_forever()
