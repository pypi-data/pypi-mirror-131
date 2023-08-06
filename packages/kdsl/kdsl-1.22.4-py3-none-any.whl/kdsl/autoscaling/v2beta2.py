from __future__ import annotations
import kdsl.autoscaling.v2beta2
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_list_converter_HPAScalingPolicy(value: Union[Sequence[HPAScalingPolicyUnion], OmitEnum, None]) ->Union[Sequence[HPAScalingPolicy], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HPAScalingPolicy(x) for x in value]


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


def optional_converter_HPAScalingPolicy(value: Union[HPAScalingPolicyUnion, OmitEnum, None]) ->Union[HPAScalingPolicy, OmitEnum, None]:
    return HPAScalingPolicy(**value) if isinstance(value, dict) else value


def optional_converter_HPAScalingRules(value: Union[HPAScalingRulesUnion, OmitEnum, None]) ->Union[HPAScalingRules, OmitEnum, None]:
    return HPAScalingRules(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerBehavior(value: Union[HorizontalPodAutoscalerBehaviorUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerBehavior, OmitEnum, None]:
    return HorizontalPodAutoscalerBehavior(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerCondition(value: Union[HorizontalPodAutoscalerConditionUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerCondition, OmitEnum, None]:
    return HorizontalPodAutoscalerCondition(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerSpec(value: Union[HorizontalPodAutoscalerSpecUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerSpec, OmitEnum, None]:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def optional_converter_HorizontalPodAutoscalerStatus(value: Union[HorizontalPodAutoscalerStatusUnion, OmitEnum, None]) ->Union[HorizontalPodAutoscalerStatus, OmitEnum, None]:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


def optional_converter_MetricIdentifier(value: Union[MetricIdentifierUnion, OmitEnum, None]) ->Union[MetricIdentifier, OmitEnum, None]:
    return MetricIdentifier(**value) if isinstance(value, dict) else value


def optional_converter_MetricSpec(value: Union[MetricSpecUnion, OmitEnum, None]) ->Union[MetricSpec, OmitEnum, None]:
    return MetricSpec(**value) if isinstance(value, dict) else value


def optional_converter_MetricStatus(value: Union[MetricStatusUnion, OmitEnum, None]) ->Union[MetricStatus, OmitEnum, None]:
    return MetricStatus(**value) if isinstance(value, dict) else value


def optional_converter_MetricTarget(value: Union[MetricTargetUnion, OmitEnum, None]) ->Union[MetricTarget, OmitEnum, None]:
    return MetricTarget(**value) if isinstance(value, dict) else value


def optional_converter_MetricValueStatus(value: Union[MetricValueStatusUnion, OmitEnum, None]) ->Union[MetricValueStatus, OmitEnum, None]:
    return MetricValueStatus(**value) if isinstance(value, dict) else value


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


def required_converter_HPAScalingPolicy(value: HPAScalingPolicyUnion) ->HPAScalingPolicy:
    return HPAScalingPolicy(**value) if isinstance(value, dict) else value


def required_converter_HPAScalingRules(value: HPAScalingRulesUnion) ->HPAScalingRules:
    return HPAScalingRules(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerBehavior(value: HorizontalPodAutoscalerBehaviorUnion) ->HorizontalPodAutoscalerBehavior:
    return HorizontalPodAutoscalerBehavior(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerCondition(value: HorizontalPodAutoscalerConditionUnion) ->HorizontalPodAutoscalerCondition:
    return HorizontalPodAutoscalerCondition(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerSpec(value: HorizontalPodAutoscalerSpecUnion) ->HorizontalPodAutoscalerSpec:
    return HorizontalPodAutoscalerSpec(**value) if isinstance(value, dict) else value


def required_converter_HorizontalPodAutoscalerStatus(value: HorizontalPodAutoscalerStatusUnion) ->HorizontalPodAutoscalerStatus:
    return HorizontalPodAutoscalerStatus(**value) if isinstance(value, dict) else value


def required_converter_MetricIdentifier(value: MetricIdentifierUnion) ->MetricIdentifier:
    return MetricIdentifier(**value) if isinstance(value, dict) else value


def required_converter_MetricSpec(value: MetricSpecUnion) ->MetricSpec:
    return MetricSpec(**value) if isinstance(value, dict) else value


def required_converter_MetricStatus(value: MetricStatusUnion) ->MetricStatus:
    return MetricStatus(**value) if isinstance(value, dict) else value


def required_converter_MetricTarget(value: MetricTargetUnion) ->MetricTarget:
    return MetricTarget(**value) if isinstance(value, dict) else value


def required_converter_MetricValueStatus(value: MetricValueStatusUnion) ->MetricValueStatus:
    return MetricValueStatus(**value) if isinstance(value, dict) else value


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
    target: MetricTarget = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_MetricTarget)


class ContainerResourceMetricSourceTypedDict(TypedDict, total=(True)):
    container: str
    name: str
    target: MetricTarget


ContainerResourceMetricSourceUnion = Union[ContainerResourceMetricSource, ContainerResourceMetricSourceTypedDict]


@attr.s(kw_only=True)
class ContainerResourceMetricStatus(K8sObject):
    container: str = attr.ib(metadata={'yaml_name': 'container'})
    current: MetricValueStatus = attr.ib(metadata={'yaml_name': 'current'}, converter=required_converter_MetricValueStatus)
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class ContainerResourceMetricStatusTypedDict(TypedDict, total=(True)):
    container: str
    current: MetricValueStatus
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
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)
    target: MetricTarget = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_MetricTarget)


class ExternalMetricSourceTypedDict(TypedDict, total=(True)):
    metric: MetricIdentifier
    target: MetricTarget


ExternalMetricSourceUnion = Union[ExternalMetricSource, ExternalMetricSourceTypedDict]


@attr.s(kw_only=True)
class ExternalMetricStatus(K8sObject):
    current: MetricValueStatus = attr.ib(metadata={'yaml_name': 'current'}, converter=required_converter_MetricValueStatus)
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)


class ExternalMetricStatusTypedDict(TypedDict, total=(True)):
    current: MetricValueStatus
    metric: MetricIdentifier


ExternalMetricStatusUnion = Union[ExternalMetricStatus, ExternalMetricStatusTypedDict]


@attr.s(kw_only=True)
class HPAScalingPolicy(K8sObject):
    periodSeconds: int = attr.ib(metadata={'yaml_name': 'periodSeconds'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    value: int = attr.ib(metadata={'yaml_name': 'value'})


class HPAScalingPolicyTypedDict(TypedDict, total=(True)):
    periodSeconds: int
    type: str
    value: int


HPAScalingPolicyUnion = Union[HPAScalingPolicy, HPAScalingPolicyTypedDict]


@attr.s(kw_only=True)
class HPAScalingRules(K8sObject):
    policies: Union[None, OmitEnum, Sequence[HPAScalingPolicy]] = attr.ib(metadata={'yaml_name': 'policies'}, converter=optional_list_converter_HPAScalingPolicy, default=OMIT)
    selectPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'selectPolicy'}, default=OMIT)
    stabilizationWindowSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'stabilizationWindowSeconds'}, default=OMIT)


class HPAScalingRulesTypedDict(TypedDict, total=(False)):
    policies: Sequence[HPAScalingPolicy]
    selectPolicy: str
    stabilizationWindowSeconds: int


HPAScalingRulesUnion = Union[HPAScalingRules, HPAScalingRulesTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerBehavior(K8sObject):
    scaleDown: Union[None, OmitEnum, HPAScalingRules] = attr.ib(metadata={'yaml_name': 'scaleDown'}, converter=optional_converter_HPAScalingRules, default=OMIT)
    scaleUp: Union[None, OmitEnum, HPAScalingRules] = attr.ib(metadata={'yaml_name': 'scaleUp'}, converter=optional_converter_HPAScalingRules, default=OMIT)


class HorizontalPodAutoscalerBehaviorTypedDict(TypedDict, total=(False)):
    scaleDown: HPAScalingRules
    scaleUp: HPAScalingRules


HorizontalPodAutoscalerBehaviorUnion = Union[HorizontalPodAutoscalerBehavior, HorizontalPodAutoscalerBehaviorTypedDict]


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
    behavior: Union[None, OmitEnum, HorizontalPodAutoscalerBehavior] = attr.ib(metadata={'yaml_name': 'behavior'}, converter=optional_converter_HorizontalPodAutoscalerBehavior, default=OMIT)
    metrics: Union[None, OmitEnum, Sequence[MetricSpec]] = attr.ib(metadata={'yaml_name': 'metrics'}, converter=optional_list_converter_MetricSpec, default=OMIT)
    minReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReplicas'}, default=OMIT)


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    behavior: HorizontalPodAutoscalerBehavior
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
class MetricIdentifier(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


class MetricIdentifierOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class MetricIdentifierTypedDict(MetricIdentifierOptionalTypedDict, total=(True)):
    name: str


MetricIdentifierUnion = Union[MetricIdentifier, MetricIdentifierTypedDict]


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
class MetricTarget(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    averageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'averageUtilization'}, default=OMIT)
    averageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'averageValue'}, default=OMIT)
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)


class MetricTargetOptionalTypedDict(TypedDict, total=(False)):
    averageUtilization: int
    averageValue: str
    value: str


class MetricTargetTypedDict(MetricTargetOptionalTypedDict, total=(True)):
    type: str


MetricTargetUnion = Union[MetricTarget, MetricTargetTypedDict]


@attr.s(kw_only=True)
class MetricValueStatus(K8sObject):
    averageUtilization: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'averageUtilization'}, default=OMIT)
    averageValue: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'averageValue'}, default=OMIT)
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)


