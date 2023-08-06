from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.apps.v1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_mlist_converter_DaemonSetConditionItem(value: Union[Mapping[str, DaemonSetConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, DaemonSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_DaemonSetConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_DeploymentConditionItem(value: Union[Mapping[str, DeploymentConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, DeploymentConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_DeploymentConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_ReplicaSetConditionItem(value: Union[Mapping[str, ReplicaSetConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, ReplicaSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ReplicaSetConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_StatefulSetConditionItem(value: Union[Mapping[str, StatefulSetConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, StatefulSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_StatefulSetConditionItem(v) for k, v in value.items()}


def optional_converter_DaemonSetConditionItem(value: Union[DaemonSetConditionItemUnion, OmitEnum, None]) ->Union[DaemonSetConditionItem, OmitEnum, None]:
    return DaemonSetConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_DaemonSetSpec(value: Union[DaemonSetSpecUnion, OmitEnum, None]) ->Union[DaemonSetSpec, OmitEnum, None]:
    return DaemonSetSpec(**value) if isinstance(value, dict) else value


def optional_converter_DaemonSetStatus(value: Union[DaemonSetStatusUnion, OmitEnum, None]) ->Union[DaemonSetStatus, OmitEnum, None]:
    return DaemonSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_DaemonSetUpdateStrategy(value: Union[DaemonSetUpdateStrategyUnion, OmitEnum, None]) ->Union[DaemonSetUpdateStrategy, OmitEnum, None]:
    return DaemonSetUpdateStrategy(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentConditionItem(value: Union[DeploymentConditionItemUnion, OmitEnum, None]) ->Union[DeploymentConditionItem, OmitEnum, None]:
    return DeploymentConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentSpec(value: Union[DeploymentSpecUnion, OmitEnum, None]) ->Union[DeploymentSpec, OmitEnum, None]:
    return DeploymentSpec(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentStatus(value: Union[DeploymentStatusUnion, OmitEnum, None]) ->Union[DeploymentStatus, OmitEnum, None]:
    return DeploymentStatus(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentStrategy(value: Union[DeploymentStrategyUnion, OmitEnum, None]) ->Union[DeploymentStrategy, OmitEnum, None]:
    return DeploymentStrategy(**value) if isinstance(value, dict) else value


def optional_converter_ReplicaSetConditionItem(value: Union[ReplicaSetConditionItemUnion, OmitEnum, None]) ->Union[ReplicaSetConditionItem, OmitEnum, None]:
    return ReplicaSetConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_ReplicaSetSpec(value: Union[ReplicaSetSpecUnion, OmitEnum, None]) ->Union[ReplicaSetSpec, OmitEnum, None]:
    return ReplicaSetSpec(**value) if isinstance(value, dict) else value


def optional_converter_ReplicaSetStatus(value: Union[ReplicaSetStatusUnion, OmitEnum, None]) ->Union[ReplicaSetStatus, OmitEnum, None]:
    return ReplicaSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_RollingUpdateDaemonSet(value: Union[RollingUpdateDaemonSetUnion, OmitEnum, None]) ->Union[RollingUpdateDaemonSet, OmitEnum, None]:
    return RollingUpdateDaemonSet(**value) if isinstance(value, dict) else value


def optional_converter_RollingUpdateDeployment(value: Union[RollingUpdateDeploymentUnion, OmitEnum, None]) ->Union[RollingUpdateDeployment, OmitEnum, None]:
    return RollingUpdateDeployment(**value) if isinstance(value, dict) else value


def optional_converter_RollingUpdateStatefulSetStrategy(value: Union[RollingUpdateStatefulSetStrategyUnion, OmitEnum, None]) ->Union[RollingUpdateStatefulSetStrategy, OmitEnum, None]:
    return RollingUpdateStatefulSetStrategy(**value) if isinstance(value, dict) else value


def optional_converter_StatefulSetConditionItem(value: Union[StatefulSetConditionItemUnion, OmitEnum, None]) ->Union[StatefulSetConditionItem, OmitEnum, None]:
    return StatefulSetConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_StatefulSetSpec(value: Union[StatefulSetSpecUnion, OmitEnum, None]) ->Union[StatefulSetSpec, OmitEnum, None]:
    return StatefulSetSpec(**value) if isinstance(value, dict) else value


def optional_converter_StatefulSetStatus(value: Union[StatefulSetStatusUnion, OmitEnum, None]) ->Union[StatefulSetStatus, OmitEnum, None]:
    return StatefulSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_StatefulSetUpdateStrategy(value: Union[StatefulSetUpdateStrategyUnion, OmitEnum, None]) ->Union[StatefulSetUpdateStrategy, OmitEnum, None]:
    return StatefulSetUpdateStrategy(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetConditionItem(value: DaemonSetConditionItemUnion) ->DaemonSetConditionItem:
    return DaemonSetConditionItem(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetSpec(value: DaemonSetSpecUnion) ->DaemonSetSpec:
    return DaemonSetSpec(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetStatus(value: DaemonSetStatusUnion) ->DaemonSetStatus:
    return DaemonSetStatus(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetUpdateStrategy(value: DaemonSetUpdateStrategyUnion) ->DaemonSetUpdateStrategy:
    return DaemonSetUpdateStrategy(**value) if isinstance(value, dict) else value


def required_converter_DeploymentConditionItem(value: DeploymentConditionItemUnion) ->DeploymentConditionItem:
    return DeploymentConditionItem(**value) if isinstance(value, dict) else value


def required_converter_DeploymentSpec(value: DeploymentSpecUnion) ->DeploymentSpec:
    return DeploymentSpec(**value) if isinstance(value, dict) else value


def required_converter_DeploymentStatus(value: DeploymentStatusUnion) ->DeploymentStatus:
    return DeploymentStatus(**value) if isinstance(value, dict) else value


def required_converter_DeploymentStrategy(value: DeploymentStrategyUnion) ->DeploymentStrategy:
    return DeploymentStrategy(**value) if isinstance(value, dict) else value


def required_converter_ReplicaSetConditionItem(value: ReplicaSetConditionItemUnion) ->ReplicaSetConditionItem:
    return ReplicaSetConditionItem(**value) if isinstance(value, dict) else value


def required_converter_ReplicaSetSpec(value: ReplicaSetSpecUnion) ->ReplicaSetSpec:
    return ReplicaSetSpec(**value) if isinstance(value, dict) else value


def required_converter_ReplicaSetStatus(value: ReplicaSetStatusUnion) ->ReplicaSetStatus:
    return ReplicaSetStatus(**value) if isinstance(value, dict) else value


def required_converter_RollingUpdateDaemonSet(value: RollingUpdateDaemonSetUnion) ->RollingUpdateDaemonSet:
    return RollingUpdateDaemonSet(**value) if isinstance(value, dict) else value


def required_converter_RollingUpdateDeployment(value: RollingUpdateDeploymentUnion) ->RollingUpdateDeployment:
    return RollingUpdateDeployment(**value) if isinstance(value, dict) else value


def required_converter_RollingUpdateStatefulSetStrategy(value: RollingUpdateStatefulSetStrategyUnion) ->RollingUpdateStatefulSetStrategy:
    return RollingUpdateStatefulSetStrategy(**value) if isinstance(value, dict) else value


def required_converter_StatefulSetConditionItem(value: StatefulSetConditionItemUnion) ->StatefulSetConditionItem:
    return StatefulSetConditionItem(**value) if isinstance(value, dict) else value


def required_converter_StatefulSetSpec(value: StatefulSetSpecUnion) ->StatefulSetSpec:
    return StatefulSetSpec(**value) if isinstance(value, dict) else value


def required_converter_StatefulSetStatus(value: StatefulSetStatusUnion) ->StatefulSetStatus:
    return StatefulSetStatus(**value) if isinstance(value, dict) else value


def required_converter_StatefulSetUpdateStrategy(value: StatefulSetUpdateStrategyUnion) ->StatefulSetUpdateStrategy:
    return StatefulSetUpdateStrategy(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class DaemonSetConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class DaemonSetConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class DaemonSetConditionItemTypedDict(DaemonSetConditionItemOptionalTypedDict, total=(True)):
    status: str


DaemonSetConditionItemUnion = Union[DaemonSetConditionItem, DaemonSetConditionItemTypedDict]


@attr.s(kw_only=True)
class DaemonSetSpec(K8sObject):
    selector: kdsl.core.v1.LabelSelector = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.required_converter_LabelSelector)
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(metadata={'yaml_name': 'template'}, converter=kdsl.core.v1.required_converter_PodTemplateSpec)
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReadySeconds'}, default=OMIT)
    revisionHistoryLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'revisionHistoryLimit'}, default=OMIT)
    updateStrategy: Union[None, OmitEnum, DaemonSetUpdateStrategy] = attr.ib(metadata={'yaml_name': 'updateStrategy'}, converter=optional_converter_DaemonSetUpdateStrategy, default=OMIT)


class DaemonSetSpecOptionalTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    revisionHistoryLimit: int
    updateStrategy: DaemonSetUpdateStrategy


class DaemonSetSpecTypedDict(DaemonSetSpecOptionalTypedDict, total=(True)):
    selector: kdsl.core.v1.LabelSelector
    template: kdsl.core.v1.PodTemplateSpec


DaemonSetSpecUnion = Union[DaemonSetSpec, DaemonSetSpecTypedDict]


@attr.s(kw_only=True)
class DaemonSetStatus(K8sObject):
    currentNumberScheduled: int = attr.ib(metadata={'yaml_name': 'currentNumberScheduled'})
    desiredNumberScheduled: int = attr.ib(metadata={'yaml_name': 'desiredNumberScheduled'})
    numberMisscheduled: int = attr.ib(metadata={'yaml_name': 'numberMisscheduled'})
    numberReady: int = attr.ib(metadata={'yaml_name': 'numberReady'})
    collisionCount: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'collisionCount'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.apps.v1.DaemonSetConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_DaemonSetConditionItem, default=OMIT)
    numberAvailable: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'numberAvailable'}, default=OMIT)
    numberUnavailable: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'numberUnavailable'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)
    updatedNumberScheduled: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'updatedNumberScheduled'}, default=OMIT)


class DaemonSetStatusOptionalTypedDict(TypedDict, total=(False)):
    collisionCount: int
    conditions: Mapping[str, kdsl.apps.v1.DaemonSetConditionItem]
    numberAvailable: int
    numberUnavailable: int
    observedGeneration: int
    updatedNumberScheduled: int


class DaemonSetStatusTypedDict(DaemonSetStatusOptionalTypedDict, total=(True)):
    currentNumberScheduled: int
    desiredNumberScheduled: int
    numberMisscheduled: int
    numberReady: int


DaemonSetStatusUnion = Union[DaemonSetStatus, DaemonSetStatusTypedDict]


@attr.s(kw_only=True)
class DaemonSetUpdateStrategy(K8sObject):
    rollingUpdate: Union[None, OmitEnum, RollingUpdateDaemonSet] = attr.ib(metadata={'yaml_name': 'rollingUpdate'}, converter=optional_converter_RollingUpdateDaemonSet, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class DaemonSetUpdateStrategyTypedDict(TypedDict, total=(False)):
    rollingUpdate: RollingUpdateDaemonSet
    type: str


DaemonSetUpdateStrategyUnion = Union[DaemonSetUpdateStrategy, DaemonSetUpdateStrategyTypedDict]


@attr.s(kw_only=True)
class DeploymentConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    lastUpdateTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastUpdateTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class DeploymentConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    lastUpdateTime: str
    message: str
    reason: str


class DeploymentConditionItemTypedDict(DeploymentConditionItemOptionalTypedDict, total=(True)):
    status: str


DeploymentConditionItemUnion = Union[DeploymentConditionItem, DeploymentConditionItemTypedDict]


@attr.s(kw_only=True)
class DeploymentSpec(K8sObject):
    selector: kdsl.core.v1.LabelSelector = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.required_converter_LabelSelector)
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(metadata={'yaml_name': 'template'}, converter=kdsl.core.v1.required_converter_PodTemplateSpec)
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReadySeconds'}, default=OMIT)
    paused: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'paused'}, default=OMIT)
    progressDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'progressDeadlineSeconds'}, default=OMIT)
    replicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'replicas'}, default=OMIT)
    revisionHistoryLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'revisionHistoryLimit'}, default=OMIT)
    strategy: Union[None, OmitEnum, DeploymentStrategy] = attr.ib(metadata={'yaml_name': 'strategy'}, converter=optional_converter_DeploymentStrategy, default=OMIT)


class DeploymentSpecOptionalTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    paused: bool
    progressDeadlineSeconds: int
    replicas: int
    revisionHistoryLimit: int
    strategy: DeploymentStrategy


class DeploymentSpecTypedDict(DeploymentSpecOptionalTypedDict, total=(True)):
    selector: kdsl.core.v1.LabelSelector
    template: kdsl.core.v1.PodTemplateSpec


DeploymentSpecUnion = Union[DeploymentSpec, DeploymentSpecTypedDict]


@attr.s(kw_only=True)
class DeploymentStatus(K8sObject):
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'availableReplicas'}, default=OMIT)
    collisionCount: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'collisionCount'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.apps.v1.DeploymentConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_DeploymentConditionItem, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'readyReplicas'}, default=OMIT)
    replicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'replicas'}, default=OMIT)
    unavailableReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'unavailableReplicas'}, default=OMIT)
    updatedReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'updatedReplicas'}, default=OMIT)


class DeploymentStatusTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    collisionCount: int
    conditions: Mapping[str, kdsl.apps.v1.DeploymentConditionItem]
    observedGeneration: int
    readyReplicas: int
    replicas: int
    unavailableReplicas: int
    updatedReplicas: int


DeploymentStatusUnion = Union[DeploymentStatus, DeploymentStatusTypedDict]


@attr.s(kw_only=True)
class DeploymentStrategy(K8sObject):
    rollingUpdate: Union[None, OmitEnum, RollingUpdateDeployment] = attr.ib(metadata={'yaml_name': 'rollingUpdate'}, converter=optional_converter_RollingUpdateDeployment, default=OMIT)
    type: Union[None, OmitEnum, Literal['Recreate', 'RollingUpdate']] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class DeploymentStrategyTypedDict(TypedDict, total=(False)):
    rollingUpdate: RollingUpdateDeployment
    type: Literal['Recreate', 'RollingUpdate']


DeploymentStrategyUnion = Union[DeploymentStrategy, DeploymentStrategyTypedDict]


@attr.s(kw_only=True)
class ReplicaSetConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class ReplicaSetConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class ReplicaSetConditionItemTypedDict(ReplicaSetConditionItemOptionalTypedDict, total=(True)):
    status: str


ReplicaSetConditionItemUnion = Union[ReplicaSetConditionItem, ReplicaSetConditionItemTypedDict]


