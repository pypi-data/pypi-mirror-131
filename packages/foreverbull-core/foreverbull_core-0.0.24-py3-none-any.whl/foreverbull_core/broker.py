from foreverbull_core.http import HTTPClient
from foreverbull_core.models.socket import SocketConfig
from foreverbull_core.socket.client import SocketClient


class Broker:
    def __init__(self, broker_host: str, local_host: str) -> None:
        self._broker_host = broker_host
        self._local_host = local_host
        self.http = HTTPClient(self._broker_host)
        self.socket_config = SocketConfig(host=self._local_host)
        self.socket = SocketClient(self.socket_config)
