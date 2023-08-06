from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.flowcontrol.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_list_converter_FlowSchemaCondition(value: Union[Sequence[FlowSchemaConditionUnion], OmitEnum, None]) ->Union[Sequence[FlowSchemaCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_FlowSchemaCondition(x) for x in value]


def optional_list_converter_NonResourcePolicyRule(value: Union[Sequence[NonResourcePolicyRuleUnion], OmitEnum, None]) ->Union[Sequence[NonResourcePolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NonResourcePolicyRule(x) for x in value]


def optional_list_converter_PolicyRulesWithSubjects(value: Union[Sequence[PolicyRulesWithSubjectsUnion], OmitEnum, None]) ->Union[Sequence[PolicyRulesWithSubjects], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PolicyRulesWithSubjects(x) for x in value]


def optional_list_converter_PriorityLevelConfigurationCondition(value: Union[Sequence[PriorityLevelConfigurationConditionUnion], OmitEnum, None]) ->Union[Sequence[PriorityLevelConfigurationCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PriorityLevelConfigurationCondition(x) for x in value]


def optional_list_converter_ResourcePolicyRule(value: Union[Sequence[ResourcePolicyRuleUnion], OmitEnum, None]) ->Union[Sequence[ResourcePolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ResourcePolicyRule(x) for x in value]


def required_list_converter_Subject(value: Sequence[SubjectUnion]) ->Sequence[Subject]:
    return [required_converter_Subject(x) for x in value]


def optional_converter_FlowDistinguisherMethod(value: Union[FlowDistinguisherMethodUnion, OmitEnum, None]) ->Union[FlowDistinguisherMethod, OmitEnum, None]:
    return FlowDistinguisherMethod(**value) if isinstance(value, dict) else value


def optional_converter_FlowSchemaCondition(value: Union[FlowSchemaConditionUnion, OmitEnum, None]) ->Union[FlowSchemaCondition, OmitEnum, None]:
    return FlowSchemaCondition(**value) if isinstance(value, dict) else value


def optional_converter_FlowSchemaSpec(value: Union[FlowSchemaSpecUnion, OmitEnum, None]) ->Union[FlowSchemaSpec, OmitEnum, None]:
    return FlowSchemaSpec(**value) if isinstance(value, dict) else value


def optional_converter_FlowSchemaStatus(value: Union[FlowSchemaStatusUnion, OmitEnum, None]) ->Union[FlowSchemaStatus, OmitEnum, None]:
    return FlowSchemaStatus(**value) if isinstance(value, dict) else value


def optional_converter_GroupSubject(value: Union[GroupSubjectUnion, OmitEnum, None]) ->Union[GroupSubject, OmitEnum, None]:
    return GroupSubject(**value) if isinstance(value, dict) else value


def optional_converter_LimitResponse(value: Union[LimitResponseUnion, OmitEnum, None]) ->Union[LimitResponse, OmitEnum, None]:
    return LimitResponse(**value) if isinstance(value, dict) else value


def optional_converter_LimitedPriorityLevelConfiguration(value: Union[LimitedPriorityLevelConfigurationUnion, OmitEnum, None]) ->Union[LimitedPriorityLevelConfiguration, OmitEnum, None]:
    return LimitedPriorityLevelConfiguration(**value) if isinstance(value, dict) else value


def optional_converter_NonResourcePolicyRule(value: Union[NonResourcePolicyRuleUnion, OmitEnum, None]) ->Union[NonResourcePolicyRule, OmitEnum, None]:
    return NonResourcePolicyRule(**value) if isinstance(value, dict) else value


def optional_converter_PolicyRulesWithSubjects(value: Union[PolicyRulesWithSubjectsUnion, OmitEnum, None]) ->Union[PolicyRulesWithSubjects, OmitEnum, None]:
    return PolicyRulesWithSubjects(**value) if isinstance(value, dict) else value


def optional_converter_PriorityLevelConfigurationCondition(value: Union[PriorityLevelConfigurationConditionUnion, OmitEnum, None]) ->Union[PriorityLevelConfigurationCondition, OmitEnum, None]:
    return PriorityLevelConfigurationCondition(**value) if isinstance(value, dict) else value


def optional_converter_PriorityLevelConfigurationReference(value: Union[PriorityLevelConfigurationReferenceUnion, OmitEnum, None]) ->Union[PriorityLevelConfigurationReference, OmitEnum, None]:
    return PriorityLevelConfigurationReference(**value) if isinstance(value, dict) else value


def optional_converter_PriorityLevelConfigurationSpec(value: Union[PriorityLevelConfigurationSpecUnion, OmitEnum, None]) ->Union[PriorityLevelConfigurationSpec, OmitEnum, None]:
    return PriorityLevelConfigurationSpec(**value) if isinstance(value, dict) else value


def optional_converter_PriorityLevelConfigurationStatus(value: Union[PriorityLevelConfigurationStatusUnion, OmitEnum, None]) ->Union[PriorityLevelConfigurationStatus, OmitEnum, None]:
    return PriorityLevelConfigurationStatus(**value) if isinstance(value, dict) else value


def optional_converter_QueuingConfiguration(value: Union[QueuingConfigurationUnion, OmitEnum, None]) ->Union[QueuingConfiguration, OmitEnum, None]:
    return QueuingConfiguration(**value) if isinstance(value, dict) else value


def optional_converter_ResourcePolicyRule(value: Union[ResourcePolicyRuleUnion, OmitEnum, None]) ->Union[ResourcePolicyRule, OmitEnum, None]:
    return ResourcePolicyRule(**value) if isinstance(value, dict) else value


def optional_converter_ServiceAccountSubject(value: Union[ServiceAccountSubjectUnion, OmitEnum, None]) ->Union[ServiceAccountSubject, OmitEnum, None]:
    return ServiceAccountSubject(**value) if isinstance(value, dict) else value


def optional_converter_Subject(value: Union[SubjectUnion, OmitEnum, None]) ->Union[Subject, OmitEnum, None]:
    return Subject(**value) if isinstance(value, dict) else value


def optional_converter_UserSubject(value: Union[UserSubjectUnion, OmitEnum, None]) ->Union[UserSubject, OmitEnum, None]:
    return UserSubject(**value) if isinstance(value, dict) else value


def required_converter_FlowDistinguisherMethod(value: FlowDistinguisherMethodUnion) ->FlowDistinguisherMethod:
    return FlowDistinguisherMethod(**value) if isinstance(value, dict) else value


def required_converter_FlowSchemaCondition(value: FlowSchemaConditionUnion) ->FlowSchemaCondition:
    return FlowSchemaCondition(**value) if isinstance(value, dict) else value


def required_converter_FlowSchemaSpec(value: FlowSchemaSpecUnion) ->FlowSchemaSpec:
    return FlowSchemaSpec(**value) if isinstance(value, dict) else value


def required_converter_FlowSchemaStatus(value: FlowSchemaStatusUnion) ->FlowSchemaStatus:
    return FlowSchemaStatus(**value) if isinstance(value, dict) else value


def required_converter_GroupSubject(value: GroupSubjectUnion) ->GroupSubject:
    return GroupSubject(**value) if isinstance(value, dict) else value


def required_converter_LimitResponse(value: LimitResponseUnion) ->LimitResponse:
    return LimitResponse(**value) if isinstance(value, dict) else value


def required_converter_LimitedPriorityLevelConfiguration(value: LimitedPriorityLevelConfigurationUnion) ->LimitedPriorityLevelConfiguration:
    return LimitedPriorityLevelConfiguration(**value) if isinstance(value, dict) else value


def required_converter_NonResourcePolicyRule(value: NonResourcePolicyRuleUnion) ->NonResourcePolicyRule:
    return NonResourcePolicyRule(**value) if isinstance(value, dict) else value


def required_converter_PolicyRulesWithSubjects(value: PolicyRulesWithSubjectsUnion) ->PolicyRulesWithSubjects:
    return PolicyRulesWithSubjects(**value) if isinstance(value, dict) else value


def required_converter_PriorityLevelConfigurationCondition(value: PriorityLevelConfigurationConditionUnion) ->PriorityLevelConfigurationCondition:
    return PriorityLevelConfigurationCondition(**value) if isinstance(value, dict) else value


def required_converter_PriorityLevelConfigurationReference(value: PriorityLevelConfigurationReferenceUnion) ->PriorityLevelConfigurationReference:
    return PriorityLevelConfigurationReference(**value) if isinstance(value, dict) else value


def required_converter_PriorityLevelConfigurationSpec(value: PriorityLevelConfigurationSpecUnion) ->PriorityLevelConfigurationSpec:
    return PriorityLevelConfigurationSpec(**value) if isinstance(value, dict) else value


def required_converter_PriorityLevelConfigurationStatus(value: PriorityLevelConfigurationStatusUnion) ->PriorityLevelConfigurationStatus:
    return PriorityLevelConfigurationStatus(**value) if isinstance(value, dict) else value


def required_converter_QueuingConfiguration(value: QueuingConfigurationUnion) ->QueuingConfiguration:
    return QueuingConfiguration(**value) if isinstance(value, dict) else value


def required_converter_ResourcePolicyRule(value: ResourcePolicyRuleUnion) ->ResourcePolicyRule:
    return ResourcePolicyRule(**value) if isinstance(value, dict) else value


def required_converter_ServiceAccountSubject(value: ServiceAccountSubjectUnion) ->ServiceAccountSubject:
    return ServiceAccountSubject(**value) if isinstance(value, dict) else value


def required_converter_Subject(value: SubjectUnion) ->Subject:
    return Subject(**value) if isinstance(value, dict) else value


def required_converter_UserSubject(value: UserSubjectUnion) ->UserSubject:
    return UserSubject(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class FlowDistinguisherMethod(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})


class FlowDistinguisherMethodTypedDict(TypedDict, total=(True)):
    type: str


FlowDistinguisherMethodUnion = Union[FlowDistinguisherMethod, FlowDistinguisherMethodTypedDict]


@attr.s(kw_only=True)
class FlowSchemaCondition(K8sObject):
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    status: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'status'}, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class FlowSchemaConditionTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str
    status: str
    type: str


FlowSchemaConditionUnion = Union[FlowSchemaCondition, FlowSchemaConditionTypedDict]


@attr.s(kw_only=True)
class FlowSchemaSpec(K8sObject):
    priorityLevelConfiguration: PriorityLevelConfigurationReference = attr.ib(metadata={'yaml_name': 'priorityLevelConfiguration'}, converter=required_converter_PriorityLevelConfigurationReference)
    distinguisherMethod: Union[None, OmitEnum, FlowDistinguisherMethod] = attr.ib(metadata={'yaml_name': 'distinguisherMethod'}, converter=optional_converter_FlowDistinguisherMethod, default=OMIT)
    matchingPrecedence: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'matchingPrecedence'}, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[PolicyRulesWithSubjects]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_PolicyRulesWithSubjects, default=OMIT)


class FlowSchemaSpecOptionalTypedDict(TypedDict, total=(False)):
    distinguisherMethod: FlowDistinguisherMethod
    matchingPrecedence: int
    rules: Sequence[PolicyRulesWithSubjects]


class FlowSchemaSpecTypedDict(FlowSchemaSpecOptionalTypedDict, total=(True)):
    priorityLevelConfiguration: PriorityLevelConfigurationReference


FlowSchemaSpecUnion = Union[FlowSchemaSpec, FlowSchemaSpecTypedDict]


@attr.s(kw_only=True)
class FlowSchemaStatus(K8sObject):
    conditions: Union[None, OmitEnum, Sequence[FlowSchemaCondition]] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_list_converter_FlowSchemaCondition, default=OMIT)


