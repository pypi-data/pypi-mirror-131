from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.discovery.v1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_EndpointPort(value: Union[Sequence[EndpointPortUnion], OmitEnum, None]) ->Union[Sequence[EndpointPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointPort(x) for x in value]


def optional_list_converter_ForZone(value: Union[Sequence[ForZoneUnion], OmitEnum, None]) ->Union[Sequence[ForZone], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ForZone(x) for x in value]


def required_list_converter_Endpoint(value: Sequence[EndpointUnion]) ->Sequence[Endpoint]:
    return [required_converter_Endpoint(x) for x in value]


def optional_converter_Endpoint(value: Union[EndpointUnion, OmitEnum, None]) ->Union[Endpoint, OmitEnum, None]:
    return Endpoint(**value) if isinstance(value, dict) else value


def optional_converter_EndpointConditions(value: Union[EndpointConditionsUnion, OmitEnum, None]) ->Union[EndpointConditions, OmitEnum, None]:
    return EndpointConditions(**value) if isinstance(value, dict) else value


def optional_converter_EndpointHints(value: Union[EndpointHintsUnion, OmitEnum, None]) ->Union[EndpointHints, OmitEnum, None]:
    return EndpointHints(**value) if isinstance(value, dict) else value


def optional_converter_EndpointPort(value: Union[EndpointPortUnion, OmitEnum, None]) ->Union[EndpointPort, OmitEnum, None]:
    return EndpointPort(**value) if isinstance(value, dict) else value


def optional_converter_ForZone(value: Union[ForZoneUnion, OmitEnum, None]) ->Union[ForZone, OmitEnum, None]:
    return ForZone(**value) if isinstance(value, dict) else value


def required_converter_Endpoint(value: EndpointUnion) ->Endpoint:
    return Endpoint(**value) if isinstance(value, dict) else value


def required_converter_EndpointConditions(value: EndpointConditionsUnion) ->EndpointConditions:
    return EndpointConditions(**value) if isinstance(value, dict) else value


def required_converter_EndpointHints(value: EndpointHintsUnion) ->EndpointHints:
    return EndpointHints(**value) if isinstance(value, dict) else value


def required_converter_EndpointPort(value: EndpointPortUnion) ->EndpointPort:
    return EndpointPort(**value) if isinstance(value, dict) else value


def required_converter_ForZone(value: ForZoneUnion) ->ForZone:
    return ForZone(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class Endpoint(K8sObject):
    addresses: Sequence[str] = attr.ib(metadata={'yaml_name': 'addresses'})
    conditions: Union[None, OmitEnum, EndpointConditions] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_converter_EndpointConditions, default=OMIT)
    deprecatedTopology: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'deprecatedTopology'}, default=OMIT)
    hints: Union[None, OmitEnum, EndpointHints] = attr.ib(metadata={'yaml_name': 'hints'}, converter=optional_converter_EndpointHints, default=OMIT)
    hostname: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostname'}, default=OMIT)
    nodeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'nodeName'}, default=OMIT)
    targetRef: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(metadata={'yaml_name': 'targetRef'}, converter=kdsl.core.v1.optional_converter_ObjectReference, default=OMIT)
    zone: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'zone'}, default=OMIT)


class EndpointOptionalTypedDict(TypedDict, total=(False)):
    conditions: EndpointConditions
    deprecatedTopology: Mapping[str, str]
    hints: EndpointHints
    hostname: str
    nodeName: str
    targetRef: kdsl.core.v1.ObjectReference
    zone: str


class EndpointTypedDict(EndpointOptionalTypedDict, total=(True)):
    addresses: Sequence[str]


EndpointUnion = Union[Endpoint, EndpointTypedDict]


@attr.s(kw_only=True)
class EndpointConditions(K8sObject):
    ready: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'ready'}, default=OMIT)
    serving: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'serving'}, default=OMIT)
    terminating: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'terminating'}, default=OMIT)


class EndpointConditionsTypedDict(TypedDict, total=(False)):
    ready: bool
    serving: bool
    terminating: bool


EndpointConditionsUnion = Union[EndpointConditions, EndpointConditionsTypedDict]


@attr.s(kw_only=True)
class EndpointHints(K8sObject):
    forZones: Union[None, OmitEnum, Sequence[ForZone]] = attr.ib(metadata={'yaml_name': 'forZones'}, converter=optional_list_converter_ForZone, default=OMIT)


class EndpointHintsTypedDict(TypedDict, total=(False)):
    forZones: Sequence[ForZone]


EndpointHintsUnion = Union[EndpointHints, EndpointHintsTypedDict]


@attr.s(kw_only=True)
class EndpointPort(K8sObject):
    appProtocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'appProtocol'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    port: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'port'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)


class EndpointPortTypedDict(TypedDict, total=(False)):
    appProtocol: str
    name: str
    port: int
    protocol: str


EndpointPortUnion = Union[EndpointPort, EndpointPortTypedDict]


@attr.s(kw_only=True)
class ForZone(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class ForZoneTypedDict(TypedDict, total=(True)):
    name: str


ForZoneUnion = Union[ForZone, ForZoneTypedDict]


@attr.s(kw_only=True)
class EndpointSlice(K8sResource):
    apiVersion: ClassVar[str] = 'discovery.k8s.io/v1'
    kind: ClassVar[str] = 'EndpointSlice'
    addressType: str = attr.ib(metadata={'yaml_name': 'addressType'})
    endpoints: Sequence[Endpoint] = attr.ib(metadata={'yaml_name': 'endpoints'}, converter=required_list_converter_Endpoint)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    ports: Union[None, OmitEnum, Sequence[EndpointPort]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_EndpointPort, default=OMIT)
