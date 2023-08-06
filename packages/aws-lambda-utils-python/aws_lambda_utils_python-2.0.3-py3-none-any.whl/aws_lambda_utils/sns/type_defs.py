from enum import Enum


class SnsProtocolSubscribeTypes(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    EMAIL = "email"
    EMAIL_JSON = "email-json"
    SMS = "sms"
    SQS = "sqs"
    APPLICATION = "application"
    LAMBDA = "lambda"
    FIREHOSE = "firehose"


class SnsAttributeNames(str, Enum):
    DeliveryPolicy = "DeliveryPolicy"
    DisplayName = "DisplayName"
    FifoTopic = "FifoTopic"
    Policy = "Policy"
    KmsMasterKeyId = "KmsMasterKeyId"
    ContentBasedDeduplication = "ContentBasedDeduplication"


class SmsTypes(str, Enum):
    Transactional = "Transactional"
    Promotional = "Promotional"
