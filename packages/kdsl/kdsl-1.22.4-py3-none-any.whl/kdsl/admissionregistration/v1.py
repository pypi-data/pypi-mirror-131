from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.admissionregistration.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_list_converter_RuleWithOperations(value: Union[Sequence[RuleWithOperationsUnion], OmitEnum, None]) ->Union[Sequence[RuleWithOperations], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_RuleWithOperations(x) for x in value]


def optional_mlist_converter_MutatingWebhookItem(value: Union[Mapping[str, MutatingWebhookItemUnion], OmitEnum, None]) ->Union[Mapping[str, MutatingWebhookItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_MutatingWebhookItem(v) for k, v in value.items()}


def optional_mlist_converter_ValidatingWebhookItem(value: Union[Mapping[str, ValidatingWebhookItemUnion], OmitEnum, None]) ->Union[Mapping[str, ValidatingWebhookItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ValidatingWebhookItem(v) for k, v in value.items()}


def optional_converter_MutatingWebhookItem(value: Union[MutatingWebhookItemUnion, OmitEnum, None]) ->Union[MutatingWebhookItem, OmitEnum, None]:
    return MutatingWebhookItem(**value) if isinstance(value, dict) else value


def optional_converter_RuleWithOperations(value: Union[RuleWithOperationsUnion, OmitEnum, None]) ->Union[RuleWithOperations, OmitEnum, None]:
    return RuleWithOperations(**value) if isinstance(value, dict) else value


def optional_converter_ServiceReference(value: Union[ServiceReferenceUnion, OmitEnum, None]) ->Union[ServiceReference, OmitEnum, None]:
    return ServiceReference(**value) if isinstance(value, dict) else value


def optional_converter_ValidatingWebhookItem(value: Union[ValidatingWebhookItemUnion, OmitEnum, None]) ->Union[ValidatingWebhookItem, OmitEnum, None]:
    return ValidatingWebhookItem(**value) if isinstance(value, dict) else value


def optional_converter_WebhookClientConfig(value: Union[WebhookClientConfigUnion, OmitEnum, None]) ->Union[WebhookClientConfig, OmitEnum, None]:
    return WebhookClientConfig(**value) if isinstance(value, dict) else value


def required_converter_MutatingWebhookItem(value: MutatingWebhookItemUnion) ->MutatingWebhookItem:
    return MutatingWebhookItem(**value) if isinstance(value, dict) else value


def required_converter_RuleWithOperations(value: RuleWithOperationsUnion) ->RuleWithOperations:
    return RuleWithOperations(**value) if isinstance(value, dict) else value


def required_converter_ServiceReference(value: ServiceReferenceUnion) ->ServiceReference:
    return ServiceReference(**value) if isinstance(value, dict) else value


def required_converter_ValidatingWebhookItem(value: ValidatingWebhookItemUnion) ->ValidatingWebhookItem:
    return ValidatingWebhookItem(**value) if isinstance(value, dict) else value


def required_converter_WebhookClientConfig(value: WebhookClientConfigUnion) ->WebhookClientConfig:
    return WebhookClientConfig(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class MutatingWebhookItem(K8sObject):
    admissionReviewVersions: Sequence[str] = attr.ib(metadata={'yaml_name': 'admissionReviewVersions'})
    clientConfig: WebhookClientConfig = attr.ib(metadata={'yaml_name': 'clientConfig'}, converter=required_converter_WebhookClientConfig)
    sideEffects: str = attr.ib(metadata={'yaml_name': 'sideEffects'})
    failurePolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'failurePolicy'}, default=OMIT)
    matchPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'matchPolicy'}, default=OMIT)
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'namespaceSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    objectSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'objectSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    reinvocationPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reinvocationPolicy'}, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[RuleWithOperations]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_RuleWithOperations, default=OMIT)
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'timeoutSeconds'}, default=OMIT)


class MutatingWebhookItemOptionalTypedDict(TypedDict, total=(False)):
    failurePolicy: str
    matchPolicy: str
    namespaceSelector: kdsl.core.v1.LabelSelector
    objectSelector: kdsl.core.v1.LabelSelector
    reinvocationPolicy: str
    rules: Sequence[RuleWithOperations]
    timeoutSeconds: int


class MutatingWebhookItemTypedDict(MutatingWebhookItemOptionalTypedDict, total=(True)):
    admissionReviewVersions: Sequence[str]
    clientConfig: WebhookClientConfig
    sideEffects: str


MutatingWebhookItemUnion = Union[MutatingWebhookItem, MutatingWebhookItemTypedDict]


