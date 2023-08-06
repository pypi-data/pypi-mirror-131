from __future__ import annotations
import attr
import kdsl.rbac.v1alpha1
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_list_converter_PolicyRule(value: Union[Sequence[PolicyRuleUnion], OmitEnum, None]) ->Union[Sequence[PolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PolicyRule(x) for x in value]


def optional_list_converter_Subject(value: Union[Sequence[SubjectUnion], OmitEnum, None]) ->Union[Sequence[Subject], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Subject(x) for x in value]


def optional_converter_AggregationRule(value: Union[AggregationRuleUnion, OmitEnum, None]) ->Union[AggregationRule, OmitEnum, None]:
    return AggregationRule(**value) if isinstance(value, dict) else value


def optional_converter_PolicyRule(value: Union[PolicyRuleUnion, OmitEnum, None]) ->Union[PolicyRule, OmitEnum, None]:
    return PolicyRule(**value) if isinstance(value, dict) else value


def optional_converter_RoleRef(value: Union[RoleRefUnion, OmitEnum, None]) ->Union[RoleRef, OmitEnum, None]:
    return RoleRef(**value) if isinstance(value, dict) else value


def optional_converter_Subject(value: Union[SubjectUnion, OmitEnum, None]) ->Union[Subject, OmitEnum, None]:
    return Subject(**value) if isinstance(value, dict) else value


def required_converter_AggregationRule(value: AggregationRuleUnion) ->AggregationRule:
    return AggregationRule(**value) if isinstance(value, dict) else value


def required_converter_PolicyRule(value: PolicyRuleUnion) ->PolicyRule:
    return PolicyRule(**value) if isinstance(value, dict) else value


def required_converter_RoleRef(value: RoleRefUnion) ->RoleRef:
    return RoleRef(**value) if isinstance(value, dict) else value


def required_converter_Subject(value: SubjectUnion) ->Subject:
    return Subject(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class AggregationRule(K8sObject):
    clusterRoleSelectors: Union[None, OmitEnum, Sequence[kdsl.core.v1.LabelSelector]] = attr.ib(metadata={'yaml_name': 'clusterRoleSelectors'}, converter=kdsl.core.v1.optional_list_converter_LabelSelector, default=OMIT)


class AggregationRuleTypedDict(TypedDict, total=(False)):
    clusterRoleSelectors: Sequence[kdsl.core.v1.LabelSelector]


AggregationRuleUnion = Union[AggregationRule, AggregationRuleTypedDict]


@attr.s(kw_only=True)
class PolicyRule(K8sObject):
    verbs: Sequence[str] = attr.ib(metadata={'yaml_name': 'verbs'})
    apiGroups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'apiGroups'}, default=OMIT)
    nonResourceURLs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'nonResourceURLs'}, default=OMIT)
    resourceNames: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'resourceNames'}, default=OMIT)
    resources: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'resources'}, default=OMIT)


class PolicyRuleOptionalTypedDict(TypedDict, total=(False)):
    apiGroups: Sequence[str]
    nonResourceURLs: Sequence[str]
    resourceNames: Sequence[str]
    resources: Sequence[str]


class PolicyRuleTypedDict(PolicyRuleOptionalTypedDict, total=(True)):
    verbs: Sequence[str]


PolicyRuleUnion = Union[PolicyRule, PolicyRuleTypedDict]


@attr.s(kw_only=True)
class RoleRef(K8sObject):
    apiGroup: str = attr.ib(metadata={'yaml_name': 'apiGroup'})
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class RoleRefTypedDict(TypedDict, total=(True)):
    apiGroup: str
    kind: str
    name: str


RoleRefUnion = Union[RoleRef, RoleRefTypedDict]


@attr.s(kw_only=True)
class Subject(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)


class SubjectOptionalTypedDict(TypedDict, total=(False)):
    apiVersion: str
    namespace: str


class SubjectTypedDict(SubjectOptionalTypedDict, total=(True)):
    kind: str
    name: str


SubjectUnion = Union[Subject, SubjectTypedDict]


@attr.s(kw_only=True)
class ClusterRole(K8sResource):
    apiVersion: ClassVar[str] = 'rbac.authorization.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'ClusterRole'
    aggregationRule: Union[None, OmitEnum, AggregationRule] = attr.ib(metadata={'yaml_name': 'aggregationRule'}, converter=optional_converter_AggregationRule, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[PolicyRule]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_PolicyRule, default=OMIT)


@attr.s(kw_only=True)
class ClusterRoleBinding(K8sResource):
    apiVersion: ClassVar[str] = 'rbac.authorization.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'ClusterRoleBinding'
    roleRef: RoleRef = attr.ib(metadata={'yaml_name': 'roleRef'}, converter=required_converter_RoleRef)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    subjects: Union[None, OmitEnum, Sequence[Subject]] = attr.ib(metadata={'yaml_name': 'subjects'}, converter=optional_list_converter_Subject, default=OMIT)


@attr.s(kw_only=True)
class Role(K8sResource):
    apiVersion: ClassVar[str] = 'rbac.authorization.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'Role'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[PolicyRule]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_PolicyRule, default=OMIT)


@attr.s(kw_only=True)
class RoleBinding(K8sResource):
    apiVersion: ClassVar[str] = 'rbac.authorization.k8s.io/v1alpha1'
    kind: ClassVar[str] = 'RoleBinding'
    roleRef: RoleRef = attr.ib(metadata={'yaml_name': 'roleRef'}, converter=required_converter_RoleRef)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    subjects: Union[None, OmitEnum, Sequence[Subject]] = attr.ib(metadata={'yaml_name': 'subjects'}, converter=optional_list_converter_Subject, default=OMIT)
