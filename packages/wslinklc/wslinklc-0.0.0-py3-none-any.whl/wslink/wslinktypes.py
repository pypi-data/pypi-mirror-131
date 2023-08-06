from typing import Any, Callable, Dict, List, Optional, Protocol, TypedDict

# To publish a message: (topic, data) -> None
PublishCallback = Callable[[str, bytes], None]

# TODO: Autobahn HTTP request type.
HTTPRequest = Any

class LinkProtocol(Protocol):
    #def publish(topic: str, data: bytes) -> None: ...

    def init(self, publish: PublishCallback, addAttachment, stopServer: Callable[[], None]) -> None:
        ...

    def onConnect(self, request: HTTPRequest, client_id: str) -> None:
        ...

    def onClose(self, client_id: str) -> None:
        ...

class ServerProtocol(Protocol):
    #def publish(topic: str, data: bytes) -> None: ...

    def initialize(self) -> None:
        ...

    def updateSecret(self, newSecret: str) -> None:
        ...

    def onConnect(self, request: HTTPRequest, client_id: str) -> None:
        ...

    def onClose(self, client_id: str) -> None:
        ...

    def registerLinkProtocol(self, protocol: LinkProtocol) -> None:
        ...

    def unregisterLinkProtocol(self, protocol: LinkProtocol) -> None:
        ...

    def getLinkProtocols(self) -> List[LinkProtocol]:
        ...

class ServerConfig(TypedDict, total=False):
    # The network interface to bind to. If None,
    # bind to all interfaces.
    host: Optional[str]
    # HTTP port to listen to.
    port: int
    # Idle shutdown timeout, in seconds.
    timeout: float
    ws: Dict[str, ServerProtocol]
    static: Dict[str, str]
    logging_level: Optional[int]
    handle_signals: bool
