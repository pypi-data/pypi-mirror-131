from __future__ import annotations
import attr
import kdsl.storage.v1
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_list_converter_TokenRequest(value: Union[Sequence[TokenRequestUnion], OmitEnum, None]) ->Union[Sequence[TokenRequest], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_TokenRequest(x) for x in value]


def required_mlist_converter_CSINodeDriverItem(value: Mapping[str, CSINodeDriverItemUnion]) ->Mapping[str, CSINodeDriverItem]:
    return {k: required_converter_CSINodeDriverItem(v) for k, v in value.items()}


def optional_converter_CSIDriverSpec(value: Union[CSIDriverSpecUnion, OmitEnum, None]) ->Union[CSIDriverSpec, OmitEnum, None]:
    return CSIDriverSpec(**value) if isinstance(value, dict) else value


def optional_converter_CSINodeDriverItem(value: Union[CSINodeDriverItemUnion, OmitEnum, None]) ->Union[CSINodeDriverItem, OmitEnum, None]:
    return CSINodeDriverItem(**value) if isinstance(value, dict) else value


def optional_converter_CSINodeSpec(value: Union[CSINodeSpecUnion, OmitEnum, None]) ->Union[CSINodeSpec, OmitEnum, None]:
    return CSINodeSpec(**value) if isinstance(value, dict) else value


def optional_converter_TokenRequest(value: Union[TokenRequestUnion, OmitEnum, None]) ->Union[TokenRequest, OmitEnum, None]:
    return TokenRequest(**value) if isinstance(value, dict) else value


def optional_converter_VolumeAttachmentSource(value: Union[VolumeAttachmentSourceUnion, OmitEnum, None]) ->Union[VolumeAttachmentSource, OmitEnum, None]:
    return VolumeAttachmentSource(**value) if isinstance(value, dict) else value


def optional_converter_VolumeAttachmentSpec(value: Union[VolumeAttachmentSpecUnion, OmitEnum, None]) ->Union[VolumeAttachmentSpec, OmitEnum, None]:
    return VolumeAttachmentSpec(**value) if isinstance(value, dict) else value


def optional_converter_VolumeAttachmentStatus(value: Union[VolumeAttachmentStatusUnion, OmitEnum, None]) ->Union[VolumeAttachmentStatus, OmitEnum, None]:
    return VolumeAttachmentStatus(**value) if isinstance(value, dict) else value


def optional_converter_VolumeError(value: Union[VolumeErrorUnion, OmitEnum, None]) ->Union[VolumeError, OmitEnum, None]:
    return VolumeError(**value) if isinstance(value, dict) else value


def optional_converter_VolumeNodeResources(value: Union[VolumeNodeResourcesUnion, OmitEnum, None]) ->Union[VolumeNodeResources, OmitEnum, None]:
    return VolumeNodeResources(**value) if isinstance(value, dict) else value


def required_converter_CSIDriverSpec(value: CSIDriverSpecUnion) ->CSIDriverSpec:
    return CSIDriverSpec(**value) if isinstance(value, dict) else value


def required_converter_CSINodeDriverItem(value: CSINodeDriverItemUnion) ->CSINodeDriverItem:
    return CSINodeDriverItem(**value) if isinstance(value, dict) else value


def required_converter_CSINodeSpec(value: CSINodeSpecUnion) ->CSINodeSpec:
    return CSINodeSpec(**value) if isinstance(value, dict) else value


