from pydantic.dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
from aws_lambda_utils import BaseOptionalDataClass


@dataclass
class UserIdentityType(BaseOptionalDataClass):
    type: str
    principalId: str
    arn: str
    accountId: str
    accessKeyId: str
    sessionContext: Dict[str, str]


@dataclass
class S3BucketData(BaseOptionalDataClass):
    name: str
    ownerIdentity: Dict[str, str]
    arn: str


@dataclass
class S3ObjectData(BaseOptionalDataClass):
    key: str
    size: int
    eTag: str
    versionId: str
    sequencer: str


@dataclass
class S3Data(BaseOptionalDataClass):
    s3SchemaVersion: str
    configurationId: str
    bucket: S3BucketData
    object: S3ObjectData


@dataclass
class S3Records(BaseOptionalDataClass):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: datetime
    eventName: str
    userIdentity: UserIdentityType
    requestParameters: Dict[str, str]
    responseElements: Dict[str, str]
    s3: S3Data


@dataclass
class S3ObjectLambdaEvent(BaseOptionalDataClass):
    Records: List[S3Records]
