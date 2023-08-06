from __future__ import annotations
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Mapping, Literal, Sequence, TypedDict, ClassVar
from kdsl.bases import OmitEnum, OMIT, K8sResource, K8sObject


@attr.s(kw_only=True)
class CSIStorageCapacity(K8sResource):
    apiVersion: ClassVar[str] = 'storage.k8s.io/v1beta1'
    kind: ClassVar[str] = 'CSIStorageCapacity'
    storageClassName: str = attr.ib(metadata={'yaml_name': 'storageClassName'})
    capacity: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'capacity'}, default=OMIT)
    maximumVolumeSize: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'maximumVolumeSize'}, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    nodeTopology: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'nodeTopology'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
