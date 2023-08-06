from typing import Dict, List
from .common import MessageAttribute
from datetime import datetime
from aws_lambda_utils import BaseModelOptionalFields


class SNSMessage(BaseModelOptionalFields):
    Message: str
    MessageAttributes: Dict[str, MessageAttribute]
    MessageId: str
    Signature: str
    SignatureVersion: str
    SigningCertUrl: str
    Subject: str
    Timestamp: datetime
    TopicArn: str
    Type: str
    UnsubscribeUrl: str


class SNSRecord(BaseModelOptionalFields):
    EventSource: str
    EventSubscriptionArn: str
    EventVersion: str
    Sns: SNSMessage


class SNSEvent(BaseModelOptionalFields):
    Records: List[SNSRecord]
