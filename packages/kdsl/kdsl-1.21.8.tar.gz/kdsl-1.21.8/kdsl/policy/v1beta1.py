from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.policy.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_AllowedCSIDriver(value: Union[Sequence[AllowedCSIDriverUnion], OmitEnum, None]) ->Union[Sequence[AllowedCSIDriver], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedCSIDriver(x) for x in value]


def optional_list_converter_AllowedFlexVolume(value: Union[Sequence[AllowedFlexVolumeUnion], OmitEnum, None]) ->Union[Sequence[AllowedFlexVolume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedFlexVolume(x) for x in value]


def optional_list_converter_AllowedHostPath(value: Union[Sequence[AllowedHostPathUnion], OmitEnum, None]) ->Union[Sequence[AllowedHostPath], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedHostPath(x) for x in value]


def optional_list_converter_HostPortRange(value: Union[Sequence[HostPortRangeUnion], OmitEnum, None]) ->Union[Sequence[HostPortRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HostPortRange(x) for x in value]


def optional_list_converter_IDRange(value: Union[Sequence[IDRangeUnion], OmitEnum, None]) ->Union[Sequence[IDRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IDRange(x) for x in value]


def optional_converter_AllowedCSIDriver(value: Union[AllowedCSIDriverUnion, OmitEnum, None]) ->Union[AllowedCSIDriver, OmitEnum, None]:
    return AllowedCSIDriver(**value) if isinstance(value, dict) else value


def optional_converter_AllowedFlexVolume(value: Union[AllowedFlexVolumeUnion, OmitEnum, None]) ->Union[AllowedFlexVolume, OmitEnum, None]:
    return AllowedFlexVolume(**value) if isinstance(value, dict) else value


def optional_converter_AllowedHostPath(value: Union[AllowedHostPathUnion, OmitEnum, None]) ->Union[AllowedHostPath, OmitEnum, None]:
    return AllowedHostPath(**value) if isinstance(value, dict) else value


def optional_converter_FSGroupStrategyOptions(value: Union[FSGroupStrategyOptionsUnion, OmitEnum, None]) ->Union[FSGroupStrategyOptions, OmitEnum, None]:
    return FSGroupStrategyOptions(**value) if isinstance(value, dict) else value


def optional_converter_HostPortRange(value: Union[HostPortRangeUnion, OmitEnum, None]) ->Union[HostPortRange, OmitEnum, None]:
    return HostPortRange(**value) if isinstance(value, dict) else value


def optional_converter_IDRange(value: Union[IDRangeUnion, OmitEnum, None]) ->Union[IDRange, OmitEnum, None]:
    return IDRange(**value) if isinstance(value, dict) else value


def optional_converter_PodDisruptionBudgetSpec(value: Union[PodDisruptionBudgetSpecUnion, OmitEnum, None]) ->Union[PodDisruptionBudgetSpec, OmitEnum, None]:
    return PodDisruptionBudgetSpec(**value) if isinstance(value, dict) else value


def optional_converter_PodDisruptionBudgetStatus(value: Union[PodDisruptionBudgetStatusUnion, OmitEnum, None]) ->Union[PodDisruptionBudgetStatus, OmitEnum, None]:
    return PodDisruptionBudgetStatus(**value) if isinstance(value, dict) else value


def optional_converter_PodSecurityPolicySpec(value: Union[PodSecurityPolicySpecUnion, OmitEnum, None]) ->Union[PodSecurityPolicySpec, OmitEnum, None]:
    return PodSecurityPolicySpec(**value) if isinstance(value, dict) else value


def optional_converter_RunAsGroupStrategyOptions(value: Union[RunAsGroupStrategyOptionsUnion, OmitEnum, None]) ->Union[RunAsGroupStrategyOptions, OmitEnum, None]:
    return RunAsGroupStrategyOptions(**value) if isinstance(value, dict) else value


def optional_converter_RunAsUserStrategyOptions(value: Union[RunAsUserStrategyOptionsUnion, OmitEnum, None]) ->Union[RunAsUserStrategyOptions, OmitEnum, None]:
    return RunAsUserStrategyOptions(**value) if isinstance(value, dict) else value


def optional_converter_RuntimeClassStrategyOptions(value: Union[RuntimeClassStrategyOptionsUnion, OmitEnum, None]) ->Union[RuntimeClassStrategyOptions, OmitEnum, None]:
    return RuntimeClassStrategyOptions(**value) if isinstance(value, dict) else value


def optional_converter_SELinuxStrategyOptions(value: Union[SELinuxStrategyOptionsUnion, OmitEnum, None]) ->Union[SELinuxStrategyOptions, OmitEnum, None]:
    return SELinuxStrategyOptions(**value) if isinstance(value, dict) else value


def optional_converter_SupplementalGroupsStrategyOptions(value: Union[SupplementalGroupsStrategyOptionsUnion, OmitEnum, None]) ->Union[SupplementalGroupsStrategyOptions, OmitEnum, None]:
    return SupplementalGroupsStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_AllowedCSIDriver(value: AllowedCSIDriverUnion) ->AllowedCSIDriver:
    return AllowedCSIDriver(**value) if isinstance(value, dict) else value


def required_converter_AllowedFlexVolume(value: AllowedFlexVolumeUnion) ->AllowedFlexVolume:
    return AllowedFlexVolume(**value) if isinstance(value, dict) else value


def required_converter_AllowedHostPath(value: AllowedHostPathUnion) ->AllowedHostPath:
    return AllowedHostPath(**value) if isinstance(value, dict) else value


def required_converter_FSGroupStrategyOptions(value: FSGroupStrategyOptionsUnion) ->FSGroupStrategyOptions:
    return FSGroupStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_HostPortRange(value: HostPortRangeUnion) ->HostPortRange:
    return HostPortRange(**value) if isinstance(value, dict) else value


def required_converter_IDRange(value: IDRangeUnion) ->IDRange:
    return IDRange(**value) if isinstance(value, dict) else value


def required_converter_PodDisruptionBudgetSpec(value: PodDisruptionBudgetSpecUnion) ->PodDisruptionBudgetSpec:
    return PodDisruptionBudgetSpec(**value) if isinstance(value, dict) else value


def required_converter_PodDisruptionBudgetStatus(value: PodDisruptionBudgetStatusUnion) ->PodDisruptionBudgetStatus:
    return PodDisruptionBudgetStatus(**value) if isinstance(value, dict) else value


def required_converter_PodSecurityPolicySpec(value: PodSecurityPolicySpecUnion) ->PodSecurityPolicySpec:
    return PodSecurityPolicySpec(**value) if isinstance(value, dict) else value


def required_converter_RunAsGroupStrategyOptions(value: RunAsGroupStrategyOptionsUnion) ->RunAsGroupStrategyOptions:
    return RunAsGroupStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_RunAsUserStrategyOptions(value: RunAsUserStrategyOptionsUnion) ->RunAsUserStrategyOptions:
    return RunAsUserStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_RuntimeClassStrategyOptions(value: RuntimeClassStrategyOptionsUnion) ->RuntimeClassStrategyOptions:
    return RuntimeClassStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_SELinuxStrategyOptions(value: SELinuxStrategyOptionsUnion) ->SELinuxStrategyOptions:
    return SELinuxStrategyOptions(**value) if isinstance(value, dict) else value


def required_converter_SupplementalGroupsStrategyOptions(value: SupplementalGroupsStrategyOptionsUnion) ->SupplementalGroupsStrategyOptions:
    return SupplementalGroupsStrategyOptions(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class AllowedCSIDriver(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class AllowedCSIDriverTypedDict(TypedDict, total=(True)):
    name: str


AllowedCSIDriverUnion = Union[AllowedCSIDriver, AllowedCSIDriverTypedDict]


@attr.s(kw_only=True)
class AllowedFlexVolume(K8sObject):
    driver: str = attr.ib(metadata={'yaml_name': 'driver'})


class AllowedFlexVolumeTypedDict(TypedDict, total=(True)):
    driver: str


AllowedFlexVolumeUnion = Union[AllowedFlexVolume, AllowedFlexVolumeTypedDict]


@attr.s(kw_only=True)
class AllowedHostPath(K8sObject):
    pathPrefix: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'pathPrefix'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class AllowedHostPathTypedDict(TypedDict, total=(False)):
    pathPrefix: str
    readOnly: bool


AllowedHostPathUnion = Union[AllowedHostPath, AllowedHostPathTypedDict]


@attr.s(kw_only=True)
class FSGroupStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[IDRange]] = attr.ib(metadata={'yaml_name': 'ranges'}, converter=optional_list_converter_IDRange, default=OMIT)
    rule: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'rule'}, default=OMIT)


class FSGroupStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[IDRange]
    rule: str


FSGroupStrategyOptionsUnion = Union[FSGroupStrategyOptions, FSGroupStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class HostPortRange(K8sObject):
    max: int = attr.ib(metadata={'yaml_name': 'max'})
    min: int = attr.ib(metadata={'yaml_name': 'min'})


class HostPortRangeTypedDict(TypedDict, total=(True)):
    max: int
    min: int


HostPortRangeUnion = Union[HostPortRange, HostPortRangeTypedDict]


@attr.s(kw_only=True)
class IDRange(K8sObject):
    max: int = attr.ib(metadata={'yaml_name': 'max'})
    min: int = attr.ib(metadata={'yaml_name': 'min'})


class IDRangeTypedDict(TypedDict, total=(True)):
    max: int
    min: int


IDRangeUnion = Union[IDRange, IDRangeTypedDict]


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
class PodSecurityPolicySpec(K8sObject):
    fsGroup: FSGroupStrategyOptions = attr.ib(metadata={'yaml_name': 'fsGroup'}, converter=required_converter_FSGroupStrategyOptions)
    runAsUser: RunAsUserStrategyOptions = attr.ib(metadata={'yaml_name': 'runAsUser'}, converter=required_converter_RunAsUserStrategyOptions)
    seLinux: SELinuxStrategyOptions = attr.ib(metadata={'yaml_name': 'seLinux'}, converter=required_converter_SELinuxStrategyOptions)
    supplementalGroups: SupplementalGroupsStrategyOptions = attr.ib(metadata={'yaml_name': 'supplementalGroups'}, converter=required_converter_SupplementalGroupsStrategyOptions)
    allowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'allowPrivilegeEscalation'}, default=OMIT)
    allowedCSIDrivers: Union[None, OmitEnum, Sequence[AllowedCSIDriver]] = attr.ib(metadata={'yaml_name': 'allowedCSIDrivers'}, converter=optional_list_converter_AllowedCSIDriver, default=OMIT)
    allowedCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'allowedCapabilities'}, default=OMIT)
    allowedFlexVolumes: Union[None, OmitEnum, Sequence[AllowedFlexVolume]] = attr.ib(metadata={'yaml_name': 'allowedFlexVolumes'}, converter=optional_list_converter_AllowedFlexVolume, default=OMIT)
    allowedHostPaths: Union[None, OmitEnum, Sequence[AllowedHostPath]] = attr.ib(metadata={'yaml_name': 'allowedHostPaths'}, converter=optional_list_converter_AllowedHostPath, default=OMIT)
    allowedProcMountTypes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'allowedProcMountTypes'}, default=OMIT)
    allowedUnsafeSysctls: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'allowedUnsafeSysctls'}, default=OMIT)
    defaultAddCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'defaultAddCapabilities'}, default=OMIT)
    defaultAllowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'defaultAllowPrivilegeEscalation'}, default=OMIT)
    forbiddenSysctls: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'forbiddenSysctls'}, default=OMIT)
    hostIPC: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostIPC'}, default=OMIT)
    hostNetwork: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostNetwork'}, default=OMIT)
    hostPID: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostPID'}, default=OMIT)
    hostPorts: Union[None, OmitEnum, Sequence[HostPortRange]] = attr.ib(metadata={'yaml_name': 'hostPorts'}, converter=optional_list_converter_HostPortRange, default=OMIT)
    privileged: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'privileged'}, default=OMIT)
    readOnlyRootFilesystem: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnlyRootFilesystem'}, default=OMIT)
    requiredDropCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'requiredDropCapabilities'}, default=OMIT)
    runAsGroup: Union[None, OmitEnum, RunAsGroupStrategyOptions] = attr.ib(metadata={'yaml_name': 'runAsGroup'}, converter=optional_converter_RunAsGroupStrategyOptions, default=OMIT)
    runtimeClass: Union[None, OmitEnum, RuntimeClassStrategyOptions] = attr.ib(metadata={'yaml_name': 'runtimeClass'}, converter=optional_converter_RuntimeClassStrategyOptions, default=OMIT)
    volumes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'volumes'}, default=OMIT)


class PodSecurityPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    allowPrivilegeEscalation: bool
    allowedCSIDrivers: Sequence[AllowedCSIDriver]
    allowedCapabilities: Sequence[str]
    allowedFlexVolumes: Sequence[AllowedFlexVolume]
    allowedHostPaths: Sequence[AllowedHostPath]
    allowedProcMountTypes: Sequence[str]
    allowedUnsafeSysctls: Sequence[str]
    defaultAddCapabilities: Sequence[str]
    defaultAllowPrivilegeEscalation: bool
    forbiddenSysctls: Sequence[str]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostPorts: Sequence[HostPortRange]
    privileged: bool
    readOnlyRootFilesystem: bool
    requiredDropCapabilities: Sequence[str]
    runAsGroup: RunAsGroupStrategyOptions
    runtimeClass: RuntimeClassStrategyOptions
    volumes: Sequence[str]


class PodSecurityPolicySpecTypedDict(PodSecurityPolicySpecOptionalTypedDict, total=(True)):
    fsGroup: FSGroupStrategyOptions
    runAsUser: RunAsUserStrategyOptions
    seLinux: SELinuxStrategyOptions
    supplementalGroups: SupplementalGroupsStrategyOptions


PodSecurityPolicySpecUnion = Union[PodSecurityPolicySpec, PodSecurityPolicySpecTypedDict]


