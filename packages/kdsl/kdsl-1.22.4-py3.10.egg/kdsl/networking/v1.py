from __future__ import annotations
import kdsl.networking.v1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


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


def optional_list_converter_NetworkPolicyEgressRule(value: Union[Sequence[NetworkPolicyEgressRuleUnion], OmitEnum, None]) ->Union[Sequence[NetworkPolicyEgressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyEgressRule(x) for x in value]


def optional_list_converter_NetworkPolicyIngressRule(value: Union[Sequence[NetworkPolicyIngressRuleUnion], OmitEnum, None]) ->Union[Sequence[NetworkPolicyIngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyIngressRule(x) for x in value]


def optional_list_converter_NetworkPolicyPeer(value: Union[Sequence[NetworkPolicyPeerUnion], OmitEnum, None]) ->Union[Sequence[NetworkPolicyPeer], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPeer(x) for x in value]


def optional_list_converter_NetworkPolicyPort(value: Union[Sequence[NetworkPolicyPortUnion], OmitEnum, None]) ->Union[Sequence[NetworkPolicyPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPort(x) for x in value]


def required_list_converter_HTTPIngressPath(value: Sequence[HTTPIngressPathUnion]) ->Sequence[HTTPIngressPath]:
    return [required_converter_HTTPIngressPath(x) for x in value]


def optional_converter_HTTPIngressPath(value: Union[HTTPIngressPathUnion, OmitEnum, None]) ->Union[HTTPIngressPath, OmitEnum, None]:
    return HTTPIngressPath(**value) if isinstance(value, dict) else value


def optional_converter_HTTPIngressRuleValue(value: Union[HTTPIngressRuleValueUnion, OmitEnum, None]) ->Union[HTTPIngressRuleValue, OmitEnum, None]:
    return HTTPIngressRuleValue(**value) if isinstance(value, dict) else value


def optional_converter_IPBlock(value: Union[IPBlockUnion, OmitEnum, None]) ->Union[IPBlock, OmitEnum, None]:
    return IPBlock(**value) if isinstance(value, dict) else value


def optional_converter_IngressBackend(value: Union[IngressBackendUnion, OmitEnum, None]) ->Union[IngressBackend, OmitEnum, None]:
    return IngressBackend(**value) if isinstance(value, dict) else value


def optional_converter_IngressClassParametersReference(value: Union[IngressClassParametersReferenceUnion, OmitEnum, None]) ->Union[IngressClassParametersReference, OmitEnum, None]:
    return IngressClassParametersReference(**value) if isinstance(value, dict) else value


def optional_converter_IngressClassSpec(value: Union[IngressClassSpecUnion, OmitEnum, None]) ->Union[IngressClassSpec, OmitEnum, None]:
    return IngressClassSpec(**value) if isinstance(value, dict) else value


def optional_converter_IngressRule(value: Union[IngressRuleUnion, OmitEnum, None]) ->Union[IngressRule, OmitEnum, None]:
    return IngressRule(**value) if isinstance(value, dict) else value


def optional_converter_IngressServiceBackend(value: Union[IngressServiceBackendUnion, OmitEnum, None]) ->Union[IngressServiceBackend, OmitEnum, None]:
    return IngressServiceBackend(**value) if isinstance(value, dict) else value


def optional_converter_IngressSpec(value: Union[IngressSpecUnion, OmitEnum, None]) ->Union[IngressSpec, OmitEnum, None]:
    return IngressSpec(**value) if isinstance(value, dict) else value


def optional_converter_IngressStatus(value: Union[IngressStatusUnion, OmitEnum, None]) ->Union[IngressStatus, OmitEnum, None]:
    return IngressStatus(**value) if isinstance(value, dict) else value


def optional_converter_IngressTLS(value: Union[IngressTLSUnion, OmitEnum, None]) ->Union[IngressTLS, OmitEnum, None]:
    return IngressTLS(**value) if isinstance(value, dict) else value


def optional_converter_NetworkPolicyEgressRule(value: Union[NetworkPolicyEgressRuleUnion, OmitEnum, None]) ->Union[NetworkPolicyEgressRule, OmitEnum, None]:
    return NetworkPolicyEgressRule(**value) if isinstance(value, dict) else value


def optional_converter_NetworkPolicyIngressRule(value: Union[NetworkPolicyIngressRuleUnion, OmitEnum, None]) ->Union[NetworkPolicyIngressRule, OmitEnum, None]:
    return NetworkPolicyIngressRule(**value) if isinstance(value, dict) else value


def optional_converter_NetworkPolicyPeer(value: Union[NetworkPolicyPeerUnion, OmitEnum, None]) ->Union[NetworkPolicyPeer, OmitEnum, None]:
    return NetworkPolicyPeer(**value) if isinstance(value, dict) else value


def optional_converter_NetworkPolicyPort(value: Union[NetworkPolicyPortUnion, OmitEnum, None]) ->Union[NetworkPolicyPort, OmitEnum, None]:
    return NetworkPolicyPort(**value) if isinstance(value, dict) else value


def optional_converter_NetworkPolicySpec(value: Union[NetworkPolicySpecUnion, OmitEnum, None]) ->Union[NetworkPolicySpec, OmitEnum, None]:
    return NetworkPolicySpec(**value) if isinstance(value, dict) else value


def optional_converter_ServiceBackendPort(value: Union[ServiceBackendPortUnion, OmitEnum, None]) ->Union[ServiceBackendPort, OmitEnum, None]:
    return ServiceBackendPort(**value) if isinstance(value, dict) else value


def required_converter_HTTPIngressPath(value: HTTPIngressPathUnion) ->HTTPIngressPath:
    return HTTPIngressPath(**value) if isinstance(value, dict) else value


def required_converter_HTTPIngressRuleValue(value: HTTPIngressRuleValueUnion) ->HTTPIngressRuleValue:
    return HTTPIngressRuleValue(**value) if isinstance(value, dict) else value


def required_converter_IPBlock(value: IPBlockUnion) ->IPBlock:
    return IPBlock(**value) if isinstance(value, dict) else value


def required_converter_IngressBackend(value: IngressBackendUnion) ->IngressBackend:
    return IngressBackend(**value) if isinstance(value, dict) else value


def required_converter_IngressClassParametersReference(value: IngressClassParametersReferenceUnion) ->IngressClassParametersReference:
    return IngressClassParametersReference(**value) if isinstance(value, dict) else value


def required_converter_IngressClassSpec(value: IngressClassSpecUnion) ->IngressClassSpec:
    return IngressClassSpec(**value) if isinstance(value, dict) else value


def required_converter_IngressRule(value: IngressRuleUnion) ->IngressRule:
    return IngressRule(**value) if isinstance(value, dict) else value


def required_converter_IngressServiceBackend(value: IngressServiceBackendUnion) ->IngressServiceBackend:
    return IngressServiceBackend(**value) if isinstance(value, dict) else value


def required_converter_IngressSpec(value: IngressSpecUnion) ->IngressSpec:
    return IngressSpec(**value) if isinstance(value, dict) else value


def required_converter_IngressStatus(value: IngressStatusUnion) ->IngressStatus:
    return IngressStatus(**value) if isinstance(value, dict) else value


def required_converter_IngressTLS(value: IngressTLSUnion) ->IngressTLS:
    return IngressTLS(**value) if isinstance(value, dict) else value


def required_converter_NetworkPolicyEgressRule(value: NetworkPolicyEgressRuleUnion) ->NetworkPolicyEgressRule:
    return NetworkPolicyEgressRule(**value) if isinstance(value, dict) else value


def required_converter_NetworkPolicyIngressRule(value: NetworkPolicyIngressRuleUnion) ->NetworkPolicyIngressRule:
    return NetworkPolicyIngressRule(**value) if isinstance(value, dict) else value


def required_converter_NetworkPolicyPeer(value: NetworkPolicyPeerUnion) ->NetworkPolicyPeer:
    return NetworkPolicyPeer(**value) if isinstance(value, dict) else value


def required_converter_NetworkPolicyPort(value: NetworkPolicyPortUnion) ->NetworkPolicyPort:
    return NetworkPolicyPort(**value) if isinstance(value, dict) else value


def required_converter_NetworkPolicySpec(value: NetworkPolicySpecUnion) ->NetworkPolicySpec:
    return NetworkPolicySpec(**value) if isinstance(value, dict) else value


def required_converter_ServiceBackendPort(value: ServiceBackendPortUnion) ->ServiceBackendPort:
    return ServiceBackendPort(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class HTTPIngressPath(K8sObject):
    backend: IngressBackend = attr.ib(metadata={'yaml_name': 'backend'}, converter=required_converter_IngressBackend)
    pathType: str = attr.ib(metadata={'yaml_name': 'pathType'})
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)


class HTTPIngressPathOptionalTypedDict(TypedDict, total=(False)):
    path: str


class HTTPIngressPathTypedDict(HTTPIngressPathOptionalTypedDict, total=(True)):
    backend: IngressBackend
    pathType: str


HTTPIngressPathUnion = Union[HTTPIngressPath, HTTPIngressPathTypedDict]


@attr.s(kw_only=True)
class HTTPIngressRuleValue(K8sObject):
    paths: Sequence[HTTPIngressPath] = attr.ib(metadata={'yaml_name': 'paths'}, converter=required_list_converter_HTTPIngressPath)


class HTTPIngressRuleValueTypedDict(TypedDict, total=(True)):
    paths: Sequence[HTTPIngressPath]


HTTPIngressRuleValueUnion = Union[HTTPIngressRuleValue, HTTPIngressRuleValueTypedDict]


@attr.s(kw_only=True)
class IPBlock(K8sObject):
    cidr: str = attr.ib(metadata={'yaml_name': 'cidr'})
    except_: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'except'}, default=OMIT)


class IPBlockOptionalTypedDict(TypedDict, total=(False)):
    except_: Sequence[str]


class IPBlockTypedDict(IPBlockOptionalTypedDict, total=(True)):
    cidr: str


IPBlockUnion = Union[IPBlock, IPBlockTypedDict]


@attr.s(kw_only=True)
class IngressBackend(K8sObject):
    resource: Union[None, OmitEnum, kdsl.core.v1.TypedLocalObjectReference] = attr.ib(metadata={'yaml_name': 'resource'}, converter=kdsl.core.v1.optional_converter_TypedLocalObjectReference, default=OMIT)
    service: Union[None, OmitEnum, IngressServiceBackend] = attr.ib(metadata={'yaml_name': 'service'}, converter=optional_converter_IngressServiceBackend, default=OMIT)


class IngressBackendTypedDict(TypedDict, total=(False)):
    resource: kdsl.core.v1.TypedLocalObjectReference
    service: IngressServiceBackend


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
class IngressServiceBackend(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    port: Union[None, OmitEnum, ServiceBackendPort] = attr.ib(metadata={'yaml_name': 'port'}, converter=optional_converter_ServiceBackendPort, default=OMIT)


class IngressServiceBackendOptionalTypedDict(TypedDict, total=(False)):
    port: ServiceBackendPort


class IngressServiceBackendTypedDict(IngressServiceBackendOptionalTypedDict, total=(True)):
    name: str


IngressServiceBackendUnion = Union[IngressServiceBackend, IngressServiceBackendTypedDict]


@attr.s(kw_only=True)
class IngressSpec(K8sObject):
    defaultBackend: Union[None, OmitEnum, IngressBackend] = attr.ib(metadata={'yaml_name': 'defaultBackend'}, converter=optional_converter_IngressBackend, default=OMIT)
    ingressClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'ingressClassName'}, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[IngressRule]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_IngressRule, default=OMIT)
    tls: Union[None, OmitEnum, Sequence[IngressTLS]] = attr.ib(metadata={'yaml_name': 'tls'}, converter=optional_list_converter_IngressTLS, default=OMIT)


