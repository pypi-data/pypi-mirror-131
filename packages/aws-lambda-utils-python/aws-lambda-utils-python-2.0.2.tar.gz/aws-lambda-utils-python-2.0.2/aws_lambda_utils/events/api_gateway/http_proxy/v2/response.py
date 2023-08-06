from typing import Dict, Sequence

from aws_lambda_utils import BaseModelOptionalFields


class APIGatewayHttpApiV2ProxyResponse(BaseModelOptionalFields):
    StatusCode: int
    Headers: Dict[str, str]
    Cookies: Sequence[str]
    Body: str
    IsBase64Encoded: bool
