from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.node.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_converter_Overhead(value: Union[OverheadUnion, OmitEnum, None]) ->Union[Overhead, OmitEnum, None]:
    return Overhead(**value) if isinstance(value, dict) else value


def optional_converter_Scheduling(value: Union[SchedulingUnion, OmitEnum, None]) ->Union[Scheduling, OmitEnum, None]:
    return Scheduling(**value) if isinstance(value, dict) else value


def required_converter_Overhead(value: OverheadUnion) ->Overhead:
    return Overhead(**value) if isinstance(value, dict) else value


def required_converter_Scheduling(value: SchedulingUnion) ->Scheduling:
    return Scheduling(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class Overhead(K8sObject):
    podFixed: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'podFixed'}, default=OMIT)


class OverheadTypedDict(TypedDict, total=(False)):
    podFixed: Mapping[str, str]


OverheadUnion = Union[Overhead, OverheadTypedDict]


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
    apiVersion: ClassVar[str] = 'node.k8s.io/v1beta1'
    kind: ClassVar[str] = 'RuntimeClass'
    handler: str = attr.ib(metadata={'yaml_name': 'handler'})
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    overhead: Union[None, OmitEnum, Overhead] = attr.ib(metadata={'yaml_name': 'overhead'}, converter=optional_converter_Overhead, default=OMIT)
    scheduling: Union[None, OmitEnum, Scheduling] = attr.ib(metadata={'yaml_name': 'scheduling'}, converter=optional_converter_Scheduling, default=OMIT)
