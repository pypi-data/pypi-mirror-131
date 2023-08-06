from abc import ABC, abstractmethod
from typing import Dict
from aws_lambda_utils import BaseModelOptionalFields


class Identity(BaseModelOptionalFields):
    cognito_identity_id: str
    cognito_identity_pool_id: str


class Client(BaseModelOptionalFields):
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str
    custom: Dict[str, str]
    env: Dict[str, str]


class ClientContext(BaseModelOptionalFields):
    client: Client


class IContextData(BaseModelOptionalFields):
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: Identity
    client_context: ClientContext


class IContext(ABC, IContextData):
    @staticmethod
    @abstractmethod
    def get_remaining_time_in_millis() -> int:
        """
        Returns:
            int:  Returns the number of milliseconds left before the execution times out.
        """
