import socket
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class FunasrTranscriberProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        host = credentials.get('funasr_host')
        port = credentials.get('funasr_port')

        if not host or not port:
            raise ToolProviderCredentialValidationError("FunASR host and port are required.")

        try:
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                raise ValueError("Port number must be between 1 and 65535.")
        except ValueError as e:
            raise ToolProviderCredentialValidationError(f"Invalid port number: {e}")

        try:
            with socket.create_connection((host, port_num), timeout=5):
                pass
        except (socket.timeout, socket.error) as e:
            raise ToolProviderCredentialValidationError(f"Failed to connect to FunASR server at {host}:{port_num}. Error: {e}")