class IngressSpecTypedDict(TypedDict, total=(False)):
    defaultBackend: IngressBackend
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
class NetworkPolicyEgressRule(K8sObject):
    ports: Union[None, OmitEnum, Sequence[NetworkPolicyPort]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_NetworkPolicyPort, default=OMIT)
    to: Union[None, OmitEnum, Sequence[NetworkPolicyPeer]] = attr.ib(metadata={'yaml_name': 'to'}, converter=optional_list_converter_NetworkPolicyPeer, default=OMIT)


class NetworkPolicyEgressRuleTypedDict(TypedDict, total=(False)):
    ports: Sequence[NetworkPolicyPort]
    to: Sequence[NetworkPolicyPeer]


NetworkPolicyEgressRuleUnion = Union[NetworkPolicyEgressRule, NetworkPolicyEgressRuleTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyIngressRule(K8sObject):
    from_: Union[None, OmitEnum, Sequence[NetworkPolicyPeer]] = attr.ib(metadata={'yaml_name': 'from'}, converter=optional_list_converter_NetworkPolicyPeer, default=OMIT)
    ports: Union[None, OmitEnum, Sequence[NetworkPolicyPort]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_NetworkPolicyPort, default=OMIT)


class NetworkPolicyIngressRuleTypedDict(TypedDict, total=(False)):
    from_: Sequence[NetworkPolicyPeer]
    ports: Sequence[NetworkPolicyPort]


NetworkPolicyIngressRuleUnion = Union[NetworkPolicyIngressRule, NetworkPolicyIngressRuleTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyPeer(K8sObject):
    ipBlock: Union[None, OmitEnum, IPBlock] = attr.ib(metadata={'yaml_name': 'ipBlock'}, converter=optional_converter_IPBlock, default=OMIT)
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'namespaceSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    podSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'podSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class NetworkPolicyPeerTypedDict(TypedDict, total=(False)):
    ipBlock: IPBlock
    namespaceSelector: kdsl.core.v1.LabelSelector
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicyPeerUnion = Union[NetworkPolicyPeer, NetworkPolicyPeerTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyPort(K8sObject):
    endPort: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'endPort'}, default=OMIT)
    port: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'port'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)


