r"""
This module implements the core RPC and publish APIs. Developers can extend
LinkProtocol to provide additional RPC callbacks for their web-applications. Then extend
ServerProtocol to hook all the needed LinkProtocols together.
"""

import logging
from typing import Any, Callable, Dict, Hashable, List, Optional

from . import register as exportRpc
from . import schedule_callback
from . import wslinktypes

# =============================================================================
#
# Base class for objects that can accept RPC calls or publish over wslink
#
# =============================================================================


class LinkProtocol(wslinktypes.LinkProtocol):
    """
    Subclass this to communicate with wslink clients. LinkProtocol
    objects provide rpc and pub/sub actions.
    """

    def __init__(self) -> None:
        # need a no-op in case they are called before connect.
        self.publish: wslinktypes.PublishCallback = lambda x, y: None
        self.addAttachment = lambda x: None
        self.stopServer = lambda: None
        self.coreServer: Optional["ServerProtocol"] = None

    def init(self, publish: wslinktypes.PublishCallback, addAttachment, stopServer: Callable[[], None]) -> None:
        self.publish = publish
        self.addAttachment = addAttachment
        self.stopServer = stopServer

    def getSharedObject(self, key):
        if self.coreServer:
            return self.coreServer.getSharedObject(key)
        return None


# =============================================================================
#
# Base class for wslink ServerProtocol objects
#
# =============================================================================


class ServerProtocol(wslinktypes.ServerProtocol):
    """
    Defines the core server protocol for wslink. Gathers a list of LinkProtocol
    objects that provide rpc and publish functionality.
    """

    def __init__(self):
        self.linkProtocols: List[wslinktypes.LinkProtocol] = []
        self.secret: Optional[str] = None
        self.publish: wslinktypes.PublishCallback = lambda x, y: None
        self.initialize()

    def init(self, publish: wslinktypes.PublishCallback, addAttachment, stopServer) -> None:
        self.publish = publish
        self.addAttachment = addAttachment
        self.stopServer = stopServer

    def initialize(self) -> None:
        """
        Let sub classes define what they need to do to properly initialize
        themselves.
        """
        pass

    def setSharedObject(self, key: Hashable, shared: Optional[Any]) -> None:
        if not hasattr(self, "sharedObjects"):
            self.sharedObjects: Dict[Hashable, Any] = {}
        if shared == None and key in self.sharedObjects:
            del self.sharedObjects[key]
        else:
            self.sharedObjects[key] = shared

    def getSharedObject(self, key: Hashable) -> Any:
        if key in self.sharedObjects:
            return self.sharedObjects[key]
        else:
            return None

    def registerLinkProtocol(self, protocol: wslinktypes.LinkProtocol) -> None:
        assert isinstance(protocol, LinkProtocol), protocol
        protocol.coreServer = self
        self.linkProtocols.append(protocol)

    # Note: this can only be used _before_ a connection is made -
    # otherwise the WslinkWebSocketServerProtocol will already have stored references to
    # the RPC methods in the protocol.
    def unregisterLinkProtocol(self, protocol: wslinktypes.LinkProtocol) -> None:
        assert isinstance(protocol, LinkProtocol), protocol
        protocol.coreServer = None
        try:
            self.linkProtocols.remove(protocol)
        except ValueError as e:
            logging.error("Link protocol missing from registered list.")

    def getLinkProtocols(self) -> List[wslinktypes.LinkProtocol]:
        return self.linkProtocols

    def updateSecret(self, newSecret: str) -> None:
        self.secret = newSecret

    @exportRpc("application.exit")
    def exit(self) -> None:
        """RPC callback to exit"""
        self.stopServer()

    @exportRpc("application.exit.later")
    def exitLater(self, secondsLater: float=60) -> None:
        """RPC callback to exit after a short delay"""
        print(f"schedule exit for {secondsLater} seconds from now")
        schedule_callback(secondsLater, self.stopServer)