@attr.s(kw_only=True)
class RunAsGroupStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={'yaml_name': 'rule'})
    ranges: Union[None, OmitEnum, Sequence[IDRange]] = attr.ib(metadata={'yaml_name': 'ranges'}, converter=optional_list_converter_IDRange, default=OMIT)


class RunAsGroupStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[IDRange]


class RunAsGroupStrategyOptionsTypedDict(RunAsGroupStrategyOptionsOptionalTypedDict, total=(True)):
    rule: str


RunAsGroupStrategyOptionsUnion = Union[RunAsGroupStrategyOptions, RunAsGroupStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class RunAsUserStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={'yaml_name': 'rule'})
    ranges: Union[None, OmitEnum, Sequence[IDRange]] = attr.ib(metadata={'yaml_name': 'ranges'}, converter=optional_list_converter_IDRange, default=OMIT)


class RunAsUserStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[IDRange]


class RunAsUserStrategyOptionsTypedDict(RunAsUserStrategyOptionsOptionalTypedDict, total=(True)):
    rule: str


RunAsUserStrategyOptionsUnion = Union[RunAsUserStrategyOptions, RunAsUserStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class RuntimeClassStrategyOptions(K8sObject):
    allowedRuntimeClassNames: Sequence[str] = attr.ib(metadata={'yaml_name': 'allowedRuntimeClassNames'})
    defaultRuntimeClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'defaultRuntimeClassName'}, default=OMIT)


class RuntimeClassStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    defaultRuntimeClassName: str


class RuntimeClassStrategyOptionsTypedDict(RuntimeClassStrategyOptionsOptionalTypedDict, total=(True)):
    allowedRuntimeClassNames: Sequence[str]


RuntimeClassStrategyOptionsUnion = Union[RuntimeClassStrategyOptions, RuntimeClassStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class SELinuxStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={'yaml_name': 'rule'})
    seLinuxOptions: Union[None, OmitEnum, kdsl.core.v1.SELinuxOptions] = attr.ib(metadata={'yaml_name': 'seLinuxOptions'}, converter=kdsl.core.v1.optional_converter_SELinuxOptions, default=OMIT)


class SELinuxStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    seLinuxOptions: kdsl.core.v1.SELinuxOptions


class SELinuxStrategyOptionsTypedDict(SELinuxStrategyOptionsOptionalTypedDict, total=(True)):
    rule: str


SELinuxStrategyOptionsUnion = Union[SELinuxStrategyOptions, SELinuxStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class SupplementalGroupsStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[IDRange]] = attr.ib(metadata={'yaml_name': 'ranges'}, converter=optional_list_converter_IDRange, default=OMIT)
    rule: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'rule'}, default=OMIT)


class SupplementalGroupsStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[IDRange]
    rule: str


SupplementalGroupsStrategyOptionsUnion = Union[SupplementalGroupsStrategyOptions, SupplementalGroupsStrategyOptionsTypedDict]


@attr.s(kw_only=True)
class Eviction(K8sResource):
    apiVersion: ClassVar[str] = 'policy/v1beta1'
    kind: ClassVar[str] = 'Eviction'
    deleteOptions: Union[None, OmitEnum, kdsl.core.v1.DeleteOptions] = attr.ib(metadata={'yaml_name': 'deleteOptions'}, converter=kdsl.core.v1.optional_converter_DeleteOptions, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class PodDisruptionBudget(K8sResource):
    apiVersion: ClassVar[str] = 'policy/v1beta1'
    kind: ClassVar[str] = 'PodDisruptionBudget'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PodDisruptionBudgetSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PodDisruptionBudgetSpec, default=OMIT)
    status: Union[None, OmitEnum, PodDisruptionBudgetStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PodDisruptionBudgetStatus, default=OMIT)


@attr.s(kw_only=True)
class PodSecurityPolicy(K8sResource):
    apiVersion: ClassVar[str] = 'policy/v1beta1'
    kind: ClassVar[str] = 'PodSecurityPolicy'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PodSecurityPolicySpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PodSecurityPolicySpec, default=OMIT)
