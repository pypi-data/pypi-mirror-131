from __future__ import annotations
import kdsl.batch.v1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_mlist_converter_JobConditionItem(value: Union[Mapping[str, JobConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, JobConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_JobConditionItem(v) for k, v in value.items()}


def optional_converter_CronJobSpec(value: Union[CronJobSpecUnion, OmitEnum, None]) ->Union[CronJobSpec, OmitEnum, None]:
    return CronJobSpec(**value) if isinstance(value, dict) else value


def optional_converter_CronJobStatus(value: Union[CronJobStatusUnion, OmitEnum, None]) ->Union[CronJobStatus, OmitEnum, None]:
    return CronJobStatus(**value) if isinstance(value, dict) else value


def optional_converter_JobConditionItem(value: Union[JobConditionItemUnion, OmitEnum, None]) ->Union[JobConditionItem, OmitEnum, None]:
    return JobConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_JobSpec(value: Union[JobSpecUnion, OmitEnum, None]) ->Union[JobSpec, OmitEnum, None]:
    return JobSpec(**value) if isinstance(value, dict) else value


def optional_converter_JobStatus(value: Union[JobStatusUnion, OmitEnum, None]) ->Union[JobStatus, OmitEnum, None]:
    return JobStatus(**value) if isinstance(value, dict) else value


def optional_converter_JobTemplateSpec(value: Union[JobTemplateSpecUnion, OmitEnum, None]) ->Union[JobTemplateSpec, OmitEnum, None]:
    return JobTemplateSpec(**value) if isinstance(value, dict) else value


def optional_converter_UncountedTerminatedPods(value: Union[UncountedTerminatedPodsUnion, OmitEnum, None]) ->Union[UncountedTerminatedPods, OmitEnum, None]:
    return UncountedTerminatedPods(**value) if isinstance(value, dict) else value


def required_converter_CronJobSpec(value: CronJobSpecUnion) ->CronJobSpec:
    return CronJobSpec(**value) if isinstance(value, dict) else value


def required_converter_CronJobStatus(value: CronJobStatusUnion) ->CronJobStatus:
    return CronJobStatus(**value) if isinstance(value, dict) else value


def required_converter_JobConditionItem(value: JobConditionItemUnion) ->JobConditionItem:
    return JobConditionItem(**value) if isinstance(value, dict) else value


def required_converter_JobSpec(value: JobSpecUnion) ->JobSpec:
    return JobSpec(**value) if isinstance(value, dict) else value


def required_converter_JobStatus(value: JobStatusUnion) ->JobStatus:
    return JobStatus(**value) if isinstance(value, dict) else value


def required_converter_JobTemplateSpec(value: JobTemplateSpecUnion) ->JobTemplateSpec:
    return JobTemplateSpec(**value) if isinstance(value, dict) else value


def required_converter_UncountedTerminatedPods(value: UncountedTerminatedPodsUnion) ->UncountedTerminatedPods:
    return UncountedTerminatedPods(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class CronJobSpec(K8sObject):
    jobTemplate: JobTemplateSpec = attr.ib(metadata={'yaml_name': 'jobTemplate'}, converter=required_converter_JobTemplateSpec)
    schedule: str = attr.ib(metadata={'yaml_name': 'schedule'})
    concurrencyPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'concurrencyPolicy'}, default=OMIT)
    failedJobsHistoryLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'failedJobsHistoryLimit'}, default=OMIT)
    startingDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'startingDeadlineSeconds'}, default=OMIT)
    successfulJobsHistoryLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'successfulJobsHistoryLimit'}, default=OMIT)
    suspend: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'suspend'}, default=OMIT)


class CronJobSpecOptionalTypedDict(TypedDict, total=(False)):
    concurrencyPolicy: str
    failedJobsHistoryLimit: int
    startingDeadlineSeconds: int
    successfulJobsHistoryLimit: int
    suspend: bool


class CronJobSpecTypedDict(CronJobSpecOptionalTypedDict, total=(True)):
    jobTemplate: JobTemplateSpec
    schedule: str


CronJobSpecUnion = Union[CronJobSpec, CronJobSpecTypedDict]


@attr.s(kw_only=True)
class CronJobStatus(K8sObject):
    active: Union[None, OmitEnum, Sequence[kdsl.core.v1.ObjectReference]] = attr.ib(metadata={'yaml_name': 'active'}, converter=kdsl.core.v1.optional_list_converter_ObjectReference, default=OMIT)
    lastScheduleTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastScheduleTime'}, default=OMIT)
    lastSuccessfulTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastSuccessfulTime'}, default=OMIT)


