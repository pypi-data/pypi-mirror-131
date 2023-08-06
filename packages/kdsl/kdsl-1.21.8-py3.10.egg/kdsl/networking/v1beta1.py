from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.networking.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_IngressRule(value: Union[Sequence[IngressRuleUnion], OmitEnum, None]) ->Union[Sequence[IngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressRule(x) for x in value]


def optional_list_converter_IngressTLS(value: Union[Sequence[IngressTLSUnion], OmitEnum, None]) ->Union[Sequence[IngressTLS], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressTLS(x) for x in value]


def required_list_converter_HTTPIngressPath(value: Sequence[HTTPIngressPathUnion]) ->Sequence[HTTPIngressPath]:
    return [required_converter_HTTPIngressPath(x) for x in value]


def optional_converter_HTTPIngressPath(value: Union[HTTPIngressPathUnion, OmitEnum, None]) ->Union[HTTPIngressPath, OmitEnum, None]:
    return HTTPIngressPath(**value) if isinstance(value, dict) else value


def optional_converter_HTTPIngressRuleValue(value: Union[HTTPIngressRuleValueUnion, OmitEnum, None]) ->Union[HTTPIngressRuleValue, OmitEnum, None]:
    return HTTPIngressRuleValue(**value) if isinstance(value, dict) else value


def optional_converter_IngressBackend(value: Union[IngressBackendUnion, OmitEnum, None]) ->Union[IngressBackend, OmitEnum, None]:
    return IngressBackend(**value) if isinstance(value, dict) else value


def optional_converter_IngressClassParametersReference(value: Union[IngressClassParametersReferenceUnion, OmitEnum, None]) ->Union[IngressClassParametersReference, OmitEnum, None]:
    return IngressClassParametersReference(**value) if isinstance(value, dict) else value


def optional_converter_IngressClassSpec(value: Union[IngressClassSpecUnion, OmitEnum, None]) ->Union[IngressClassSpec, OmitEnum, None]:
    return IngressClassSpec(**value) if isinstance(value, dict) else value


def optional_converter_IngressRule(value: Union[IngressRuleUnion, OmitEnum, None]) ->Union[IngressRule, OmitEnum, None]:
    return IngressRule(**value) if isinstance(value, dict) else value


def optional_converter_IngressSpec(value: Union[IngressSpecUnion, OmitEnum, None]) ->Union[IngressSpec, OmitEnum, None]:
    return IngressSpec(**value) if isinstance(value, dict) else value


def optional_converter_IngressStatus(value: Union[IngressStatusUnion, OmitEnum, None]) ->Union[IngressStatus, OmitEnum, None]:
    return IngressStatus(**value) if isinstance(value, dict) else value


def optional_converter_IngressTLS(value: Union[IngressTLSUnion, OmitEnum, None]) ->Union[IngressTLS, OmitEnum, None]:
    return IngressTLS(**value) if isinstance(value, dict) else value


def required_converter_HTTPIngressPath(value: HTTPIngressPathUnion) ->HTTPIngressPath:
    return HTTPIngressPath(**value) if isinstance(value, dict) else value


def required_converter_HTTPIngressRuleValue(value: HTTPIngressRuleValueUnion) ->HTTPIngressRuleValue:
    return HTTPIngressRuleValue(**value) if isinstance(value, dict) else value


def required_converter_IngressBackend(value: IngressBackendUnion) ->IngressBackend:
    return IngressBackend(**value) if isinstance(value, dict) else value


def required_converter_IngressClassParametersReference(value: IngressClassParametersReferenceUnion) ->IngressClassParametersReference:
    return IngressClassParametersReference(**value) if isinstance(value, dict) else value


def required_converter_IngressClassSpec(value: IngressClassSpecUnion) ->IngressClassSpec:
    return IngressClassSpec(**value) if isinstance(value, dict) else value


def required_converter_IngressRule(value: IngressRuleUnion) ->IngressRule:
    return IngressRule(**value) if isinstance(value, dict) else value


def required_converter_IngressSpec(value: IngressSpecUnion) ->IngressSpec:
    return IngressSpec(**value) if isinstance(value, dict) else value


def required_converter_IngressStatus(value: IngressStatusUnion) ->IngressStatus:
    return IngressStatus(**value) if isinstance(value, dict) else value


def required_converter_IngressTLS(value: IngressTLSUnion) ->IngressTLS:
    return IngressTLS(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class HTTPIngressPath(K8sObject):
    backend: IngressBackend = attr.ib(metadata={'yaml_name': 'backend'}, converter=required_converter_IngressBackend)
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    pathType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'pathType'}, default=OMIT)


class HTTPIngressPathOptionalTypedDict(TypedDict, total=(False)):
    path: str
    pathType: str


class HTTPIngressPathTypedDict(HTTPIngressPathOptionalTypedDict, total=(True)):
    backend: IngressBackend


HTTPIngressPathUnion = Union[HTTPIngressPath, HTTPIngressPathTypedDict]


@attr.s(kw_only=True)
class HTTPIngressRuleValue(K8sObject):
    paths: Sequence[HTTPIngressPath] = attr.ib(metadata={'yaml_name': 'paths'}, converter=required_list_converter_HTTPIngressPath)


