from typing import Dict, List
from mypy_boto3_sqs.type_defs import MessageAttributeValueTypeDef
from aws_lambda_utils import BaseModelOptionalFields


class SQSRecord(BaseModelOptionalFields):
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


class SQSEvent(BaseModelOptionalFields):
    Records: List[SQSRecord]
