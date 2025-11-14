from typing import Any

from dify_plugin import ToolProvider


class ExcelProcessProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        pass
