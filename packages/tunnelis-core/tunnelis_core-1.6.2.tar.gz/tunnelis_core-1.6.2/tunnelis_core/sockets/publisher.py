from typing import Tuple
from zmq import PUB as ZMQ_PUB
from zmq.sugar.context import Context


class Publisher:
    """
    A generic message publisher.

    A wrapper class around ZMQ sockets of type ZMQ_PUB.

    """

    def __init__(self):
        """
        Initialize a message publisher.

        """
        self.__zmq_context = Context()

        # Connect publisher to message broker
        self.__socket = self.__zmq_context.socket(ZMQ_PUB)

    def connect(self, broker: Tuple[str, int]) -> None:
        """
        Connect publisher to an external message broker.

        Parameters
        ----------
        broker : Tuple(str, int)
            The TCP network address (host, port) of the message broker.
        """

        broker_host, broker_port = broker
        self.__socket.connect(f'tcp://{broker_host}:{broker_port}')

    def bind(self, address: Tuple[str, int]) -> None:
        """
        Bind publisher to an address.

        Parameters
        ----------
        address : Tuple(str, int)
            The TCP network address (host, port) for this publisher.
        """

        host, port = address
        self.__socket.connect(f'tcp://{host}:{port}')

    def publish(self, topic: bytes, message: bytes) -> None:
        """
        Publish a message.

        Parameters
        ----------
        topic : bytes
            The topic on which to publish the message.

        message : bytes
            The message to be published.

        """
        self.__socket.send_multipart([topic, message])

    def close(self) -> None:
        """
        Stops publisher.

        """
        self.__socket.close()
        self.__zmq_context.term()
