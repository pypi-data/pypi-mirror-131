from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.authorization.v1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def required_list_converter_NonResourceRule(value: Sequence[NonResourceRuleUnion]) ->Sequence[NonResourceRule]:
    return [required_converter_NonResourceRule(x) for x in value]


def required_list_converter_ResourceRule(value: Sequence[ResourceRuleUnion]) ->Sequence[ResourceRule]:
    return [required_converter_ResourceRule(x) for x in value]


def optional_converter_NonResourceAttributes(value: Union[NonResourceAttributesUnion, OmitEnum, None]) ->Union[NonResourceAttributes, OmitEnum, None]:
    return NonResourceAttributes(**value) if isinstance(value, dict) else value


def optional_converter_NonResourceRule(value: Union[NonResourceRuleUnion, OmitEnum, None]) ->Union[NonResourceRule, OmitEnum, None]:
    return NonResourceRule(**value) if isinstance(value, dict) else value


def optional_converter_ResourceAttributes(value: Union[ResourceAttributesUnion, OmitEnum, None]) ->Union[ResourceAttributes, OmitEnum, None]:
    return ResourceAttributes(**value) if isinstance(value, dict) else value


def optional_converter_ResourceRule(value: Union[ResourceRuleUnion, OmitEnum, None]) ->Union[ResourceRule, OmitEnum, None]:
    return ResourceRule(**value) if isinstance(value, dict) else value


def optional_converter_SelfSubjectAccessReviewSpec(value: Union[SelfSubjectAccessReviewSpecUnion, OmitEnum, None]) ->Union[SelfSubjectAccessReviewSpec, OmitEnum, None]:
    return SelfSubjectAccessReviewSpec(**value) if isinstance(value, dict) else value


def optional_converter_SelfSubjectRulesReviewSpec(value: Union[SelfSubjectRulesReviewSpecUnion, OmitEnum, None]) ->Union[SelfSubjectRulesReviewSpec, OmitEnum, None]:
    return SelfSubjectRulesReviewSpec(**value) if isinstance(value, dict) else value


def optional_converter_SubjectAccessReviewSpec(value: Union[SubjectAccessReviewSpecUnion, OmitEnum, None]) ->Union[SubjectAccessReviewSpec, OmitEnum, None]:
    return SubjectAccessReviewSpec(**value) if isinstance(value, dict) else value


def optional_converter_SubjectAccessReviewStatus(value: Union[SubjectAccessReviewStatusUnion, OmitEnum, None]) ->Union[SubjectAccessReviewStatus, OmitEnum, None]:
    return SubjectAccessReviewStatus(**value) if isinstance(value, dict) else value


def optional_converter_SubjectRulesReviewStatus(value: Union[SubjectRulesReviewStatusUnion, OmitEnum, None]) ->Union[SubjectRulesReviewStatus, OmitEnum, None]:
    return SubjectRulesReviewStatus(**value) if isinstance(value, dict) else value


def required_converter_NonResourceAttributes(value: NonResourceAttributesUnion) ->NonResourceAttributes:
    return NonResourceAttributes(**value) if isinstance(value, dict) else value


def required_converter_NonResourceRule(value: NonResourceRuleUnion) ->NonResourceRule:
    return NonResourceRule(**value) if isinstance(value, dict) else value


def required_converter_ResourceAttributes(value: ResourceAttributesUnion) ->ResourceAttributes:
    return ResourceAttributes(**value) if isinstance(value, dict) else value


def required_converter_ResourceRule(value: ResourceRuleUnion) ->ResourceRule:
    return ResourceRule(**value) if isinstance(value, dict) else value


def required_converter_SelfSubjectAccessReviewSpec(value: SelfSubjectAccessReviewSpecUnion) ->SelfSubjectAccessReviewSpec:
    return SelfSubjectAccessReviewSpec(**value) if isinstance(value, dict) else value


def required_converter_SelfSubjectRulesReviewSpec(value: SelfSubjectRulesReviewSpecUnion) ->SelfSubjectRulesReviewSpec:
    return SelfSubjectRulesReviewSpec(**value) if isinstance(value, dict) else value


def required_converter_SubjectAccessReviewSpec(value: SubjectAccessReviewSpecUnion) ->SubjectAccessReviewSpec:
    return SubjectAccessReviewSpec(**value) if isinstance(value, dict) else value


