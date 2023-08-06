from __future__ import annotations
import kdsl.storage.v1alpha1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Mapping, Literal, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


def optional_converter_VolumeAttachmentSource(value: Union[VolumeAttachmentSourceUnion, OmitEnum, None]) ->Union[VolumeAttachmentSource, OmitEnum, None]:
    return VolumeAttachmentSource(**value) if isinstance(value, dict) else value


def optional_converter_VolumeAttachmentSpec(value: Union[VolumeAttachmentSpecUnion, OmitEnum, None]) ->Union[VolumeAttachmentSpec, OmitEnum, None]:
    return VolumeAttachmentSpec(**value) if isinstance(value, dict) else value


def optional_converter_VolumeAttachmentStatus(value: Union[VolumeAttachmentStatusUnion, OmitEnum, None]) ->Union[VolumeAttachmentStatus, OmitEnum, None]:
    return VolumeAttachmentStatus(**value) if isinstance(value, dict) else value


def optional_converter_VolumeError(value: Union[VolumeErrorUnion, OmitEnum, None]) ->Union[VolumeError, OmitEnum, None]:
    return VolumeError(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentSource(value: VolumeAttachmentSourceUnion) ->VolumeAttachmentSource:
    return VolumeAttachmentSource(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentSpec(value: VolumeAttachmentSpecUnion) ->VolumeAttachmentSpec:
    return VolumeAttachmentSpec(**value) if isinstance(value, dict) else value


def required_converter_VolumeAttachmentStatus(value: VolumeAttachmentStatusUnion) ->VolumeAttachmentStatus:
    return VolumeAttachmentStatus(**value) if isinstance(value, dict) else value


def required_converter_VolumeError(value: VolumeErrorUnion) ->VolumeError:
    return VolumeError(**value) if isinstance(value, dict) else value


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
class CSIStorageCapacity(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'CSIStorageCapacity'
    storageClassName: str = attr.ib(metadata={'yaml_name': 'storageClassName'})
    capacity: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'capacity'}, default=OMIT)
    maximumVolumeSize: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'maximumVolumeSize'}, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    nodeTopology: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'nodeTopology'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)


@attr.s(kw_only=True)
class VolumeAttachment(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'VolumeAttachment'
    spec: VolumeAttachmentSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_VolumeAttachmentSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, VolumeAttachmentStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_VolumeAttachmentStatus, default=OMIT)