class MetricValueStatusTypedDict(TypedDict, total=(False)):
    averageUtilization: int
    averageValue: str
    value: str


MetricValueStatusUnion = Union[MetricValueStatus, MetricValueStatusTypedDict]


@attr.s(kw_only=True)
class ObjectMetricSource(K8sObject):
    describedObject: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'describedObject'}, converter=required_converter_CrossVersionObjectReference)
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)
    target: MetricTarget = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_MetricTarget)


class ObjectMetricSourceTypedDict(TypedDict, total=(True)):
    describedObject: CrossVersionObjectReference
    metric: MetricIdentifier
    target: MetricTarget


ObjectMetricSourceUnion = Union[ObjectMetricSource, ObjectMetricSourceTypedDict]


@attr.s(kw_only=True)
class ObjectMetricStatus(K8sObject):
    current: MetricValueStatus = attr.ib(metadata={'yaml_name': 'current'}, converter=required_converter_MetricValueStatus)
    describedObject: CrossVersionObjectReference = attr.ib(metadata={'yaml_name': 'describedObject'}, converter=required_converter_CrossVersionObjectReference)
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)


class ObjectMetricStatusTypedDict(TypedDict, total=(True)):
    current: MetricValueStatus
    describedObject: CrossVersionObjectReference
    metric: MetricIdentifier