def required_converter_TokenRequest(value: TokenRequestUnion) ->TokenRequest:
    return TokenRequest(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentSource(value: VolumeAttachmentSourceUnion) ->VolumeAttachmentSource:
    return VolumeAttachmentSource(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentSpec(value: VolumeAttachmentSpecUnion) ->VolumeAttachmentSpec:
    return VolumeAttachmentSpec(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentStatus(value: VolumeAttachmentStatusUnion) ->VolumeAttachmentStatus:
    return VolumeAttachmentStatus(**value) if isinstance(value, dict) else value


def required_converter_VolumeError(value: VolumeErrorUnion) ->VolumeError:
    return VolumeError(**value) if isinstance(value, dict) else value


def required_converter_VolumeNodeResources(value: VolumeNodeResourcesUnion) ->VolumeNodeResources:
    return VolumeNodeResources(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class CSIDriverSpec(K8sObject):
    attachRequired: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'attachRequired'}, default=OMIT)
    fsGroupPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsGroupPolicy'}, default=OMIT)
    podInfoOnMount: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'podInfoOnMount'}, default=OMIT)
    requiresRepublish: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'requiresRepublish'}, default=OMIT)
    storageCapacity: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'storageCapacity'}, default=OMIT)
    tokenRequests: Union[None, OmitEnum, Sequence[TokenRequest]] = attr.ib(metadata={'yaml_name': 'tokenRequests'}, converter=optional_list_converter_TokenRequest, default=OMIT)
    volumeLifecycleModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'volumeLifecycleModes'}, default=OMIT)


class CSIDriverSpecTypedDict(TypedDict, total=(False)):
    attachRequired: bool
    fsGroupPolicy: str
    podInfoOnMount: bool
    requiresRepublish: bool
    storageCapacity: bool
    tokenRequests: Sequence[TokenRequest]
    volumeLifecycleModes: Sequence[str]


CSIDriverSpecUnion = Union[CSIDriverSpec, CSIDriverSpecTypedDict]


@attr.s(kw_only=True)
class CSINodeDriverItem(K8sObject):
    nodeID: str = attr.ib(metadata={'yaml_name': 'nodeID'})
    allocatable: Union[None, OmitEnum, VolumeNodeResources] = attr.ib(metadata={'yaml_name': 'allocatable'}, converter=optional_converter_VolumeNodeResources, default=OMIT)
    topologyKeys: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'topologyKeys'}, default=OMIT)


class CSINodeDriverItemOptionalTypedDict(TypedDict, total=(False)):
    allocatable: VolumeNodeResources
    topologyKeys: Sequence[str]


class CSINodeDriverItemTypedDict(CSINodeDriverItemOptionalTypedDict, total=(True)):
    nodeID: str


CSINodeDriverItemUnion = Union[CSINodeDriverItem, CSINodeDriverItemTypedDict]


@attr.s(kw_only=True)
class CSINodeSpec(K8sObject):
    drivers: Mapping[str, kdsl.storage.v1.CSINodeDriverItem] = attr.ib(metadata={'yaml_name': 'drivers', 'mlist_key': 'name'}, converter=required_mlist_converter_CSINodeDriverItem)


class CSINodeSpecTypedDict(TypedDict, total=(True)):
    drivers: Mapping[str, kdsl.storage.v1.CSINodeDriverItem]


CSINodeSpecUnion = Union[CSINodeSpec, CSINodeSpecTypedDict]


@attr.s(kw_only=True)
class TokenRequest(K8sObject):
    audience: str = attr.ib(metadata={'yaml_name': 'audience'})
    expirationSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'expirationSeconds'}, default=OMIT)


class TokenRequestOptionalTypedDict(TypedDict, total=(False)):
    expirationSeconds: int


class TokenRequestTypedDict(TokenRequestOptionalTypedDict, total=(True)):
    audience: str


TokenRequestUnion = Union[TokenRequest, TokenRequestTypedDict]


@attr.s(kw_only=True)
class VolumeAttachmentSource(K8sObject):
    inlineVolumeSpec: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeSpec] = attr.ib(metadata={'yaml_name': 'inlineVolumeSpec'}, converter=kdsl.core.v1.optional_converter_PersistentVolumeSpec, default=OMIT)
    persistentVolumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'persistentVolumeName'}, default=OMIT)


class VolumeAttachmentSourceTypedDict(TypedDict, total=(False)):
    inlineVolumeSpec: kdsl.core.v1.PersistentVolumeSpec
    persistentVolumeName: str