@attr.s(kw_only=True)
class ReplicaSetSpec(K8sObject):
    selector: kdsl.core.v1.LabelSelector = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.required_converter_LabelSelector)
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReadySeconds'}, default=OMIT)
    replicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'replicas'}, default=OMIT)
    template: Union[None, OmitEnum, kdsl.core.v1.PodTemplateSpec] = attr.ib(metadata={'yaml_name': 'template'}, converter=kdsl.core.v1.optional_converter_PodTemplateSpec, default=OMIT)


class ReplicaSetSpecOptionalTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    replicas: int
    template: kdsl.core.v1.PodTemplateSpec


class ReplicaSetSpecTypedDict(ReplicaSetSpecOptionalTypedDict, total=(True)):
    selector: kdsl.core.v1.LabelSelector


ReplicaSetSpecUnion = Union[ReplicaSetSpec, ReplicaSetSpecTypedDict]


@attr.s(kw_only=True)
class ReplicaSetStatus(K8sObject):
    replicas: int = attr.ib(metadata={'yaml_name': 'replicas'})
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'availableReplicas'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.apps.v1.ReplicaSetConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_ReplicaSetConditionItem, default=OMIT)
    fullyLabeledReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'fullyLabeledReplicas'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'readyReplicas'}, default=OMIT)


class ReplicaSetStatusOptionalTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    conditions: Mapping[str, kdsl.apps.v1.ReplicaSetConditionItem]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int


class ReplicaSetStatusTypedDict(ReplicaSetStatusOptionalTypedDict, total=(True)):
    replicas: int


ReplicaSetStatusUnion = Union[ReplicaSetStatus, ReplicaSetStatusTypedDict]


@attr.s(kw_only=True)
class RollingUpdateDaemonSet(K8sObject):
    maxSurge: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'maxSurge'}, default=OMIT)
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'maxUnavailable'}, default=OMIT)


class RollingUpdateDaemonSetTypedDict(TypedDict, total=(False)):
    maxSurge: Union[int, str]
    maxUnavailable: Union[int, str]


RollingUpdateDaemonSetUnion = Union[RollingUpdateDaemonSet, RollingUpdateDaemonSetTypedDict]


@attr.s(kw_only=True)
class RollingUpdateDeployment(K8sObject):
    maxSurge: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'maxSurge'}, default=OMIT)
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'maxUnavailable'}, default=OMIT)


class RollingUpdateDeploymentTypedDict(TypedDict, total=(False)):
    maxSurge: Union[int, str]
    maxUnavailable: Union[int, str]


RollingUpdateDeploymentUnion = Union[RollingUpdateDeployment, RollingUpdateDeploymentTypedDict]