class FlowSchemaStatusTypedDict(TypedDict, total=(False)):
    conditions: Sequence[FlowSchemaCondition]


FlowSchemaStatusUnion = Union[FlowSchemaStatus, FlowSchemaStatusTypedDict]


@attr.s(kw_only=True)
class GroupSubject(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class GroupSubjectTypedDict(TypedDict, total=(True)):
    name: str


GroupSubjectUnion = Union[GroupSubject, GroupSubjectTypedDict]


@attr.s(kw_only=True)
class LimitResponse(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    queuing: Union[None, OmitEnum, QueuingConfiguration] = attr.ib(metadata={'yaml_name': 'queuing'}, converter=optional_converter_QueuingConfiguration, default=OMIT)


class LimitResponseOptionalTypedDict(TypedDict, total=(False)):
    queuing: QueuingConfiguration


class LimitResponseTypedDict(LimitResponseOptionalTypedDict, total=(True)):
    type: str


LimitResponseUnion = Union[LimitResponse, LimitResponseTypedDict]


@attr.s(kw_only=True)
class LimitedPriorityLevelConfiguration(K8sObject):
    assuredConcurrencyShares: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'assuredConcurrencyShares'}, default=OMIT)
    limitResponse: Union[None, OmitEnum, LimitResponse] = attr.ib(metadata={'yaml_name': 'limitResponse'}, converter=optional_converter_LimitResponse, default=OMIT)