ObjectMetricStatusUnion = Union[ObjectMetricStatus, ObjectMetricStatusTypedDict]


@attr.s(kw_only=True)
class PodsMetricSource(K8sObject):
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)
    target: MetricTarget = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_MetricTarget)


class PodsMetricSourceTypedDict(TypedDict, total=(True)):
    metric: MetricIdentifier
    target: MetricTarget


PodsMetricSourceUnion = Union[PodsMetricSource, PodsMetricSourceTypedDict]


@attr.s(kw_only=True)
class PodsMetricStatus(K8sObject):
    current: MetricValueStatus = attr.ib(metadata={'yaml_name': 'current'}, converter=required_converter_MetricValueStatus)
    metric: MetricIdentifier = attr.ib(metadata={'yaml_name': 'metric'}, converter=required_converter_MetricIdentifier)


class PodsMetricStatusTypedDict(TypedDict, total=(True)):
    current: MetricValueStatus
    metric: MetricIdentifier


PodsMetricStatusUnion = Union[PodsMetricStatus, PodsMetricStatusTypedDict]


@attr.s(kw_only=True)
class ResourceMetricSource(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    target: MetricTarget = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_MetricTarget)


class ResourceMetricSourceTypedDict(TypedDict, total=(True)):
    name: str
    target: MetricTarget


ResourceMetricSourceUnion = Union[ResourceMetricSource, ResourceMetricSourceTypedDict]


@attr.s(kw_only=True)
class ResourceMetricStatus(K8sObject):
    current: MetricValueStatus = attr.ib(metadata={'yaml_name': 'current'}, converter=required_converter_MetricValueStatus)
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class ResourceMetricStatusTypedDict(TypedDict, total=(True)):
    current: MetricValueStatus
    name: str


ResourceMetricStatusUnion = Union[ResourceMetricStatus, ResourceMetricStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = 'autoscaling/v2beta2'
    kind: ClassVar[str] = 'HorizontalPodAutoscaler'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, HorizontalPodAutoscalerSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_HorizontalPodAutoscalerSpec, default=OMIT)
    status: Union[None, OmitEnum, HorizontalPodAutoscalerStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_HorizontalPodAutoscalerStatus, default=OMIT)
