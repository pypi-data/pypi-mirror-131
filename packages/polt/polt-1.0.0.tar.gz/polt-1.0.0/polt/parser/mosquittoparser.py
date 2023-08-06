# system modules

# internal modules
from polt.parser.parser import Parser

# external modules


class MosquittoParser(Parser):
    """
    A simple parser that reads output of the `mosquitto_sub
    <https://mosquitto.org/man/mosquitto_sub-1.html>`_ MQTT cli client invoked
    with the ``-v`` flag.

    Example
    =======

    .. code-block:: sh

        mosquitto_sub -h your.mqtt-broker.org -t '#' -v
        # output like:
        # TOPIC                            VALUE UNIT
        # house/garden/sensor1/temperature 32.1  °C
        # house/cellar/sensor2/humidity    41    %
        # ...

        # feed this into polt like this:
        mosquitto_sub -h your.mqtt-broker.org -t '#' -v \
            | polt add-source -p mosquitto live
    """

    @property
    def data(self):
        for line in self.f:
            topic, message = (
                line.decode(errors="ignore")
                if hasattr(line, "decode")
                else line
            ).split(maxsplit=1)
            message = message.strip()
            topicsplit = topic.split("/")
            key, quantity = "/".join(topicsplit[:-1]), topicsplit[-1]
            try:
                value, unit = message.split(maxsplit=1)
            except (ValueError, TypeError):
                unit = None
                value = message
            try:
                yield {(quantity, unit, key): float(value)}
            except ValueError:
                continue
