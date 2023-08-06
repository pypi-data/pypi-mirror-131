from dataclasses import dataclass
from typing import Dict, List
from .common import MessageAttribute
from datetime import datetime
from aws_lambda_utils import BaseOptionalDataClass


@dataclass
class SNSMessage(BaseOptionalDataClass):
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


@dataclass
class SNSRecord(BaseOptionalDataClass):
    EventSource: str
    EventSubscriptionArn: str
    EventVersion: str
    Sns: SNSMessage


@dataclass
class SNSEvent(BaseOptionalDataClass):
    Records: List[SNSRecord]