class LimitedPriorityLevelConfigurationTypedDict(TypedDict, total=(False)):
    assuredConcurrencyShares: int
    limitResponse: LimitResponse


LimitedPriorityLevelConfigurationUnion = Union[LimitedPriorityLevelConfiguration, LimitedPriorityLevelConfigurationTypedDict]


@attr.s(kw_only=True)
class NonResourcePolicyRule(K8sObject):
    nonResourceURLs: Sequence[str] = attr.ib(metadata={'yaml_name': 'nonResourceURLs'})
    verbs: Sequence[str] = attr.ib(metadata={'yaml_name': 'verbs'})


class NonResourcePolicyRuleTypedDict(TypedDict, total=(True)):
    nonResourceURLs: Sequence[str]
    verbs: Sequence[str]


NonResourcePolicyRuleUnion = Union[NonResourcePolicyRule, NonResourcePolicyRuleTypedDict]


@attr.s(kw_only=True)
class PolicyRulesWithSubjects(K8sObject):
    subjects: Sequence[Subject] = attr.ib(metadata={'yaml_name': 'subjects'}, converter=required_list_converter_Subject)
    nonResourceRules: Union[None, OmitEnum, Sequence[NonResourcePolicyRule]] = attr.ib(metadata={'yaml_name': 'nonResourceRules'}, converter=optional_list_converter_NonResourcePolicyRule, default=OMIT)
    resourceRules: Union[None, OmitEnum, Sequence[ResourcePolicyRule]] = attr.ib(metadata={'yaml_name': 'resourceRules'}, converter=optional_list_converter_ResourcePolicyRule, default=OMIT)