def required_converter_SubjectAccessReviewStatus(value: SubjectAccessReviewStatusUnion) ->SubjectAccessReviewStatus:
    return SubjectAccessReviewStatus(**value) if isinstance(value, dict) else value


def required_converter_SubjectRulesReviewStatus(value: SubjectRulesReviewStatusUnion) ->SubjectRulesReviewStatus:
    return SubjectRulesReviewStatus(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class NonResourceAttributes(K8sObject):
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    verb: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'verb'}, default=OMIT)


class NonResourceAttributesTypedDict(TypedDict, total=(False)):
    path: str
    verb: str


NonResourceAttributesUnion = Union[NonResourceAttributes, NonResourceAttributesTypedDict]


@attr.s(kw_only=True)
class NonResourceRule(K8sObject):
    verbs: Sequence[str] = attr.ib(metadata={'yaml_name': 'verbs'})
    nonResourceURLs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'nonResourceURLs'}, default=OMIT)


class NonResourceRuleOptionalTypedDict(TypedDict, total=(False)):
    nonResourceURLs: Sequence[str]


class NonResourceRuleTypedDict(NonResourceRuleOptionalTypedDict, total=(True)):
    verbs: Sequence[str]


NonResourceRuleUnion = Union[NonResourceRule, NonResourceRuleTypedDict]


@attr.s(kw_only=True)
class ResourceAttributes(K8sObject):
    group: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'group'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    resource: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resource'}, default=OMIT)
    subresource: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'subresource'}, default=OMIT)
    verb: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'verb'}, default=OMIT)
    version: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'version'}, default=OMIT)


class ResourceAttributesTypedDict(TypedDict, total=(False)):
    group: str
    name: str
    namespace: str
    resource: str
    subresource: str
    verb: str
    version: str


ResourceAttributesUnion = Union[ResourceAttributes, ResourceAttributesTypedDict]


@attr.s(kw_only=True)
class ResourceRule(K8sObject):
    verbs: Sequence[str] = attr.ib(metadata={'yaml_name': 'verbs'})
    apiGroups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'apiGroups'}, default=OMIT)
    resourceNames: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'resourceNames'}, default=OMIT)
    resources: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'resources'}, default=OMIT)


class ResourceRuleOptionalTypedDict(TypedDict, total=(False)):
    apiGroups: Sequence[str]
    resourceNames: Sequence[str]
    resources: Sequence[str]


class ResourceRuleTypedDict(ResourceRuleOptionalTypedDict, total=(True)):
    verbs: Sequence[str]


ResourceRuleUnion = Union[ResourceRule, ResourceRuleTypedDict]


@attr.s(kw_only=True)
class SelfSubjectAccessReviewSpec(K8sObject):
    nonResourceAttributes: Union[None, OmitEnum, NonResourceAttributes] = attr.ib(metadata={'yaml_name': 'nonResourceAttributes'}, converter=optional_converter_NonResourceAttributes, default=OMIT)
    resourceAttributes: Union[None, OmitEnum, ResourceAttributes] = attr.ib(metadata={'yaml_name': 'resourceAttributes'}, converter=optional_converter_ResourceAttributes, default=OMIT)


class SelfSubjectAccessReviewSpecTypedDict(TypedDict, total=(False)):
    nonResourceAttributes: NonResourceAttributes
    resourceAttributes: ResourceAttributes


SelfSubjectAccessReviewSpecUnion = Union[SelfSubjectAccessReviewSpec, SelfSubjectAccessReviewSpecTypedDict]


@attr.s(kw_only=True)
class SelfSubjectRulesReviewSpec(K8sObject):
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)


class SelfSubjectRulesReviewSpecTypedDict(TypedDict, total=(False)):
    namespace: str


SelfSubjectRulesReviewSpecUnion = Union[SelfSubjectRulesReviewSpec, SelfSubjectRulesReviewSpecTypedDict]