class NetworkPolicyPortTypedDict(TypedDict, total=(False)):
    endPort: int
    port: Union[int, str]
    protocol: str


NetworkPolicyPortUnion = Union[NetworkPolicyPort, NetworkPolicyPortTypedDict]


@attr.s(kw_only=True)
class NetworkPolicySpec(K8sObject):
    podSelector: kdsl.core.v1.LabelSelector = attr.ib(metadata={'yaml_name': 'podSelector'}, converter=kdsl.core.v1.required_converter_LabelSelector)
    egress: Union[None, OmitEnum, Sequence[NetworkPolicyEgressRule]] = attr.ib(metadata={'yaml_name': 'egress'}, converter=optional_list_converter_NetworkPolicyEgressRule, default=OMIT)
    ingress: Union[None, OmitEnum, Sequence[NetworkPolicyIngressRule]] = attr.ib(metadata={'yaml_name': 'ingress'}, converter=optional_list_converter_NetworkPolicyIngressRule, default=OMIT)
    policyTypes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'policyTypes'}, default=OMIT)


class NetworkPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    egress: Sequence[NetworkPolicyEgressRule]
    ingress: Sequence[NetworkPolicyIngressRule]
    policyTypes: Sequence[str]


class NetworkPolicySpecTypedDict(NetworkPolicySpecOptionalTypedDict, total=(True)):
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicySpecUnion = Union[NetworkPolicySpec, NetworkPolicySpecTypedDict]


@attr.s(kw_only=True)
class ServiceBackendPort(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    number: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'number'}, default=OMIT)


class ServiceBackendPortTypedDict(TypedDict, total=(False)):
    name: str
    number: int


ServiceBackendPortUnion = Union[ServiceBackendPort, ServiceBackendPortTypedDict]


@attr.s(kw_only=True)
class Ingress(K8sResource):
    apiVersion: ClassVar[str] = 'networking.k8s.io/v1'
    kind: ClassVar[str] = 'Ingress'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, IngressSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_IngressSpec, default=OMIT)
    status: Union[None, OmitEnum, IngressStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_IngressStatus, default=OMIT)


@attr.s(kw_only=True)
class IngressClass(K8sResource):
    apiVersion: ClassVar[str] = 'networking.k8s.io/v1'
    kind: ClassVar[str] = 'IngressClass'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, IngressClassSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_IngressClassSpec, default=OMIT)


@attr.s(kw_only=True)
class NetworkPolicy(K8sResource):
    apiVersion: ClassVar[str] = 'networking.k8s.io/v1'
    kind: ClassVar[str] = 'NetworkPolicy'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, NetworkPolicySpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_NetworkPolicySpec, default=OMIT)