class PolicyRulesWithSubjectsOptionalTypedDict(TypedDict, total=(False)):
    nonResourceRules: Sequence[NonResourcePolicyRule]
    resourceRules: Sequence[ResourcePolicyRule]


class PolicyRulesWithSubjectsTypedDict(PolicyRulesWithSubjectsOptionalTypedDict, total=(True)):
    subjects: Sequence[Subject]


PolicyRulesWithSubjectsUnion = Union[PolicyRulesWithSubjects, PolicyRulesWithSubjectsTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationCondition(K8sObject):
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    status: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'status'}, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class PriorityLevelConfigurationConditionTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str
    status: str
    type: str


PriorityLevelConfigurationConditionUnion = Union[PriorityLevelConfigurationCondition, PriorityLevelConfigurationConditionTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationReference(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class PriorityLevelConfigurationReferenceTypedDict(TypedDict, total=(True)):
    name: str


PriorityLevelConfigurationReferenceUnion = Union[PriorityLevelConfigurationReference, PriorityLevelConfigurationReferenceTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationSpec(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    limited: Union[None, OmitEnum, LimitedPriorityLevelConfiguration] = attr.ib(metadata={'yaml_name': 'limited'}, converter=optional_converter_LimitedPriorityLevelConfiguration, default=OMIT)


class PriorityLevelConfigurationSpecOptionalTypedDict(TypedDict, total=(False)):
    limited: LimitedPriorityLevelConfiguration


class PriorityLevelConfigurationSpecTypedDict(PriorityLevelConfigurationSpecOptionalTypedDict, total=(True)):
    type: str


PriorityLevelConfigurationSpecUnion = Union[PriorityLevelConfigurationSpec, PriorityLevelConfigurationSpecTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationStatus(K8sObject):
    conditions: Union[None, OmitEnum, Sequence[PriorityLevelConfigurationCondition]] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_list_converter_PriorityLevelConfigurationCondition, default=OMIT)


class PriorityLevelConfigurationStatusTypedDict(TypedDict, total=(False)):
    conditions: Sequence[PriorityLevelConfigurationCondition]


PriorityLevelConfigurationStatusUnion = Union[PriorityLevelConfigurationStatus, PriorityLevelConfigurationStatusTypedDict]


@attr.s(kw_only=True)
class QueuingConfiguration(K8sObject):
    handSize: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'handSize'}, default=OMIT)
    queueLengthLimit: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'queueLengthLimit'}, default=OMIT)
    queues: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'queues'}, default=OMIT)


