from .messages_pb2 import (
    AuthenticationRequestMessage,
    AuthenticationResponseMessage,
    OpenTunnelRequestMessage,
    OpenTunnelResponseMessage,
    PingMessage,
    PongMessage,
    RawRequestMessage,
    RawResponseMessage,
    MessageType,
    TunnelisMessage
)
from time import time as now


def build_authentication_http_request_message(user, domain, authtoken):
    """ Builds messages of type MSG_AUTHENTICATION_REQUEST for HTTP/HTTPS tunnels.
    """

    message = AuthenticationRequestMessage()
    message.user = user
    message.domain = domain
    message.authtoken = authtoken
    message.protocol = 'HTTP'

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_AUTHENTICATION_REQUEST
    tunnelis_message.authentication_request.CopyFrom(message)

    return tunnelis_message


def build_authentication_tcp_request_message(user, domain, authtoken):
    """ Builds messages of type MSG_AUTHENTICATION_REQUEST for TCP tunnels.
    """

    message = AuthenticationRequestMessage()
    message.user = user
    message.domain = domain
    message.authtoken = authtoken
    message.protocol = 'TCP'

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_AUTHENTICATION_REQUEST
    tunnelis_message.authentication_request.CopyFrom(message)

    return tunnelis_message


def build_authentication_ws_request_message(user, domain, authtoken):
    """ Builds messages of type MSG_AUTHENTICATION_REQUEST for WS tunnels.
    """

    message = AuthenticationRequestMessage()
    message.user = user
    message.domain = domain
    message.authtoken = authtoken
    message.protocol = 'WS'

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_AUTHENTICATION_REQUEST
    tunnelis_message.authentication_request.CopyFrom(message)

    return tunnelis_message


def build_authentication_success_response_message(session_token):
    """ Builds messages of type MSG_AUTHENTICATION_RESPONSE.
    For cases when client authentication succeeds.
    """

    message = AuthenticationResponseMessage()
    message.session_token = session_token
    message.reason = ''
    message.success = True

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_AUTHENTICATION_RESPONSE
    tunnelis_message.authentication_response.CopyFrom(message)

    return tunnelis_message


def build_authentication_failure_response_message(reason):
    """ Builds messages of type MSG_AUTHENTICATION_RESPONSE.
    For cases when client authentication fails.
    """

    message = AuthenticationResponseMessage()
    message.session_token = ''
    message.reason = reason
    message.success = False

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_AUTHENTICATION_RESPONSE
    tunnelis_message.authentication_response.CopyFrom(message)

    return tunnelis_message


def build_open_tunnel_request(session_token):
    """
    Generic function to build messages of type MSG_OPEN_TUNNEL_REQUEST.
    """

    message = OpenTunnelRequestMessage()
    message.session_token = session_token

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_OPEN_TUNNEL_REQUEST
    tunnelis_message.open_tunnel_request.CopyFrom(message)

    return tunnelis_message


def build_open_tunnel_success_response_message(url):
    """ Builds messages of type MSG_OPEN_TUNNEL_RESPONSE.
    For cases when tunnel openning succeeds.
    """

    message = OpenTunnelResponseMessage()
    message.url = url
    message.reason = ''
    message.success = True

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_OPEN_TUNNEL_RESPONSE
    tunnelis_message.open_tunnel_response.CopyFrom(message)

    return tunnelis_message


def build_open_tunnel_failure_response_message(reason):
    """ Builds messages of type MSG_OPEN_TUNNEL_RESPONSE.
    For cases when tunnel openning fails.
    """

    message = OpenTunnelResponseMessage()
    message.url = ''
    message.reason = reason
    message.success = False

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_OPEN_TUNNEL_RESPONSE
    tunnelis_message.open_tunnel_response.CopyFrom(message)

    return tunnelis_message


def build_ping_message():
    """ Builds messages of type MSG_PING.
    """

    message = PingMessage()

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_PING
    tunnelis_message.ping_message.CopyFrom(message)

    return tunnelis_message


def build_pong_message(session_token):
    """ Builds messages of type MSG_PONG.
    """

    message = PongMessage()
    message.session_token = session_token
    message.timestamp = now()

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_PONG
    tunnelis_message.pong_message.CopyFrom(message)

    return tunnelis_message


def build_raw_request_message(source_id, payload):
    """ Builds messages of type MSG_RAW_REQUEST.
    """

    message = RawRequestMessage()
    message.source_id = source_id
    message.payload = payload

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_RAW_REQUEST
    tunnelis_message.raw_request.CopyFrom(message)

    return tunnelis_message


def build_raw_response_message(session_token, destination_id, payload):
    """ Builds messages of type MSG_RAW_RESPONSE.
    """

    message = RawResponseMessage()
    message.session_token = session_token
    message.destination_id = destination_id
    message.payload = payload

    tunnelis_message = TunnelisMessage()
    tunnelis_message.type = MessageType.MSG_RAW_RESPONSE
    tunnelis_message.raw_response.CopyFrom(message)

    return tunnelis_message