@attr.s(kw_only=True)
class SubjectAccessReviewSpec(K8sObject):
    extra: Union[None, OmitEnum, Mapping[str, Sequence[str]]] = attr.ib(metadata={'yaml_name': 'extra'}, default=OMIT)
    groups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'groups'}, default=OMIT)
    nonResourceAttributes: Union[None, OmitEnum, NonResourceAttributes] = attr.ib(metadata={'yaml_name': 'nonResourceAttributes'}, converter=optional_converter_NonResourceAttributes, default=OMIT)
    resourceAttributes: Union[None, OmitEnum, ResourceAttributes] = attr.ib(metadata={'yaml_name': 'resourceAttributes'}, converter=optional_converter_ResourceAttributes, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class SubjectAccessReviewSpecTypedDict(TypedDict, total=(False)):
    extra: Mapping[str, Sequence[str]]
    groups: Sequence[str]
    nonResourceAttributes: NonResourceAttributes
    resourceAttributes: ResourceAttributes
    uid: str
    user: str


SubjectAccessReviewSpecUnion = Union[SubjectAccessReviewSpec, SubjectAccessReviewSpecTypedDict]


@attr.s(kw_only=True)
class SubjectAccessReviewStatus(K8sObject):
    allowed: bool = attr.ib(metadata={'yaml_name': 'allowed'})
    denied: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'denied'}, default=OMIT)
    evaluationError: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'evaluationError'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class SubjectAccessReviewStatusOptionalTypedDict(TypedDict, total=(False)):
    denied: bool
    evaluationError: str
    reason: str


class SubjectAccessReviewStatusTypedDict(SubjectAccessReviewStatusOptionalTypedDict, total=(True)):
    allowed: bool


SubjectAccessReviewStatusUnion = Union[SubjectAccessReviewStatus, SubjectAccessReviewStatusTypedDict]


@attr.s(kw_only=True)
class SubjectRulesReviewStatus(K8sObject):
    incomplete: bool = attr.ib(metadata={'yaml_name': 'incomplete'})
    nonResourceRules: Sequence[NonResourceRule] = attr.ib(metadata={'yaml_name': 'nonResourceRules'}, converter=required_list_converter_NonResourceRule)
    resourceRules: Sequence[ResourceRule] = attr.ib(metadata={'yaml_name': 'resourceRules'}, converter=required_list_converter_ResourceRule)
    evaluationError: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'evaluationError'}, default=OMIT)


class SubjectRulesReviewStatusOptionalTypedDict(TypedDict, total=(False)):
    evaluationError: str


class SubjectRulesReviewStatusTypedDict(SubjectRulesReviewStatusOptionalTypedDict, total=(True)):
    incomplete: bool
    nonResourceRules: Sequence[NonResourceRule]
    resourceRules: Sequence[ResourceRule]


SubjectRulesReviewStatusUnion = Union[SubjectRulesReviewStatus, SubjectRulesReviewStatusTypedDict]


@attr.s(kw_only=True)
class LocalSubjectAccessReview(K8sResource):
    apiVersion: ClassVar[str] = 'authorization.k8s.io/v1'
    kind: ClassVar[str] = 'LocalSubjectAccessReview'
    spec: SubjectAccessReviewSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_SubjectAccessReviewSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, SubjectAccessReviewStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_SubjectAccessReviewStatus, default=OMIT)


@attr.s(kw_only=True)
class SelfSubjectAccessReview(K8sResource):
    apiVersion: ClassVar[str] = 'authorization.k8s.io/v1'
    kind: ClassVar[str] = 'SelfSubjectAccessReview'
    spec: SelfSubjectAccessReviewSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_SelfSubjectAccessReviewSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, SubjectAccessReviewStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_SubjectAccessReviewStatus, default=OMIT)


@attr.s(kw_only=True)
class SelfSubjectRulesReview(K8sResource):
    apiVersion: ClassVar[str] = 'authorization.k8s.io/v1'
    kind: ClassVar[str] = 'SelfSubjectRulesReview'
    spec: SelfSubjectRulesReviewSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_SelfSubjectRulesReviewSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, SubjectRulesReviewStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_SubjectRulesReviewStatus, default=OMIT)


@attr.s(kw_only=True)
class SubjectAccessReview(K8sResource):
    apiVersion: ClassVar[str] = 'authorization.k8s.io/v1'
    kind: ClassVar[str] = 'SubjectAccessReview'
    spec: SubjectAccessReviewSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_SubjectAccessReviewSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, SubjectAccessReviewStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_SubjectAccessReviewStatus, default=OMIT)
