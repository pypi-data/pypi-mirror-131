from __future__ import annotations
import kdsl.node.v1alpha1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Mapping, Literal, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_converter_Overhead(value: Union[OverheadUnion, OmitEnum, None]) ->Union[Overhead, OmitEnum, None]:
    return Overhead(**value) if isinstance(value, dict) else value


def optional_converter_RuntimeClassSpec(value: Union[RuntimeClassSpecUnion, OmitEnum, None]) ->Union[RuntimeClassSpec, OmitEnum, None]:
    return RuntimeClassSpec(**value) if isinstance(value, dict) else value


def optional_converter_Scheduling(value: Union[SchedulingUnion, OmitEnum, None]) ->Union[Scheduling, OmitEnum, None]:
    return Scheduling(**value) if isinstance(value, dict) else value


def required_converter_Overhead(value: OverheadUnion) ->Overhead:
    return Overhead(**value) if isinstance(value, dict) else value


def required_converter_RuntimeClassSpec(value: RuntimeClassSpecUnion) ->RuntimeClassSpec:
    return RuntimeClassSpec(**value) if isinstance(value, dict) else value


def required_converter_Scheduling(value: SchedulingUnion) ->Scheduling:
    return Scheduling(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class Overhead(K8sObject):
    podFixed: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'podFixed'}, default=OMIT)


class OverheadTypedDict(TypedDict, total=(False)):
    podFixed: Mapping[str, str]


OverheadUnion = Union[Overhead, OverheadTypedDict]


@attr.s(kw_only=True)
class RuntimeClassSpec(K8sObject):
    runtimeHandler: str = attr.ib(metadata={'yaml_name': 'runtimeHandler'})
    overhead: Union[None, OmitEnum, Overhead] = attr.ib(metadata={'yaml_name': 'overhead'}, converter=optional_converter_Overhead, default=OMIT)
    scheduling: Union[None, OmitEnum, Scheduling] = attr.ib(metadata={'yaml_name': 'scheduling'}, converter=optional_converter_Scheduling, default=OMIT)


class RuntimeClassSpecOptionalTypedDict(TypedDict, total=(False)):
    overhead: Overhead
    scheduling: Scheduling


class RuntimeClassSpecTypedDict(RuntimeClassSpecOptionalTypedDict, total=(True)):
    runtimeHandler: str


RuntimeClassSpecUnion = Union[RuntimeClassSpec, RuntimeClassSpecTypedDict]


@attr.s(kw_only=True)
class Scheduling(K8sObject):
    nodeSelector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'nodeSelector'}, default=OMIT)
    tolerations: Union[None, OmitEnum, Sequence[kdsl.core.v1.Toleration]] = attr.ib(metadata={'yaml_name': 'tolerations'}, converter=kdsl.core.v1.optional_list_converter_Toleration, default=OMIT)


class SchedulingTypedDict(TypedDict, total=(False)):
    nodeSelector: Mapping[str, str]
    tolerations: Sequence[kdsl.core.v1.Toleration]


SchedulingUnion = Union[Scheduling, SchedulingTypedDict]


@attr.s(kw_only=True)
class RuntimeClass(K8sResource):
    apiVersion: ClassVar[str] = 'node.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'RuntimeClass'
    spec: RuntimeClassSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_RuntimeClassSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
