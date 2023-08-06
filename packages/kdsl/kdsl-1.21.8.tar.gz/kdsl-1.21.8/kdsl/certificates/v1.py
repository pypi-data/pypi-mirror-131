from __future__ import annotations
import attr
import kdsl.certificates.v1
import kdsl.core.v1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_CertificateSigningRequestCondition(value: Union[Sequence[CertificateSigningRequestConditionUnion], OmitEnum, None]) ->Union[Sequence[CertificateSigningRequestCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CertificateSigningRequestCondition(x) for x in value]


def optional_converter_CertificateSigningRequestCondition(value: Union[CertificateSigningRequestConditionUnion, OmitEnum, None]) ->Union[CertificateSigningRequestCondition, OmitEnum, None]:
    return CertificateSigningRequestCondition(**value) if isinstance(value, dict) else value


def optional_converter_CertificateSigningRequestSpec(value: Union[CertificateSigningRequestSpecUnion, OmitEnum, None]) ->Union[CertificateSigningRequestSpec, OmitEnum, None]:
    return CertificateSigningRequestSpec(**value) if isinstance(value, dict) else value


def optional_converter_CertificateSigningRequestStatus(value: Union[CertificateSigningRequestStatusUnion, OmitEnum, None]) ->Union[CertificateSigningRequestStatus, OmitEnum, None]:
    return CertificateSigningRequestStatus(**value) if isinstance(value, dict) else value


def required_converter_CertificateSigningRequestCondition(value: CertificateSigningRequestConditionUnion) ->CertificateSigningRequestCondition:
    return CertificateSigningRequestCondition(**value) if isinstance(value, dict) else value


def required_converter_CertificateSigningRequestSpec(value: CertificateSigningRequestSpecUnion) ->CertificateSigningRequestSpec:
    return CertificateSigningRequestSpec(**value) if isinstance(value, dict) else value


def required_converter_CertificateSigningRequestStatus(value: CertificateSigningRequestStatusUnion) ->CertificateSigningRequestStatus:
    return CertificateSigningRequestStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class CertificateSigningRequestCondition(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    lastUpdateTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastUpdateTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class CertificateSigningRequestConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    lastUpdateTime: str
    message: str
    reason: str


class CertificateSigningRequestConditionTypedDict(CertificateSigningRequestConditionOptionalTypedDict, total=(True)):
    status: str
    type: str


CertificateSigningRequestConditionUnion = Union[CertificateSigningRequestCondition, CertificateSigningRequestConditionTypedDict]


@attr.s(kw_only=True)
class CertificateSigningRequestSpec(K8sObject):
    request: str = attr.ib(metadata={'yaml_name': 'request'})
    signerName: str = attr.ib(metadata={'yaml_name': 'signerName'})
    extra: Union[None, OmitEnum, Mapping[str, Sequence[str]]] = attr.ib(metadata={'yaml_name': 'extra'}, default=OMIT)
    groups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'groups'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)
    usages: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'usages'}, default=OMIT)
    username: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'username'}, default=OMIT)


class CertificateSigningRequestSpecOptionalTypedDict(TypedDict, total=(False)):
    extra: Mapping[str, Sequence[str]]
    groups: Sequence[str]
    uid: str
    usages: Sequence[str]
    username: str


class CertificateSigningRequestSpecTypedDict(CertificateSigningRequestSpecOptionalTypedDict, total=(True)):
    request: str
    signerName: str


CertificateSigningRequestSpecUnion = Union[CertificateSigningRequestSpec, CertificateSigningRequestSpecTypedDict]


@attr.s(kw_only=True)
class CertificateSigningRequestStatus(K8sObject):
    certificate: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'certificate'}, default=OMIT)
    conditions: Union[None, OmitEnum, Sequence[CertificateSigningRequestCondition]] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_list_converter_CertificateSigningRequestCondition, default=OMIT)


class CertificateSigningRequestStatusTypedDict(TypedDict, total=(False)):
    certificate: str
    conditions: Sequence[CertificateSigningRequestCondition]


CertificateSigningRequestStatusUnion = Union[CertificateSigningRequestStatus, CertificateSigningRequestStatusTypedDict]


@attr.s(kw_only=True)
class CertificateSigningRequest(K8sResource):
    apiVersion: ClassVar[str] = 'certificates.k8s.io/v1'
    kind: ClassVar[str] = 'CertificateSigningRequest'
    spec: CertificateSigningRequestSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_CertificateSigningRequestSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, CertificateSigningRequestStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_CertificateSigningRequestStatus, default=OMIT)
