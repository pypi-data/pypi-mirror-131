from __future__ import annotations
import kdsl.autoscaling.v2beta1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_list_converter_MetricSpec(value: Union[Sequence[MetricSpecUnion], OmitEnum, None]) ->Union[Sequence[MetricSpec], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricSpec(x) for x in value]


def optional_list_converter_MetricStatus(value: Union[Sequence[MetricStatusUnion], OmitEnum, None]) ->Union[Sequence[MetricStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricStatus(x) for x in value]


def required_list_converter_HorizontalPodAutoscalerCondition(value: Sequence[HorizontalPodAutoscalerConditionUnion]) ->Sequence[HorizontalPodAutoscalerCondition]:
    return [required_converter_HorizontalPodAutoscalerCondition(x) for x in value]


def optional_converter_ContainerResourceMetricSource(value: Union[ContainerResourceMetricSourceUnion, OmitEnum, None]) ->Union[ContainerResourceMetricSource, OmitEnum, None]:
    return ContainerResourceMetricSource(**value) if isinstance(value, dict) else value


def optional_converter_ContainerResourceMetricStatus(value: Union[ContainerResourceMetricStatusUnion, OmitEnum, None]) ->Union[ContainerResourceMetricStatus, OmitEnum, None]:
    return ContainerResourceMetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_CrossVersionObjectReference(value: Union[CrossVersionObjectReferenceUnion, OmitEnum, None]) ->Union[CrossVersionObjectReference, OmitEnum, None]:
    return CrossVersionObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_ExternalMetricSource(value: Union[ExternalMetricSourceUnion, OmitEnum, None]) ->Union[ExternalMetricSource, OmitEnum, None]:
    return ExternalMetricSource(**value) if isinstance(value, dict) else value


def optional_converter_ExternalMetricStatus(value: Union[ExternalMetricStatusUnion, OmitEnum, None]) ->Union[ExternalMetricStatus, OmitEnum, None]:
    return ExternalMetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerCondition(value: Union[HorizontalPodAutoscalerConditionUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerCondition, OmitEnum, None]:
    return HorizontalPodAutoscalerCondition(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerSpec(value: Union[HorizontalPodAutoscalerSpecUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerSpec, OmitEnum, None]:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerStatus(value: Union[HorizontalPodAutoscalerStatusUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerStatus, OmitEnum, None]:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


def optional_converter_MetricSpec(value: Union[MetricSpecUnion, OmitEnum, None]) ->Union[MetricSpec, OmitEnum, None]:
    return MetricSpec(**value) if isinstance(value, dict) else value


def optional_converter_MetricStatus(value: Union[MetricStatusUnion, OmitEnum, None]) ->Union[MetricStatus, OmitEnum, None]:
    return MetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_ObjectMetricSource(value: Union[ObjectMetricSourceUnion, OmitEnum, None]) ->Union[ObjectMetricSource, OmitEnum, None]:
    return ObjectMetricSource(**value) if isinstance(value, dict) else value


def optional_converter_ObjectMetricStatus(value: Union[ObjectMetricStatusUnion, OmitEnum, None]) ->Union[ObjectMetricStatus, OmitEnum, None]:
    return ObjectMetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_PodsMetricSource(value: Union[PodsMetricSourceUnion, OmitEnum, None]) ->Union[PodsMetricSource, OmitEnum, None]:
    return PodsMetricSource(**value) if isinstance(value, dict) else value


def optional_converter_PodsMetricStatus(value: Union[PodsMetricStatusUnion, OmitEnum, None]) ->Union[PodsMetricStatus, OmitEnum, None]:
    return PodsMetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_ResourceMetricSource(value: Union[ResourceMetricSourceUnion, OmitEnum, None]) ->Union[ResourceMetricSource, OmitEnum, None]:
    return ResourceMetricSource(**value) if isinstance(value, dict) else value


def optional_converter_ResourceMetricStatus(value: Union[ResourceMetricStatusUnion, OmitEnum, None]) ->Union[ResourceMetricStatus, OmitEnum, None]:
    return ResourceMetricStatus(**value) if isinstance(value, dict) else value


def required_converter_ContainerResourceMetricSource(value: ContainerResourceMetricSourceUnion) ->ContainerResourceMetricSource:
    return ContainerResourceMetricSource(**value) if isinstance(value, dict) else value


def required_converter_ContainerResourceMetricStatus(value: ContainerResourceMetricStatusUnion) ->ContainerResourceMetricStatus:
    return ContainerResourceMetricStatus(**value) if isinstance(value, dict) else value


def required_converter_CrossVersionObjectReference(value: CrossVersionObjectReferenceUnion) ->CrossVersionObjectReference:
    return CrossVersionObjectReference(**value) if isinstance(value, dict) else value


def required_converter_ExternalMetricSource(value: ExternalMetricSourceUnion) ->ExternalMetricSource:
    return ExternalMetricSource(**value) if isinstance(value, dict) else value


def required_converter_ExternalMetricStatus(value: ExternalMetricStatusUnion) ->ExternalMetricStatus:
    return ExternalMetricStatus(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerCondition(value: HorizontalPodAutoscalerConditionUnion) ->HorizontalPodAutoscalerCondition:
    return HorizontalPodAutoscalerCondition(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerSpec(value: HorizontalPodAutoscalerSpecUnion) ->HorizontalPodAutoscalerSpec:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerStatus(value: HorizontalPodAutoscalerStatusUnion) ->HorizontalPodAutoscalerStatus:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


def required_converter_MetricSpec(value: MetricSpecUnion) ->MetricSpec:
    return MetricSpec(**value) if isinstance(value, dict) else value


def required_converter_MetricStatus(value: MetricStatusUnion) ->MetricStatus:
    return MetricStatus(**value) if isinstance(value, dict) else value


def required_converter_ObjectMetricSource(value: ObjectMetricSourceUnion) ->ObjectMetricSource:
    return ObjectMetricSource(**value) if isinstance(value, dict) else value


def required_converter_ObjectMetricStatus(value: ObjectMetricStatusUnion) ->ObjectMetricStatus:
    return ObjectMetricStatus(**value) if isinstance(value, dict) else value


def required_converter_PodsMetricSource(value: PodsMetricSourceUnion) ->PodsMetricSource:
    return PodsMetricSource(**value) if isinstance(value, dict) else value


def required_converter_PodsMetricStatus(value: PodsMetricStatusUnion) ->PodsMetricStatus:
    return PodsMetricStatus(**value) if isinstance(value, dict) else value


def required_converter_ResourceMetricSource(value: ResourceMetricSourceUnion) ->ResourceMetricSource:
    return ResourceMetricSource(**value) if isinstance(value, dict) else value


def required_converter_ResourceMetricStatus(value: ResourceMetricStatusUnion) ->ResourceMetricStatus:
    return ResourceMetricStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class ContainerResourceMetricSource(K8sObject):
    container: str = attr.ib(metadata={'yaml_name': 'container'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    targetAverageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'targetAverageUtilization'}, default=OMIT)
    targetAverageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'targetAverageValue'}, default=OMIT)


class ContainerResourceMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    targetAverageUtilization: int
    targetAverageValue: str


class ContainerResourceMetricSourceTypedDict(ContainerResourceMetricSourceOptionalTypedDict, total=(True)):
    container: str
    name: str


ContainerResourceMetricSourceUnion = Union[ContainerResourceMetricSource, ContainerResourceMetricSourceTypedDict]


@attr.s(kw_only=True)
class ContainerResourceMetricStatus(K8sObject):
    container: str = attr.ib(metadata={'yaml_name': 'container'})
    currentAverageValue: str = attr.ib(metadata={'yaml_name': 'currentAverageValue'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    currentAverageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'currentAverageUtilization'}, default=OMIT)


class ContainerResourceMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    currentAverageUtilization: int


class ContainerResourceMetricStatusTypedDict(ContainerResourceMetricStatusOptionalTypedDict, total=(True)):
    container: str
    currentAverageValue: str
    name: str


ContainerResourceMetricStatusUnion = Union[ContainerResourceMetricStatus, ContainerResourceMetricStatusTypedDict]


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
class ExternalMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    metricSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'metricSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    targetAverageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'targetAverageValue'}, default=OMIT)
    targetValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'targetValue'}, default=OMIT)


class ExternalMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    metricSelector: kdsl.core.v1.LabelSelector
    targetAverageValue: str
    targetValue: str


class ExternalMetricSourceTypedDict(ExternalMetricSourceOptionalTypedDict, total=(True)):
    metricName: str


ExternalMetricSourceUnion = Union[ExternalMetricSource, ExternalMetricSourceTypedDict]


@attr.s(kw_only=True)
class ExternalMetricStatus(K8sObject):
    currentValue: str = attr.ib(metadata={'yaml_name': 'currentValue'})
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    currentAverageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'currentAverageValue'}, default=OMIT)
    metricSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'metricSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class ExternalMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    currentAverageValue: str
    metricSelector: kdsl.core.v1.LabelSelector


class ExternalMetricStatusTypedDict(ExternalMetricStatusOptionalTypedDict, total=(True)):
    currentValue: str
    metricName: str


ExternalMetricStatusUnion = Union[ExternalMetricStatus, ExternalMetricStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerCondition(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class HorizontalPodAutoscalerConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class HorizontalPodAutoscalerConditionTypedDict(HorizontalPodAutoscalerConditionOptionalTypedDict, total=(True)):
    status: str
    type: str


HorizontalPodAutoscalerConditionUnion = Union[HorizontalPodAutoscalerCondition, HorizontalPodAutoscalerConditionTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerSpec(K8sObject):
    maxReplicas: int = attr.ib(metadata={'yaml_name': 'maxReplicas'})
    scaleTargetRef: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'scaleTargetRef'}, converter=required_converter_CrossVersionObjectReference)
    metrics: Union[None, OmitEnum, Sequence[MetricSpec]] = attr.ib(metadata={'yaml_name': 'metrics'}, converter=optional_list_converter_MetricSpec, default=OMIT)
    minReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReplicas'}, default=OMIT)


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    metrics: Sequence[MetricSpec]
    minReplicas: int


class HorizontalPodAutoscalerSpecTypedDict(HorizontalPodAutoscalerSpecOptionalTypedDict, total=(True)):
    maxReplicas: int
    scaleTargetRef: CrossVersionObjectReference


HorizontalPodAutoscalerSpecUnion = Union[HorizontalPodAutoscalerSpec, HorizontalPodAutoscalerSpecTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerStatus(K8sObject):
    conditions: Sequence[HorizontalPodAutoscalerCondition] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=required_list_converter_HorizontalPodAutoscalerCondition)
    currentReplicas: int = attr.ib(metadata={'yaml_name': 'currentReplicas'})
    desiredReplicas: int = attr.ib(metadata={'yaml_name': 'desiredReplicas'})
    currentMetrics: Union[None, OmitEnum, Sequence[MetricStatus]] = attr.ib(metadata={'yaml_name': 'currentMetrics'}, converter=optional_list_converter_MetricStatus, default=OMIT)
    lastScaleTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastScaleTime'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)


class HorizontalPodAutoscalerStatusOptionalTypedDict(TypedDict, total=(False)):
    currentMetrics: Sequence[MetricStatus]
    lastScaleTime: str
    observedGeneration: int


class HorizontalPodAutoscalerStatusTypedDict(HorizontalPodAutoscalerStatusOptionalTypedDict, total=(True)):
    conditions: Sequence[HorizontalPodAutoscalerCondition]
    currentReplicas: int
    desiredReplicas: int


HorizontalPodAutoscalerStatusUnion = Union[HorizontalPodAutoscalerStatus, HorizontalPodAutoscalerStatusTypedDict]


@attr.s(kw_only=True)
class MetricSpec(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    containerResource: Union[None, OmitEnum, ContainerResourceMetricSource] = attr.ib(metadata={'yaml_name': 'containerResource'}, converter=optional_converter_ContainerResourceMetricSource, default=OMIT)
    external: Union[None, OmitEnum, ExternalMetricSource] = attr.ib(metadata={'yaml_name': 'external'}, converter=optional_converter_ExternalMetricSource, default=OMIT)
    object: Union[None, OmitEnum, ObjectMetricSource] = attr.ib(metadata={'yaml_name': 'object'}, converter=optional_converter_ObjectMetricSource, default=OMIT)
    pods: Union[None, OmitEnum, PodsMetricSource] = attr.ib(metadata={'yaml_name': 'pods'}, converter=optional_converter_PodsMetricSource, default=OMIT)
    resource: Union[None, OmitEnum, ResourceMetricSource] = attr.ib(metadata={'yaml_name': 'resource'}, converter=optional_converter_ResourceMetricSource, default=OMIT)


class MetricSpecOptionalTypedDict(TypedDict, total=(False)):
    containerResource: ContainerResourceMetricSource
    external: ExternalMetricSource
    object: ObjectMetricSource
    pods: PodsMetricSource
    resource: ResourceMetricSource


class MetricSpecTypedDict(MetricSpecOptionalTypedDict, total=(True)):
    type: str


MetricSpecUnion = Union[MetricSpec, MetricSpecTypedDict]


@attr.s(kw_only=True)
class MetricStatus(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    containerResource: Union[None, OmitEnum, ContainerResourceMetricStatus] = attr.ib(metadata={'yaml_name': 'containerResource'}, converter=optional_converter_ContainerResourceMetricStatus, default=OMIT)
    external: Union[None, OmitEnum, ExternalMetricStatus] = attr.ib(metadata={'yaml_name': 'external'}, converter=optional_converter_ExternalMetricStatus, default=OMIT)
    object: Union[None, OmitEnum, ObjectMetricStatus] = attr.ib(metadata={'yaml_name': 'object'}, converter=optional_converter_ObjectMetricStatus, default=OMIT)
    pods: Union[None, OmitEnum, PodsMetricStatus] = attr.ib(metadata={'yaml_name': 'pods'}, converter=optional_converter_PodsMetricStatus, default=OMIT)
    resource: Union[None, OmitEnum, ResourceMetricStatus] = attr.ib(metadata={'yaml_name': 'resource'}, converter=optional_converter_ResourceMetricStatus, default=OMIT)


class MetricStatusOptionalTypedDict(TypedDict, total=(False)):
    containerResource: ContainerResourceMetricStatus
    external: ExternalMetricStatus
    object: ObjectMetricStatus
    pods: PodsMetricStatus
    resource: ResourceMetricStatus


class MetricStatusTypedDict(MetricStatusOptionalTypedDict, total=(True)):
    type: str


MetricStatusUnion = Union[MetricStatus, MetricStatusTypedDict]


@attr.s(kw_only=True)
class ObjectMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    target: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_CrossVersionObjectReference)
    targetValue: str = attr.ib(metadata={'yaml_name': 'targetValue'})
    averageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'averageValue'}, default=OMIT)
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class ObjectMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    averageValue: str
    selector: kdsl.core.v1.LabelSelector


class ObjectMetricSourceTypedDict(ObjectMetricSourceOptionalTypedDict, total=(True)):
    metricName: str
    target: CrossVersionObjectReference
    targetValue: str


ObjectMetricSourceUnion = Union[ObjectMetricSource, ObjectMetricSourceTypedDict]


@attr.s(kw_only=True)
class ObjectMetricStatus(K8sObject):
    currentValue: str = attr.ib(metadata={'yaml_name': 'currentValue'})
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    target: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_CrossVersionObjectReference)
    averageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'averageValue'}, default=OMIT)
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class ObjectMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    averageValue: str
    selector: kdsl.core.v1.LabelSelector


