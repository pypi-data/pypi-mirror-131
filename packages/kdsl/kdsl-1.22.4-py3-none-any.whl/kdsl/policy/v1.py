from __future__ import annotations
import kdsl.policy.v1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Mapping, Literal, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_converter_PodDisruptionBudgetSpec(value: Union[PodDisruptionBudgetSpecUnion, OmitEnum, None]) ->Union[PodDisruptionBudgetSpec, OmitEnum, None]:
    return PodDisruptionBudgetSpec(**value) if isinstance(value, dict) else value


def optional_converter_PodDisruptionBudgetStatus(value: Union[PodDisruptionBudgetStatusUnion, OmitEnum, None]) ->Union[PodDisruptionBudgetStatus, OmitEnum, None]:
    return PodDisruptionBudgetStatus(**value) if isinstance(value, dict) else value


def required_converter_PodDisruptionBudgetSpec(value: PodDisruptionBudgetSpecUnion) ->PodDisruptionBudgetSpec:
    return PodDisruptionBudgetSpec(**value) if isinstance(value, dict) else value


def required_converter_PodDisruptionBudgetStatus(value: PodDisruptionBudgetStatusUnion) ->PodDisruptionBudgetStatus:
    return PodDisruptionBudgetStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class PodDisruptionBudgetSpec(K8sObject):
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'maxUnavailable'}, default=OMIT)
    minAvailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'minAvailable'}, default=OMIT)
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class PodDisruptionBudgetSpecTypedDict(TypedDict, total=(False)):
    maxUnavailable: Union[int, str]
    minAvailable: Union[int, str]
    selector: kdsl.core.v1.LabelSelector


PodDisruptionBudgetSpecUnion = Union[PodDisruptionBudgetSpec, PodDisruptionBudgetSpecTypedDict]


@attr.s(kw_only=True)
class PodDisruptionBudgetStatus(K8sObject):
    currentHealthy: int = attr.ib(metadata={'yaml_name': 'currentHealthy'})
    desiredHealthy: int = attr.ib(metadata={'yaml_name': 'desiredHealthy'})
    disruptionsAllowed: int = attr.ib(metadata={'yaml_name': 'disruptionsAllowed'})
    expectedPods: int = attr.ib(metadata={'yaml_name': 'expectedPods'})
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.ConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=kdsl.core.v1.optional_mlist_converter_ConditionItem, default=OMIT)
    disruptedPods: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'disruptedPods'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)


class PodDisruptionBudgetStatusOptionalTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.ConditionItem]
    disruptedPods: Mapping[str, str]
    observedGeneration: int


class PodDisruptionBudgetStatusTypedDict(PodDisruptionBudgetStatusOptionalTypedDict, total=(True)):
    currentHealthy: int
    desiredHealthy: int
    disruptionsAllowed: int
    expectedPods: int


PodDisruptionBudgetStatusUnion = Union[PodDisruptionBudgetStatus, PodDisruptionBudgetStatusTypedDict]


@attr.s(kw_only=True)
class Eviction(K8sResource):
    apiVersion: ClassVar[str] = 'policy/v1'
    kind: ClassVar[str] = 'Eviction'
    deleteOptions: Union[None, OmitEnum, kdsl.core.v1.DeleteOptions] = attr.ib(metadata={'yaml_name': 'deleteOptions'}, converter=kdsl.core.v1.optional_converter_DeleteOptions, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class PodDisruptionBudget(K8sResource):
    apiVersion: ClassVar[str] = 'policy/v1'
    kind: ClassVar[str] = 'PodDisruptionBudget'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PodDisruptionBudgetSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PodDisruptionBudgetSpec, default=OMIT)
    status: Union[None, OmitEnum, PodDisruptionBudgetStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PodDisruptionBudgetStatus, default=OMIT)
