from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.apiregistration.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_mlist_converter_APIServiceConditionItem(value: Union[Mapping[str, APIServiceConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, APIServiceConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_APIServiceConditionItem(v) for k, v in value.items()}


def optional_converter_APIServiceConditionItem(value: Union[APIServiceConditionItemUnion, OmitEnum, None]) ->Union[APIServiceConditionItem, OmitEnum, None]:
    return APIServiceConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_APIServiceSpec(value: Union[APIServiceSpecUnion, OmitEnum, None]) ->Union[APIServiceSpec, OmitEnum, None]:
    return APIServiceSpec(**value) if isinstance(value, dict) else value


def optional_converter_APIServiceStatus(value: Union[APIServiceStatusUnion, OmitEnum, None]) ->Union[APIServiceStatus, OmitEnum, None]:
    return APIServiceStatus(**value) if isinstance(value, dict) else value


def optional_converter_ServiceReference(value: Union[ServiceReferenceUnion, OmitEnum, None]) ->Union[ServiceReference, OmitEnum, None]:
    return ServiceReference(**value) if isinstance(value, dict) else value


def required_converter_APIServiceConditionItem(value: APIServiceConditionItemUnion) ->APIServiceConditionItem:
    return APIServiceConditionItem(**value) if isinstance(value, dict) else value


def required_converter_APIServiceSpec(value: APIServiceSpecUnion) ->APIServiceSpec:
    return APIServiceSpec(**value) if isinstance(value, dict) else value


def required_converter_APIServiceStatus(value: APIServiceStatusUnion) ->APIServiceStatus:
    return APIServiceStatus(**value) if isinstance(value, dict) else value


def required_converter_ServiceReference(value: ServiceReferenceUnion) ->ServiceReference:
    return ServiceReference(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class APIServiceConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class APIServiceConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class APIServiceConditionItemTypedDict(APIServiceConditionItemOptionalTypedDict, total=(True)):
    status: str


APIServiceConditionItemUnion = Union[APIServiceConditionItem, APIServiceConditionItemTypedDict]


@attr.s(kw_only=True)
class APIServiceSpec(K8sObject):
    groupPriorityMinimum: int = attr.ib(metadata={'yaml_name': 'groupPriorityMinimum'})
    versionPriority: int = attr.ib(metadata={'yaml_name': 'versionPriority'})
    caBundle: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'caBundle'}, default=OMIT)
    group: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'group'}, default=OMIT)
    insecureSkipTLSVerify: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'insecureSkipTLSVerify'}, default=OMIT)
    service: Union[None, OmitEnum, ServiceReference] = attr.ib(metadata={'yaml_name': 'service'}, converter=optional_converter_ServiceReference, default=OMIT)
    version: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'version'}, default=OMIT)


class APIServiceSpecOptionalTypedDict(TypedDict, total=(False)):
    caBundle: str
    group: str
    insecureSkipTLSVerify: bool
    service: ServiceReference
    version: str


class APIServiceSpecTypedDict(APIServiceSpecOptionalTypedDict, total=(True)):
    groupPriorityMinimum: int
    versionPriority: int


APIServiceSpecUnion = Union[APIServiceSpec, APIServiceSpecTypedDict]


@attr.s(kw_only=True)
class APIServiceStatus(K8sObject):
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.apiregistration.v1beta1.APIServiceConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_APIServiceConditionItem, default=OMIT)


class APIServiceStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.apiregistration.v1beta1.APIServiceConditionItem]


APIServiceStatusUnion = Union[APIServiceStatus, APIServiceStatusTypedDict]


@attr.s(kw_only=True)
class ServiceReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    port: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'port'}, default=OMIT)


class ServiceReferenceTypedDict(TypedDict, total=(False)):
    name: str
    namespace: str
    port: int


ServiceReferenceUnion = Union[ServiceReference, ServiceReferenceTypedDict]


@attr.s(kw_only=True)
class APIService(K8sResource):
    apiVersion: ClassVar[str] = 'apiregistration.k8s.io/v1beta1'
    kind: ClassVar[str] = 'APIService'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, APIServiceSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_APIServiceSpec, default=OMIT)
    status: Union[None, OmitEnum, APIServiceStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_APIServiceStatus, default=OMIT)
