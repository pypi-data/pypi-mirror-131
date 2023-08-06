from dataclasses import dataclass
from typing import List
from datetime import datetime
from aws_lambda_utils import BaseOptionalDataClass


@dataclass
class SimpleEmailVerdict:
    Status: str


@dataclass
class SimpleEmailCommonHeaders(BaseOptionalDataClass):
    From: List[str]
    To: List[str]
    ReturnPath: str
    MessageId: str
    Date: str
    Subject: str


@dataclass
class SimpleEmailHeader(BaseOptionalDataClass):
    Name: str
    Value: str


@dataclass
class ReceiptAction(BaseOptionalDataClass):
    Type: str


@dataclass
class SimpleEmailReceipt(BaseOptionalDataClass):
    Recipients: List[str]
    Timestamp: datetime
    SpamVerdict: SimpleEmailVerdict
    DKIMVerdict: SimpleEmailVerdict
    SPFVerdict: SimpleEmailVerdict
    VirusVerdict: SimpleEmailVerdict
    DMARCVerdict: SimpleEmailVerdict
    Action: ReceiptAction
    ProcessingTimeMillis: int


@dataclass
class SimpleEmailMessage(BaseOptionalDataClass):
    CommonHeaders: SimpleEmailCommonHeaders
    Source: str
    Timestamp: datetime
    Destination: List[str]
    Headers: List[SimpleEmailHeader]
    HeadersTruncated: bool
    MessageId: str


@dataclass
class SimpleEmailService(BaseOptionalDataClass):
    Mail: SimpleEmailMessage
    Receipt: SimpleEmailReceipt


@dataclass
class SimpleEmailRecord(BaseOptionalDataClass):
    EventVersion: str
    EventSource: str
    Ses: SimpleEmailService


@dataclass
class SimpleEmailEvent(BaseOptionalDataClass):
    Records: List[SimpleEmailRecord]