@attr.s(kw_only=True)
class RollingUpdateStatefulSetStrategy(K8sObject):
    partition: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'partition'}, default=OMIT)


class RollingUpdateStatefulSetStrategyTypedDict(TypedDict, total=(False)):
    partition: int


RollingUpdateStatefulSetStrategyUnion = Union[RollingUpdateStatefulSetStrategy, RollingUpdateStatefulSetStrategyTypedDict]


@attr.s(kw_only=True)
class StatefulSetConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class StatefulSetConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class StatefulSetConditionItemTypedDict(StatefulSetConditionItemOptionalTypedDict, total=(True)):
    status: str


StatefulSetConditionItemUnion = Union[StatefulSetConditionItem, StatefulSetConditionItemTypedDict]


@attr.s(kw_only=True)
class StatefulSetSpec(K8sObject):
    selector: kdsl.core.v1.LabelSelector = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.required_converter_LabelSelector)
    serviceName: str = attr.ib(metadata={'yaml_name': 'serviceName'})
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(metadata={'yaml_name': 'template'}, converter=kdsl.core.v1.required_converter_PodTemplateSpec)
    podManagementPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'podManagementPolicy'}, default=OMIT)
    replicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'replicas'}, default=OMIT)
    revisionHistoryLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'revisionHistoryLimit'}, default=OMIT)
    updateStrategy: Union[None, OmitEnum, StatefulSetUpdateStrategy] = attr.ib(metadata={'yaml_name': 'updateStrategy'}, converter=optional_converter_StatefulSetUpdateStrategy, default=OMIT)
    volumeClaimTemplates: Union[None, OmitEnum, Sequence[kdsl.core.v1.EmbeddedPersistentVolumeClaim]] = attr.ib(metadata={'yaml_name': 'volumeClaimTemplates'}, converter=kdsl.core.v1.optional_list_converter_EmbeddedPersistentVolumeClaim, default=OMIT)


class StatefulSetSpecOptionalTypedDict(TypedDict, total=(False)):
    podManagementPolicy: str
    replicas: int
    revisionHistoryLimit: int
    updateStrategy: StatefulSetUpdateStrategy
    volumeClaimTemplates: Sequence[kdsl.core.v1.EmbeddedPersistentVolumeClaim]


