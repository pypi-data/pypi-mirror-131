from dataclasses import dataclass
from typing import Dict, List, Sequence
from aws_lambda_utils import BaseOptionalDataClass


@dataclass
class JwtDescription(BaseOptionalDataClass):
    Claims: Dict[str, str]
    Scopes: Sequence[str]


@dataclass
class CognitoIdentityDescription(BaseOptionalDataClass):
    AMR: List[str]
    IdentityId: str
    IdentityPoolId: str


@dataclass
class IAMDescription(BaseOptionalDataClass):
    AccessKey: str
    AccountId: str
    CallerId: str
    CognitoIdentity: CognitoIdentityDescription
    PrincipalOrgId: str
    UserARN: str
    UserId: str


@dataclass
class AuthorizerDescription(BaseOptionalDataClass):
    Jwt: JwtDescription
    Lambda: Dict[str, str]
    IAM: IAMDescription


@dataclass
class HttpDescription(BaseOptionalDataClass):
    Method: str
    Path: str
    Protocol: str
    SourceIp: str
    UserAgent: str


@dataclass
class ClientCertValidity(BaseOptionalDataClass):
    NotBefore: str
    NotAfter: str


@dataclass
class ProxyRequestClientCert(BaseOptionalDataClass):
    ClientCertPem: str
    SubjectDN: str
    IssuerDN: str
    SerialNumber: str
    Validity: ClientCertValidity


@dataclass
class ProxyRequestAuthentication(BaseOptionalDataClass):
    ClientCert: ProxyRequestClientCert


@dataclass
class ProxyRequestContext(BaseOptionalDataClass):
    AccountId: str
    ApiId: str
    Authorizer: AuthorizerDescription
    DomainName: str
    DomainPrefix: str
    Http: HttpDescription
    RequestId: str
    RouteId: str
    RouteKey: str
    Stage: str
    Time: str
    TimeEpoch: int
    Authentication: ProxyRequestAuthentication


@dataclass
class APIGatewayHttpApiV2ProxyRequest(BaseOptionalDataClass):
    Version: str
    RouteKey: str
    RawPath: str
    RawQueryString: str
    Cookies: Sequence[str]
    Headers: Dict[str, str]
    QueryStringParameters: Dict[str, str]
    RequestContext: ProxyRequestContext
    Body: str
    PathParameters: Dict[str, str]
    IsBase64Encoded: bool
    StageVariables: Dict[str, str]