class ObjectMetricStatusTypedDict(ObjectMetricStatusOptionalTypedDict, total=(True)):
    currentValue: str
    metricName: str
    target: CrossVersionObjectReference


ObjectMetricStatusUnion = Union[ObjectMetricStatus, ObjectMetricStatusTypedDict]


@attr.s(kw_only=True)
class PodsMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    targetAverageValue: str = attr.ib(metadata={'yaml_name': 'targetAverageValue'})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class PodsMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class PodsMetricSourceTypedDict(PodsMetricSourceOptionalTypedDict, total=(True)):
    metricName: str
    targetAverageValue: str


PodsMetricSourceUnion = Union[PodsMetricSource, PodsMetricSourceTypedDict]


@attr.s(kw_only=True)
class PodsMetricStatus(K8sObject):
    currentAverageValue: str = attr.ib(metadata={'yaml_name': 'currentAverageValue'})
    metricName: str = attr.ib(metadata={'yaml_name': 'metricName'})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class PodsMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class PodsMetricStatusTypedDict(PodsMetricStatusOptionalTypedDict, total=(True)):
    currentAverageValue: str
    metricName: str


PodsMetricStatusUnion = Union[PodsMetricStatus, PodsMetricStatusTypedDict]


@attr.s(kw_only=True)
class ResourceMetricSource(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    targetAverageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'targetAverageUtilization'}, default=OMIT)
    targetAverageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'targetAverageValue'}, default=OMIT)


class ResourceMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    targetAverageUtilization: int
    targetAverageValue: str


class ResourceMetricSourceTypedDict(ResourceMetricSourceOptionalTypedDict, total=(True)):
    name: str


ResourceMetricSourceUnion = Union[ResourceMetricSource, ResourceMetricSourceTypedDict]


@attr.s(kw_only=True)
class ResourceMetricStatus(K8sObject):
    currentAverageValue: str = attr.ib(metadata={'yaml_name': 'currentAverageValue'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    currentAverageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'currentAverageUtilization'}, default=OMIT)


class ResourceMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    currentAverageUtilization: int


class ResourceMetricStatusTypedDict(ResourceMetricStatusOptionalTypedDict, total=(True)):
    currentAverageValue: str
    name: str


ResourceMetricStatusUnion = Union[ResourceMetricStatus, ResourceMetricStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = 'autoscaling/v2beta1'
    kind: ClassVar[str] = 'HorizontalPodAutoscaler'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, HorizontalPodAutoscalerSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_HorizontalPodAutoscalerSpec, default=OMIT)
    status: Union[None, OmitEnum, HorizontalPodAutoscalerStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_HorizontalPodAutoscalerStatus, default=OMIT)
