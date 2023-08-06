from typing import Any, Callable, Tuple
from zmq import ROUTER as ZMQ_ROUTER
from zmq.auth import load_certificate
from zmq.eventloop.zmqstream import ZMQStream
from zmq.sugar.context import Context


TCPMessageCallback = Callable[[Any, bytes, bytes], None]


class Server:
    """
    A configurable TCP server.

    A wrapper around ZMQ sockets of type ZMQ_ROUTER.

    """

    __message_handler: TCPMessageCallback = None

    def __init__(
        self,
        secure: bool = False,
        private_key: str = 'server.key_secret'
    ):
        """
        Initializes server socket.

        Parameters
        ----------
        secure : boolean
            Whether or not to secure communications.
            Communications are always secured using CURVE.

        private_key : str
            The complete path for this server's private key.
            Only relevant when using secured communications.

        """

        self.__zmq_context = Context()

        self.__socket = self.__zmq_context.socket(ZMQ_ROUTER)

        if secure:

            # Create endpoint for clients to communicate with server
            server_public, server_secret = load_certificate(private_key)

            self.__socket.curve_secretkey = server_secret
            self.__socket.curve_publickey = server_public
            self.__socket.curve_server = True

        self.stream = ZMQStream(self.__socket)
        self.stream.on_recv(self.__message_handler)

    def bind(self, port: int) -> None:
        """
        Bind socket to a TCP address and start listening for communications.

        Parameters
        ----------
        port : int
            The network port at which to bind the socket.
            When set to a non-positive integer the socket will bind to a random free port.

        """

        if port > 0:
            self.__socket.bind(f'tcp://*:{port}')
            self.port = port
        else:
            self.port = self.__socket.bind_to_random_port('tcp://*', min_port=30000)

    def send(self, identity: bytes, message: bytes) -> None:
        """
        Send raw application data to a remote client.

        Parameters
        ----------
        identity : bytes
            The identity (ZMQ_IDENTITY) of the remote client.

        message : bytes
            The TCP message to be sent.

        """
        self.stream.send_multipart([identity, message])

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
        handler : Callable(Server, bytes, bytes) -> None
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

        identity, payload = message

        if self.__message_handler:
            self.__message_handler(self, identity, payload)