class HTTPIngressRuleValueTypedDict(TypedDict, total=(True)):
    paths: Sequence[HTTPIngressPath]


HTTPIngressRuleValueUnion = Union[HTTPIngressRuleValue, HTTPIngressRuleValueTypedDict]


@attr.s(kw_only=True)
class IngressBackend(K8sObject):
    resource: Union[None, OmitEnum, kdsl.core.v1.TypedLocalObjectReference] = attr.ib(metadata={'yaml_name': 'resource'}, converter=kdsl.core.v1.optional_converter_TypedLocalObjectReference, default=OMIT)
    serviceName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'serviceName'}, default=OMIT)
    servicePort: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'servicePort'}, default=OMIT)


class IngressBackendTypedDict(TypedDict, total=(False)):
    resource: kdsl.core.v1.TypedLocalObjectReference
    serviceName: str
    servicePort: Union[int, str]


IngressBackendUnion = Union[IngressBackend, IngressBackendTypedDict]


@attr.s(kw_only=True)
class IngressClassParametersReference(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    apiGroup: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiGroup'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    scope: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'scope'}, default=OMIT)


class IngressClassParametersReferenceOptionalTypedDict(TypedDict, total=(False)):
    apiGroup: str
    namespace: str
    scope: str


class IngressClassParametersReferenceTypedDict(IngressClassParametersReferenceOptionalTypedDict, total=(True)):
    kind: str
    name: str


IngressClassParametersReferenceUnion = Union[IngressClassParametersReference, IngressClassParametersReferenceTypedDict]


@attr.s(kw_only=True)
class IngressClassSpec(K8sObject):
    controller: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'controller'}, default=OMIT)
    parameters: Union[None, OmitEnum, IngressClassParametersReference] = attr.ib(metadata={'yaml_name': 'parameters'}, converter=optional_converter_IngressClassParametersReference, default=OMIT)


class IngressClassSpecTypedDict(TypedDict, total=(False)):
    controller: str
    parameters: IngressClassParametersReference


IngressClassSpecUnion = Union[IngressClassSpec, IngressClassSpecTypedDict]


@attr.s(kw_only=True)
class IngressRule(K8sObject):
    host: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'host'}, default=OMIT)
    http: Union[None, OmitEnum, HTTPIngressRuleValue] = attr.ib(metadata={'yaml_name': 'http'}, converter=optional_converter_HTTPIngressRuleValue, default=OMIT)


class IngressRuleTypedDict(TypedDict, total=(False)):
    host: str
    http: HTTPIngressRuleValue


IngressRuleUnion = Union[IngressRule, IngressRuleTypedDict]


@attr.s(kw_only=True)
class IngressSpec(K8sObject):
    backend: Union[None, OmitEnum, IngressBackend] = attr.ib(metadata={'yaml_name': 'backend'}, converter=optional_converter_IngressBackend, default=OMIT)
    ingressClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'ingressClassName'}, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[IngressRule]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_IngressRule, default=OMIT)
    tls: Union[None, OmitEnum, Sequence[IngressTLS]] = attr.ib(metadata={'yaml_name': 'tls'}, converter=optional_list_converter_IngressTLS, default=OMIT)


class IngressSpecTypedDict(TypedDict, total=(False)):
    backend: IngressBackend
    ingressClassName: str
    rules: Sequence[IngressRule]
    tls: Sequence[IngressTLS]


IngressSpecUnion = Union[IngressSpec, IngressSpecTypedDict]


@attr.s(kw_only=True)
class IngressStatus(K8sObject):
    loadBalancer: Union[None, OmitEnum, kdsl.core.v1.LoadBalancerStatus] = attr.ib(metadata={'yaml_name': 'loadBalancer'}, converter=kdsl.core.v1.optional_converter_LoadBalancerStatus, default=OMIT)


class IngressStatusTypedDict(TypedDict, total=(False)):
    loadBalancer: kdsl.core.v1.LoadBalancerStatus


IngressStatusUnion = Union[IngressStatus, IngressStatusTypedDict]


@attr.s(kw_only=True)
class IngressTLS(K8sObject):
    hosts: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'hosts'}, default=OMIT)
    secretName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'secretName'}, default=OMIT)


class IngressTLSTypedDict(TypedDict, total=(False)):
    hosts: Sequence[str]
    secretName: str


IngressTLSUnion = Union[IngressTLS, IngressTLSTypedDict]


@attr.s(kw_only=True)
class Ingress(K8sResource):
    apiVersion: ClassVar[str] = 'networking.k8s.io/v1beta1'
    kind: ClassVar[str] = 'Ingress'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, IngressSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_IngressSpec, default=OMIT)
    status: Union[None, OmitEnum, IngressStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_IngressStatus, default=OMIT)


@attr.s(kw_only=True)
class IngressClass(K8sResource):
    apiVersion: ClassVar[str] = 'networking.k8s.io/v1beta1'
    kind: ClassVar[str] = 'IngressClass'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, IngressClassSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_IngressClassSpec, default=OMIT)