class CronJobStatusTypedDict(TypedDict, total=(False)):
    active: Sequence[kdsl.core.v1.ObjectReference]
    lastScheduleTime: str
    lastSuccessfulTime: str


CronJobStatusUnion = Union[CronJobStatus, CronJobStatusTypedDict]


@attr.s(kw_only=True)
class JobConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastProbeTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastProbeTime'}, default=OMIT)
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class JobConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class JobConditionItemTypedDict(JobConditionItemOptionalTypedDict, total=(True)):
    status: str


JobConditionItemUnion = Union[JobConditionItem, JobConditionItemTypedDict]


@attr.s(kw_only=True)
class JobSpec(K8sObject):
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(metadata={'yaml_name': 'template'}, converter=kdsl.core.v1.required_converter_PodTemplateSpec)
    activeDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'activeDeadlineSeconds'}, default=OMIT)
    backoffLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'backoffLimit'}, default=OMIT)
    completionMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'completionMode'}, default=OMIT)
    completions: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'completions'}, default=OMIT)
    manualSelector: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'manualSelector'}, default=OMIT)
    parallelism: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'parallelism'}, default=OMIT)
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    suspend: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'suspend'}, default=OMIT)
    ttlSecondsAfterFinished: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'ttlSecondsAfterFinished'}, default=OMIT)


class JobSpecOptionalTypedDict(TypedDict, total=(False)):
    activeDeadlineSeconds: int
    backoffLimit: int
    completionMode: str
    completions: int
    manualSelector: bool
    parallelism: int
    selector: kdsl.core.v1.LabelSelector
    suspend: bool
    ttlSecondsAfterFinished: int


class JobSpecTypedDict(JobSpecOptionalTypedDict, total=(True)):
    template: kdsl.core.v1.PodTemplateSpec


JobSpecUnion = Union[JobSpec, JobSpecTypedDict]


@attr.s(kw_only=True)
class JobStatus(K8sObject):
    active: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'active'}, default=OMIT)
    completedIndexes: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'completedIndexes'}, default=OMIT)
    completionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'completionTime'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.batch.v1.JobConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_JobConditionItem, default=OMIT)
    failed: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'failed'}, default=OMIT)
    startTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'startTime'}, default=OMIT)
    succeeded: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'succeeded'}, default=OMIT)
    uncountedTerminatedPods: Union[None, OmitEnum, UncountedTerminatedPods] = attr.ib(metadata={'yaml_name': 'uncountedTerminatedPods'}, converter=optional_converter_UncountedTerminatedPods, default=OMIT)


class JobStatusTypedDict(TypedDict, total=(False)):
    active: int
    completedIndexes: str
    completionTime: str
    conditions: Mapping[str, kdsl.batch.v1.JobConditionItem]
    failed: int
    startTime: str
    succeeded: int
    uncountedTerminatedPods: UncountedTerminatedPods


JobStatusUnion = Union[JobStatus, JobStatusTypedDict]


@attr.s(kw_only=True)
class JobTemplateSpec(K8sObject):
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, JobSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_JobSpec, default=OMIT)


class JobTemplateSpecTypedDict(TypedDict, total=(False)):
    metadata: kdsl.core.v1.ObjectMeta
    spec: JobSpec


JobTemplateSpecUnion = Union[JobTemplateSpec, JobTemplateSpecTypedDict]


@attr.s(kw_only=True)
class UncountedTerminatedPods(K8sObject):
    failed: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'failed'}, default=OMIT)
    succeeded: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'succeeded'}, default=OMIT)


class UncountedTerminatedPodsTypedDict(TypedDict, total=(False)):
    failed: Sequence[str]
    succeeded: Sequence[str]


UncountedTerminatedPodsUnion = Union[UncountedTerminatedPods, UncountedTerminatedPodsTypedDict]


@attr.s(kw_only=True)
class CronJob(K8sResource):
    apiVersion: ClassVar[str] = 'batch/v1'
    kind: ClassVar[str] = 'CronJob'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, CronJobSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_CronJobSpec, default=OMIT)
    status: Union[None, OmitEnum, CronJobStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_CronJobStatus, default=OMIT)


@attr.s(kw_only=True)
class Job(K8sResource):
    apiVersion: ClassVar[str] = 'batch/v1'
    kind: ClassVar[str] = 'Job'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, JobSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_JobSpec, default=OMIT)
    status: Union[None, OmitEnum, JobStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_JobStatus, default=OMIT)