class QueuingConfigurationTypedDict(TypedDict, total=(False)):
    handSize: int
    queueLengthLimit: int
    queues: int


QueuingConfigurationUnion = Union[QueuingConfiguration, QueuingConfigurationTypedDict]


@attr.s(kw_only=True)
class ResourcePolicyRule(K8sObject):
    apiGroups: Sequence[str] = attr.ib(metadata={'yaml_name': 'apiGroups'})
    resources: Sequence[str] = attr.ib(metadata={'yaml_name': 'resources'})
    verbs: Sequence[str] = attr.ib(metadata={'yaml_name': 'verbs'})
    clusterScope: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'clusterScope'}, default=OMIT)
    namespaces: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'namespaces'}, default=OMIT)


class ResourcePolicyRuleOptionalTypedDict(TypedDict, total=(False)):
    clusterScope: bool
    namespaces: Sequence[str]


class ResourcePolicyRuleTypedDict(ResourcePolicyRuleOptionalTypedDict, total=(True)):
    apiGroups: Sequence[str]
    resources: Sequence[str]
    verbs: Sequence[str]


ResourcePolicyRuleUnion = Union[ResourcePolicyRule, ResourcePolicyRuleTypedDict]


@attr.s(kw_only=True)
class ServiceAccountSubject(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    namespace: str = attr.ib(metadata={'yaml_name': 'namespace'})


class ServiceAccountSubjectTypedDict(TypedDict, total=(True)):
    name: str
    namespace: str


ServiceAccountSubjectUnion = Union[ServiceAccountSubject, ServiceAccountSubjectTypedDict]


@attr.s(kw_only=True)
class Subject(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    group: Union[None, OmitEnum, GroupSubject] = attr.ib(metadata={'yaml_name': 'group'}, converter=optional_converter_GroupSubject, default=OMIT)
    serviceAccount: Union[None, OmitEnum, ServiceAccountSubject] = attr.ib(metadata={'yaml_name': 'serviceAccount'}, converter=optional_converter_ServiceAccountSubject, default=OMIT)
    user: Union[None, OmitEnum, UserSubject] = attr.ib(metadata={'yaml_name': 'user'}, converter=optional_converter_UserSubject, default=OMIT)


class SubjectOptionalTypedDict(TypedDict, total=(False)):
    group: GroupSubject
    serviceAccount: ServiceAccountSubject
    user: UserSubject


class SubjectTypedDict(SubjectOptionalTypedDict, total=(True)):
    kind: str


SubjectUnion = Union[Subject, SubjectTypedDict]


@attr.s(kw_only=True)
class UserSubject(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class UserSubjectTypedDict(TypedDict, total=(True)):
    name: str


UserSubjectUnion = Union[UserSubject, UserSubjectTypedDict]


@attr.s(kw_only=True)
class FlowSchema(K8sResource):
    apiVersion: ClassVar[str] = 'flowcontrol.apiserver.k8s.io/v1beta1'
    kind: ClassVar[str] = 'FlowSchema'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, FlowSchemaSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_FlowSchemaSpec, default=OMIT)
    status: Union[None, OmitEnum, FlowSchemaStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_FlowSchemaStatus, default=OMIT)


@attr.s(kw_only=True)
class PriorityLevelConfiguration(K8sResource):
    apiVersion: ClassVar[str] = 'flowcontrol.apiserver.k8s.io/v1beta1'
    kind: ClassVar[str] = 'PriorityLevelConfiguration'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PriorityLevelConfigurationSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PriorityLevelConfigurationSpec, default=OMIT)
    status: Union[None, OmitEnum, PriorityLevelConfigurationStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PriorityLevelConfigurationStatus, default=OMIT)