class StatefulSetSpecTypedDict(StatefulSetSpecOptionalTypedDict, total=(True)):
    selector: kdsl.core.v1.LabelSelector
    serviceName: str
    template: kdsl.core.v1.PodTemplateSpec


StatefulSetSpecUnion = Union[StatefulSetSpec, StatefulSetSpecTypedDict]


@attr.s(kw_only=True)
class StatefulSetStatus(K8sObject):
    replicas: int = attr.ib(metadata={'yaml_name': 'replicas'})
    collisionCount: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'collisionCount'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.apps.v1.StatefulSetConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_StatefulSetConditionItem, default=OMIT)
    currentReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'currentReplicas'}, default=OMIT)
    currentRevision: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'currentRevision'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'readyReplicas'}, default=OMIT)
    updateRevision: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'updateRevision'}, default=OMIT)
    updatedReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'updatedReplicas'}, default=OMIT)


class StatefulSetStatusOptionalTypedDict(TypedDict, total=(False)):
    collisionCount: int
    conditions: Mapping[str, kdsl.apps.v1.StatefulSetConditionItem]
    currentReplicas: int
    currentRevision: str
    observedGeneration: int
    readyReplicas: int
    updateRevision: str
    updatedReplicas: int


class StatefulSetStatusTypedDict(StatefulSetStatusOptionalTypedDict, total=(True)):
    replicas: int


StatefulSetStatusUnion = Union[StatefulSetStatus, StatefulSetStatusTypedDict]


@attr.s(kw_only=True)
class StatefulSetUpdateStrategy(K8sObject):
    rollingUpdate: Union[None, OmitEnum, RollingUpdateStatefulSetStrategy] = attr.ib(metadata={'yaml_name': 'rollingUpdate'}, converter=optional_converter_RollingUpdateStatefulSetStrategy, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class StatefulSetUpdateStrategyTypedDict(TypedDict, total=(False)):
    rollingUpdate: RollingUpdateStatefulSetStrategy
    type: str


StatefulSetUpdateStrategyUnion = Union[StatefulSetUpdateStrategy, StatefulSetUpdateStrategyTypedDict]


@attr.s(kw_only=True)
class ControllerRevision(K8sResource):
    apiVersion: ClassVar[str] = 'apps/v1'
    kind: ClassVar[str] = 'ControllerRevision'
    revision: int = attr.ib(metadata={'yaml_name': 'revision'})
    data: Union[None, OmitEnum, Mapping[str, Any]] = attr.ib(metadata={'yaml_name': 'data'}, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class DaemonSet(K8sResource):
    apiVersion: ClassVar[str] = 'apps/v1'
    kind: ClassVar[str] = 'DaemonSet'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, DaemonSetSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_DaemonSetSpec, default=OMIT)
    status: Union[None, OmitEnum, DaemonSetStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_DaemonSetStatus, default=OMIT)


@attr.s(kw_only=True)
class Deployment(K8sResource):
    apiVersion: ClassVar[str] = 'apps/v1'
    kind: ClassVar[str] = 'Deployment'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, DeploymentSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_DeploymentSpec, default=OMIT)
    status: Union[None, OmitEnum, DeploymentStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_DeploymentStatus, default=OMIT)


@attr.s(kw_only=True)
class ReplicaSet(K8sResource):
    apiVersion: ClassVar[str] = 'apps/v1'
    kind: ClassVar[str] = 'ReplicaSet'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, ReplicaSetSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_ReplicaSetSpec, default=OMIT)
    status: Union[None, OmitEnum, ReplicaSetStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_ReplicaSetStatus, default=OMIT)


@attr.s(kw_only=True)
class StatefulSet(K8sResource):
    apiVersion: ClassVar[str] = 'apps/v1'
    kind: ClassVar[str] = 'StatefulSet'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, StatefulSetSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_StatefulSetSpec, default=OMIT)
    status: Union[None, OmitEnum, StatefulSetStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_StatefulSetStatus, default=OMIT)
