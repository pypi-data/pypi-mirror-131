"""Websocket client section for the Slurry stream processing microframework."""
__version__ = '0.4.2'

from trio_websocket import ConnectionClosed, ConnectionTimeout, HandshakeError, DisconnectionTimeout

from .websocket import Websocket
