from dataclasses import dataclass
from typing import Dict, List
from mypy_boto3_sqs.type_defs import MessageAttributeValueTypeDef
from aws_lambda_utils import BaseOptionalDataClass


@dataclass
class SQSRecord(BaseOptionalDataClass):
    messageId: str
    receiptHandle: str
    body: str
    md5OfBody: str
    md5OfMessageAttributes: str
    eventSourceArn: str
    eventSource: str
    awsRegion: str
    attributes: Dict[str, str]
    messageAttributes: Dict[str, MessageAttributeValueTypeDef]


@dataclass
class SQSEvent(BaseOptionalDataClass):
    Records: List[SQSRecord]
