from __future__ import annotations
import kdsl.coordination.v1beta1
import attr
import kdsl.core.v1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_converter_LeaseSpec(value: Union[LeaseSpecUnion, OmitEnum, None]) ->Union[LeaseSpec, OmitEnum, None]:
    return LeaseSpec(**value) if isinstance(value, dict) else value


def required_converter_LeaseSpec(value: LeaseSpecUnion) ->LeaseSpec:
    return LeaseSpec(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class LeaseSpec(K8sObject):
    acquireTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'acquireTime'}, default=OMIT)
    holderIdentity: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'holderIdentity'}, default=OMIT)
    leaseDurationSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'leaseDurationSeconds'}, default=OMIT)
    leaseTransitions: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'leaseTransitions'}, default=OMIT)
    renewTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'renewTime'}, default=OMIT)


class LeaseSpecTypedDict(TypedDict, total=(False)):
    acquireTime: str
    holderIdentity: str
    leaseDurationSeconds: int
    leaseTransitions: int
    renewTime: str


LeaseSpecUnion = Union[LeaseSpec, LeaseSpecTypedDict]


@attr.s(kw_only=True)
class Lease(K8sResource):
    apiVersion: ClassVar[str] = 'coordination.k8s.io/v1beta1'
    kind: ClassVar[str] = 'Lease'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, LeaseSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_LeaseSpec, default=OMIT)
