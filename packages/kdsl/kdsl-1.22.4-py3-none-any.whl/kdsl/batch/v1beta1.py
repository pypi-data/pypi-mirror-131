from __future__ import annotations
import kdsl.batch.v1
import attr
import kdsl.batch.v1beta1
import kdsl.core.v1
from typing import Any, Optional, Union, Mapping, Literal, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_converter_CronJobSpec(value: Union[CronJobSpecUnion, OmitEnum, None]) ->Union[CronJobSpec, OmitEnum, None]:
    return CronJobSpec(**value) if isinstance(value, dict) else value


def optional_converter_CronJobStatus(value: Union[CronJobStatusUnion, OmitEnum, None]) ->Union[CronJobStatus, OmitEnum, None]:
    return CronJobStatus(**value) if isinstance(value, dict) else value


def optional_converter_JobTemplateSpec(value: Union[JobTemplateSpecUnion, OmitEnum, None]) ->Union[JobTemplateSpec, OmitEnum, None]:
    return JobTemplateSpec(**value) if isinstance(value, dict) else value


def required_converter_CronJobSpec(value: CronJobSpecUnion) ->CronJobSpec:
    return CronJobSpec(**value) if isinstance(value, dict) else value


def required_converter_CronJobStatus(value: CronJobStatusUnion) ->CronJobStatus:
    return CronJobStatus(**value) if isinstance(value, dict) else value


def required_converter_JobTemplateSpec(value: JobTemplateSpecUnion) ->JobTemplateSpec:
    return JobTemplateSpec(**value) if isinstance(value, dict) else value


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
class JobTemplateSpec(K8sObject):
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, kdsl.batch.v1.JobSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=kdsl.batch.v1.optional_converter_JobSpec, default=OMIT)


class JobTemplateSpecTypedDict(TypedDict, total=(False)):
    metadata: kdsl.core.v1.ObjectMeta
    spec: kdsl.batch.v1.JobSpec


JobTemplateSpecUnion = Union[JobTemplateSpec, JobTemplateSpecTypedDict]


@attr.s(kw_only=True)
class CronJob(K8sResource):
    apiVersion: ClassVar[str] = 'batch/v1beta1'
    kind: ClassVar[str] = 'CronJob'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, CronJobSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_CronJobSpec, default=OMIT)
    status: Union[None, OmitEnum, CronJobStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_CronJobStatus, default=OMIT)
