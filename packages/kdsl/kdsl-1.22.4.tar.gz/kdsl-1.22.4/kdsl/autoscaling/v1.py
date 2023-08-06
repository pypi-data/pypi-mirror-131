from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.autoscaling.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_converter_CrossVersionObjectReference(value: Union[CrossVersionObjectReferenceUnion, OmitEnum, None]) ->Union[CrossVersionObjectReference, OmitEnum, None]:
    return CrossVersionObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerSpec(value: Union[HorizontalPodAutoscalerSpecUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerSpec, OmitEnum, None]:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerStatus(value: Union[HorizontalPodAutoscalerStatusUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerStatus, OmitEnum, None]:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


def required_converter_CrossVersionObjectReference(value: CrossVersionObjectReferenceUnion) ->CrossVersionObjectReference:
    return CrossVersionObjectReference(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerSpec(value: HorizontalPodAutoscalerSpecUnion) ->HorizontalPodAutoscalerSpec:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerStatus(value: HorizontalPodAutoscalerStatusUnion) ->HorizontalPodAutoscalerStatus:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class CrossVersionObjectReference(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)


class CrossVersionObjectReferenceOptionalTypedDict(TypedDict, total=(False)):
    apiVersion: str


class CrossVersionObjectReferenceTypedDict(CrossVersionObjectReferenceOptionalTypedDict, total=(True)):
    kind: str
    name: str


CrossVersionObjectReferenceUnion = Union[CrossVersionObjectReference, CrossVersionObjectReferenceTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerSpec(K8sObject):
    maxReplicas: int = attr.ib(metadata={'yaml_name': 'maxReplicas'})
    scaleTargetRef: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'scaleTargetRef'}, converter=required_converter_CrossVersionObjectReference)
    minReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReplicas'}, default=OMIT)
    targetCPUUtilizationPercentage: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'targetCPUUtilizationPercentage'}, default=OMIT)


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    minReplicas: int
    targetCPUUtilizationPercentage: int


class HorizontalPodAutoscalerSpecTypedDict(HorizontalPodAutoscalerSpecOptionalTypedDict, total=(True)):
    maxReplicas: int
    scaleTargetRef: CrossVersionObjectReference


HorizontalPodAutoscalerSpecUnion = Union[HorizontalPodAutoscalerSpec, HorizontalPodAutoscalerSpecTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerStatus(K8sObject):
    currentReplicas: int = attr.ib(metadata={'yaml_name': 'currentReplicas'})
    desiredReplicas: int = attr.ib(metadata={'yaml_name': 'desiredReplicas'})
    currentCPUUtilizationPercentage: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'currentCPUUtilizationPercentage'}, default=OMIT)
    lastScaleTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastScaleTime'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)


class HorizontalPodAutoscalerStatusOptionalTypedDict(TypedDict, total=(False)):
    currentCPUUtilizationPercentage: int
    lastScaleTime: str
    observedGeneration: int


class HorizontalPodAutoscalerStatusTypedDict(HorizontalPodAutoscalerStatusOptionalTypedDict, total=(True)):
    currentReplicas: int
    desiredReplicas: int


HorizontalPodAutoscalerStatusUnion = Union[HorizontalPodAutoscalerStatus, HorizontalPodAutoscalerStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = 'autoscaling/v1'
    kind: ClassVar[str] = 'HorizontalPodAutoscaler'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, HorizontalPodAutoscalerSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_HorizontalPodAutoscalerSpec, default=OMIT)
    status: Union[None, OmitEnum, HorizontalPodAutoscalerStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_HorizontalPodAutoscalerStatus, default=OMIT)
