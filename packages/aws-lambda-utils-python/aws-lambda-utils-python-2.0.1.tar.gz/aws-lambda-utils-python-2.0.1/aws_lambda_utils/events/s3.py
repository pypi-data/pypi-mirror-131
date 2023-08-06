from typing import Dict, List
from datetime import datetime
from aws_lambda_utils import BaseModelOptionalFields


class UserIdentityType(BaseModelOptionalFields):
    type: str
    principalId: str
    arn: str
    accountId: str
    accessKeyId: str
    sessionContext: Dict[str, str]


class S3BucketData(BaseModelOptionalFields):
    name: str
    ownerIdentity: Dict[str, str]
    arn: str


class S3ObjectData(BaseModelOptionalFields):
    key: str
    size: int
    eTag: str
    versionId: str
    sequencer: str


class S3Data(BaseModelOptionalFields):
    s3SchemaVersion: str
    configurationId: str
    bucket: S3BucketData
    object: S3ObjectData


class S3Records(BaseModelOptionalFields):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: datetime
    eventName: str
    userIdentity: UserIdentityType
    requestParameters: Dict[str, str]
    responseElements: Dict[str, str]
    s3: S3Data


class S3ObjectLambdaEvent(BaseModelOptionalFields):
    Records: List[S3Records]
