from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.apiserverinternal.v1alpha1
from typing import Sequence, Any, Optional, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_ServerStorageVersion(value: Union[Sequence[ServerStorageVersionUnion], OmitEnum, None]) ->Union[Sequence[ServerStorageVersion], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ServerStorageVersion(x) for x in value]


def optional_list_converter_StorageVersionCondition(value: Union[Sequence[StorageVersionConditionUnion], OmitEnum, None]) ->Union[Sequence[StorageVersionCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_StorageVersionCondition(x) for x in value]


def optional_converter_ServerStorageVersion(value: Union[ServerStorageVersionUnion, OmitEnum, None]) ->Union[ServerStorageVersion, OmitEnum, None]:
    return ServerStorageVersion(**value) if isinstance(value, dict) else value


def optional_converter_StorageVersionCondition(value: Union[StorageVersionConditionUnion, OmitEnum, None]) ->Union[StorageVersionCondition, OmitEnum, None]:
    return StorageVersionCondition(**value) if isinstance(value, dict) else value


def optional_converter_StorageVersionStatus(value: Union[StorageVersionStatusUnion, OmitEnum, None]) ->Union[StorageVersionStatus, OmitEnum, None]:
    return StorageVersionStatus(**value) if isinstance(value, dict) else value


def required_converter_ServerStorageVersion(value: ServerStorageVersionUnion) ->ServerStorageVersion:
    return ServerStorageVersion(**value) if isinstance(value, dict) else value


def required_converter_StorageVersionCondition(value: StorageVersionConditionUnion) ->StorageVersionCondition:
    return StorageVersionCondition(**value) if isinstance(value, dict) else value


def required_converter_StorageVersionStatus(value: StorageVersionStatusUnion) ->StorageVersionStatus:
    return StorageVersionStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class ServerStorageVersion(K8sObject):
    apiServerID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiServerID'}, default=OMIT)
    decodableVersions: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'decodableVersions'}, default=OMIT)
    encodingVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'encodingVersion'}, default=OMIT)


class ServerStorageVersionTypedDict(TypedDict, total=(False)):
    apiServerID: str
    decodableVersions: Sequence[str]
    encodingVersion: str


ServerStorageVersionUnion = Union[ServerStorageVersion, ServerStorageVersionTypedDict]


@attr.s(kw_only=True)
class StorageVersionCondition(K8sObject):
    reason: str = attr.ib(metadata={'yaml_name': 'reason'})
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)


class StorageVersionConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    observedGeneration: int


class StorageVersionConditionTypedDict(StorageVersionConditionOptionalTypedDict, total=(True)):
    reason: str
    status: str
    type: str


StorageVersionConditionUnion = Union[StorageVersionCondition, StorageVersionConditionTypedDict]


@attr.s(kw_only=True)
class StorageVersionStatus(K8sObject):
    commonEncodingVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'commonEncodingVersion'}, default=OMIT)
    conditions: Union[None, OmitEnum, Sequence[StorageVersionCondition]] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_list_converter_StorageVersionCondition, default=OMIT)
    storageVersions: Union[None, OmitEnum, Sequence[ServerStorageVersion]] = attr.ib(metadata={'yaml_name': 'storageVersions'}, converter=optional_list_converter_ServerStorageVersion, default=OMIT)


class StorageVersionStatusTypedDict(TypedDict, total=(False)):
    commonEncodingVersion: str
    conditions: Sequence[StorageVersionCondition]
    storageVersions: Sequence[ServerStorageVersion]


StorageVersionStatusUnion = Union[StorageVersionStatus, StorageVersionStatusTypedDict]


@attr.s(kw_only=True)
class StorageVersion(K8sResource):
    apiVersion: ClassVar[str] = 'internal.apiserver.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'StorageVersion'
    spec: Any = attr.ib(metadata={'yaml_name': 'spec'})
    status: StorageVersionStatus = attr.ib(metadata={'yaml_name': 'status'}, converter=required_converter_StorageVersionStatus)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
