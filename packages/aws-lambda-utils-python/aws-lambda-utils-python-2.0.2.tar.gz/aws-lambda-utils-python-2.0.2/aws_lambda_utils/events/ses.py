from typing import List
from datetime import datetime
from aws_lambda_utils import BaseModelOptionalFields


class SimpleEmailVerdict(BaseModelOptionalFields):
    Status: str


class SimpleEmailCommonHeaders(BaseModelOptionalFields):
    From: List[str]
    To: List[str]
    ReturnPath: str
    MessageId: str
    Date: str
    Subject: str


class SimpleEmailHeader(BaseModelOptionalFields):
    Name: str
    Value: str


class ReceiptAction(BaseModelOptionalFields):
    Type: str


class SimpleEmailReceipt(BaseModelOptionalFields):
    Recipients: List[str]
    Timestamp: datetime
    SpamVerdict: SimpleEmailVerdict
    DKIMVerdict: SimpleEmailVerdict
    SPFVerdict: SimpleEmailVerdict
    VirusVerdict: SimpleEmailVerdict
    DMARCVerdict: SimpleEmailVerdict
    Action: ReceiptAction
    ProcessingTimeMillis: int


class SimpleEmailMessage(BaseModelOptionalFields):
    CommonHeaders: SimpleEmailCommonHeaders
    Source: str
    Timestamp: datetime
    Destination: List[str]
    Headers: List[SimpleEmailHeader]
    HeadersTruncated: bool
    MessageId: str


class SimpleEmailService(BaseModelOptionalFields):
    Mail: SimpleEmailMessage
    Receipt: SimpleEmailReceipt


class SimpleEmailRecord(BaseModelOptionalFields):
    EventVersion: str
    EventSource: str
    Ses: SimpleEmailService


class SimpleEmailEvent(BaseModelOptionalFields):
    Records: List[SimpleEmailRecord]
