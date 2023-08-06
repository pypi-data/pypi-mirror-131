from dataclasses import dataclass
from typing import Dict, Sequence


@dataclass
class APIGatewayHttpApiV2ProxyResponse:
    StatusCode: int
    Headers: Dict[str, str]
    Cookies: Sequence[str]
    Body: str
    IsBase64Encoded: bool
