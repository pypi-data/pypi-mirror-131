from typing import Dict, List
from aws_lambda_utils import BaseModelOptionalFields


class APIGatewayProxyResponse(BaseModelOptionalFields):
    StatusCode: int
    Headers: Dict[str, str]
    MultiValueHeaders: Dict[str, List[str]]
    Body: str
    IsBase64Encoded: bool
