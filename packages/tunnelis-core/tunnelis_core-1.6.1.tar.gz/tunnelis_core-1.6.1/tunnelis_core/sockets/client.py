from typing import Any, Callable, Tuple
from zmq import DEALER as ZMQ_DEALER
from zmq.auth import load_certificate
from zmq.eventloop.zmqstream import ZMQStream
from zmq.sugar.context import Context


TCPMessageCallback = Callable[[Any, bytes], None]


class Client:
    """
    A configurable TCP client.

    A wrapper around ZMQ sockets of type ZMQ_DEALER.

    """

    __message_handler: TCPMessageCallback = None

    def __init__(
        self,
        secure: bool = False,
        client_private_key: str = 'client.key_secret',
        server_public_key: str = 'server.key'
    ):
        """
        Initializes client socket.

        Parameters
        ----------
        server_address : Tuple(str, int)
            The network address (host, port) of the server to connect to.

        secure : boolean
            Whether or not to secure communications.
            Communications are always secured using CURVE.

        client_private_key : str
            The complete path for this client's private key.
            Only relevant when using secured communications.

        server_public_key : str
            The complete path for the server's public key.
            Only relevant when using secured communications.

        """

        self.__zmq_context = Context()

        self.__socket = self.__zmq_context.socket(ZMQ_DEALER)

        if secure:

            server_public, _ = load_certificate(server_public_key)
            client_public, client_secret = load_certificate(client_private_key)

            self.__socket.curve_secretkey = client_secret
            self.__socket.curve_publickey = client_public
            self.__socket.curve_serverkey = server_public

        self.stream = ZMQStream(self.__socket)
        self.stream.on_recv(self.__message_handler)

    def connect(self, address: Tuple[str, int]) -> None:
        """
        Connect to a TCP address.

        Parameters
        ----------
        address : Tuple(str, int)
            The TCP network address to which to connect to.

        """
        host, port = address
        self.__socket.connect(f'tcp://{host}:{port}')

    def send(self, message: bytes) -> None:
        """
        Send raw application data to a remote client.

        Parameters
        ----------
        message : bytes
            The TCP message to be sent.

        """
        self.stream.send_multipart([message])

    def close(self) -> None:
        """
        Close endpoint.

        """
        self.stream.close()
        self.__socket.close()
        self.__zmq_context.term()

    def set_message_handler(self, handler: TCPMessageCallback) -> None:
        """
        Set the callback function to handle incoming TCP messages.

        Parameters
        ----------
        handler : Callable(Client, bytes) -> None
            The callback function.

        """
        self.__message_handler = handler

    def unset_message_handler(self) -> None:
        """
        Stop handling incoming TCP messages.

        """
        self.__message_handler = None

    def __message_handler(self, message: Tuple[bytes, bytes]) -> None:
        """
        A generic message handler.
        Forwards received messages to their proper message handlers.

        Parameters
        ----------
        message : Tuple(bytes, bytes)
            The received message.

        """

        if self.__message_handler:
            self.__message_handler(self, message[0])
