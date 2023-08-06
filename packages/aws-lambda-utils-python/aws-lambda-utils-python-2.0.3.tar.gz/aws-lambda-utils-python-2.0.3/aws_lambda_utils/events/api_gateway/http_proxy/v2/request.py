from typing import Dict, List, Sequence
from aws_lambda_utils import BaseModelOptionalFields


class JwtDescription(BaseModelOptionalFields):
    Claims: Dict[str, str]
    Scopes: Sequence[str]


class CognitoIdentityDescription(BaseModelOptionalFields):
    AMR: List[str]
    IdentityId: str
    IdentityPoolId: str


class IAMDescription(BaseModelOptionalFields):
    AccessKey: str
    AccountId: str
    CallerId: str
    CognitoIdentity: CognitoIdentityDescription
    PrincipalOrgId: str
    UserARN: str
    UserId: str


class AuthorizerDescription(BaseModelOptionalFields):
    Jwt: JwtDescription
    Lambda: Dict[str, str]
    IAM: IAMDescription


class HttpDescription(BaseModelOptionalFields):
    Method: str
    Path: str
    Protocol: str
    SourceIp: str
    UserAgent: str


class ClientCertValidity(BaseModelOptionalFields):
    NotBefore: str
    NotAfter: str


class ProxyRequestClientCert(BaseModelOptionalFields):
    ClientCertPem: str
    SubjectDN: str
    IssuerDN: str
    SerialNumber: str
    Validity: ClientCertValidity


class ProxyRequestAuthentication(BaseModelOptionalFields):
    ClientCert: ProxyRequestClientCert


class ProxyRequestContext(BaseModelOptionalFields):
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


class APIGatewayHttpApiV2ProxyRequest(BaseModelOptionalFields):
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