@attr.s(kw_only=True)
class RuleWithOperations(K8sObject):
    apiGroups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'apiGroups'}, default=OMIT)
    apiVersions: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'apiVersions'}, default=OMIT)
    operations: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'operations'}, default=OMIT)
    resources: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'resources'}, default=OMIT)
    scope: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'scope'}, default=OMIT)


class RuleWithOperationsTypedDict(TypedDict, total=(False)):
    apiGroups: Sequence[str]
    apiVersions: Sequence[str]
    operations: Sequence[str]
    resources: Sequence[str]
    scope: str


RuleWithOperationsUnion = Union[RuleWithOperations, RuleWithOperationsTypedDict]


@attr.s(kw_only=True)
class ServiceReference(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    namespace: str = attr.ib(metadata={'yaml_name': 'namespace'})
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    port: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'port'}, default=OMIT)


class ServiceReferenceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    port: int


class ServiceReferenceTypedDict(ServiceReferenceOptionalTypedDict, total=(True)):
    name: str
    namespace: str


ServiceReferenceUnion = Union[ServiceReference, ServiceReferenceTypedDict]


@attr.s(kw_only=True)
class ValidatingWebhookItem(K8sObject):
    admissionReviewVersions: Sequence[str] = attr.ib(metadata={'yaml_name': 'admissionReviewVersions'})
    clientConfig: WebhookClientConfig = attr.ib(metadata={'yaml_name': 'clientConfig'}, converter=required_converter_WebhookClientConfig)
    sideEffects: str = attr.ib(metadata={'yaml_name': 'sideEffects'})
    failurePolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'failurePolicy'}, default=OMIT)
    matchPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'matchPolicy'}, default=OMIT)
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'namespaceSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    objectSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(metadata={'yaml_name': 'objectSelector'}, converter=kdsl.core.v1.optional_converter_LabelSelector, default=OMIT)
    rules: Union[None, OmitEnum, Sequence[RuleWithOperations]] = attr.ib(metadata={'yaml_name': 'rules'}, converter=optional_list_converter_RuleWithOperations, default=OMIT)
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'timeoutSeconds'}, default=OMIT)


class ValidatingWebhookItemOptionalTypedDict(TypedDict, total=(False)):
    failurePolicy: str
    matchPolicy: str
    namespaceSelector: kdsl.core.v1.LabelSelector
    objectSelector: kdsl.core.v1.LabelSelector
    rules: Sequence[RuleWithOperations]
    timeoutSeconds: int


class ValidatingWebhookItemTypedDict(ValidatingWebhookItemOptionalTypedDict, total=(True)):
    admissionReviewVersions: Sequence[str]
    clientConfig: WebhookClientConfig
    sideEffects: str


ValidatingWebhookItemUnion = Union[ValidatingWebhookItem, ValidatingWebhookItemTypedDict]


@attr.s(kw_only=True)
class WebhookClientConfig(K8sObject):
    caBundle: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'caBundle'}, default=OMIT)
    service: Union[None, OmitEnum, ServiceReference] = attr.ib(metadata={'yaml_name': 'service'}, converter=optional_converter_ServiceReference, default=OMIT)
    url: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'url'}, default=OMIT)


class WebhookClientConfigTypedDict(TypedDict, total=(False)):
    caBundle: str
    service: ServiceReference
    url: str


WebhookClientConfigUnion = Union[WebhookClientConfig, WebhookClientConfigTypedDict]


@attr.s(kw_only=True)
class MutatingWebhookConfiguration(K8sResource):
    apiVersion: ClassVar[str] = 'admissionregistration.k8s.io/v1'
    kind: ClassVar[str] = 'MutatingWebhookConfiguration'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    webhooks: Union[None, OmitEnum, Mapping[str, kdsl.admissionregistration.v1.MutatingWebhookItem]] = attr.ib(metadata={'yaml_name': 'webhooks', 'mlist_key': 'name'}, converter=optional_mlist_converter_MutatingWebhookItem, default=OMIT)


@attr.s(kw_only=True)
class ValidatingWebhookConfiguration(K8sResource):
    apiVersion: ClassVar[str] = 'admissionregistration.k8s.io/v1'
    kind: ClassVar[str] = 'ValidatingWebhookConfiguration'
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    webhooks: Union[None, OmitEnum, Mapping[str, kdsl.admissionregistration.v1.ValidatingWebhookItem]] = attr.ib(metadata={'yaml_name': 'webhooks', 'mlist_key': 'name'}, converter=optional_mlist_converter_ValidatingWebhookItem, default=OMIT)