VolumeAttachmentSourceUnion = Union[VolumeAttachmentSource, VolumeAttachmentSourceTypedDict]


@attr.s(kw_only=True)
class VolumeAttachmentSpec(K8sObject):
    attacher: str = attr.ib(metadata={'yaml_name': 'attacher'})
    nodeName: str = attr.ib(metadata={'yaml_name': 'nodeName'})
    source: VolumeAttachmentSource = attr.ib(metadata={'yaml_name': 'source'}, converter=required_converter_VolumeAttachmentSource)


class VolumeAttachmentSpecTypedDict(TypedDict, total=(True)):
    attacher: str
    nodeName: str
    source: VolumeAttachmentSource


VolumeAttachmentSpecUnion = Union[VolumeAttachmentSpec, VolumeAttachmentSpecTypedDict]


@attr.s(kw_only=True)
class VolumeAttachmentStatus(K8sObject):
    attached: bool = attr.ib(metadata={'yaml_name': 'attached'})
    attachError: Union[None, OmitEnum, VolumeError] = attr.ib(metadata={'yaml_name': 'attachError'}, converter=optional_converter_VolumeError, default=OMIT)
    attachmentMetadata: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'attachmentMetadata'}, default=OMIT)
    detachError: Union[None, OmitEnum, VolumeError] = attr.ib(metadata={'yaml_name': 'detachError'}, converter=optional_converter_VolumeError, default=OMIT)


class VolumeAttachmentStatusOptionalTypedDict(TypedDict, total=(False)):
    attachError: VolumeError
    attachmentMetadata: Mapping[str, str]
    detachError: VolumeError


class VolumeAttachmentStatusTypedDict(VolumeAttachmentStatusOptionalTypedDict, total=(True)):
    attached: bool


VolumeAttachmentStatusUnion = Union[VolumeAttachmentStatus, VolumeAttachmentStatusTypedDict]


@attr.s(kw_only=True)
class VolumeError(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    time: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'time'}, default=OMIT)


class VolumeErrorTypedDict(TypedDict, total=(False)):
    message: str
    time: str


VolumeErrorUnion = Union[VolumeError, VolumeErrorTypedDict]


@attr.s(kw_only=True)
class VolumeNodeResources(K8sObject):
    count: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'count'}, default=OMIT)


class VolumeNodeResourcesTypedDict(TypedDict, total=(False)):
    count: int


VolumeNodeResourcesUnion = Union[VolumeNodeResources, VolumeNodeResourcesTypedDict]


@attr.s(kw_only=True)
class CSIDriver(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1'
    kind: ClassVar[str] = 'CSIDriver'
    spec: CSIDriverSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_CSIDriverSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class CSINode(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1'
    kind: ClassVar[str] = 'CSINode'
    spec: CSINodeSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_CSINodeSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class StorageClass(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1'
    kind: ClassVar[str] = 'StorageClass'
    provisioner: str = attr.ib(metadata={'yaml_name': 'provisioner'})
    allowVolumeExpansion: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'allowVolumeExpansion'}, default=OMIT)
    allowedTopologies: Union[None, OmitEnum, Sequence[kdsl.core.v1.TopologySelectorTerm]] = attr.ib(metadata={'yaml_name': 'allowedTopologies'}, converter=kdsl.core.v1.optional_list_converter_TopologySelectorTerm, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    mountOptions: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'mountOptions'}, default=OMIT)
    parameters: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'parameters'}, default=OMIT)
    reclaimPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reclaimPolicy'}, default=OMIT)
    volumeBindingMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeBindingMode'}, default=OMIT)


@attr.s(kw_only=True)
class VolumeAttachment(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1'
    kind: ClassVar[str] = 'VolumeAttachment'
    spec: VolumeAttachmentSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_VolumeAttachmentSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, VolumeAttachmentStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_VolumeAttachmentStatus, default=OMIT)
