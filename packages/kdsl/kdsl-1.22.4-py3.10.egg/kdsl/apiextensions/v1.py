from __future__ import annotations
import kdsl.apiextensions.v1
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_list_converter_CustomResourceColumnDefinition(value: Union[Sequence[CustomResourceColumnDefinitionUnion], OmitEnum, None]) ->Union[Sequence[CustomResourceColumnDefinition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceColumnDefinition(x) for x in value]


def optional_list_converter_CustomResourceDefinitionCondition(value: Union[Sequence[CustomResourceDefinitionConditionUnion], OmitEnum, None]) ->Union[Sequence[CustomResourceDefinitionCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceDefinitionCondition(x) for x in value]


def required_list_converter_CustomResourceDefinitionVersion(value: Sequence[CustomResourceDefinitionVersionUnion]) ->Sequence[CustomResourceDefinitionVersion]:
    return [required_converter_CustomResourceDefinitionVersion(x) for x in value]


def optional_converter_CustomResourceColumnDefinition(value: Union[CustomResourceColumnDefinitionUnion, OmitEnum, None]) ->Union[CustomResourceColumnDefinition, OmitEnum, None]:
    return CustomResourceColumnDefinition(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceConversion(value: Union[CustomResourceConversionUnion, OmitEnum, None]) ->Union[CustomResourceConversion, OmitEnum, None]:
    return CustomResourceConversion(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceDefinitionCondition(value: Union[CustomResourceDefinitionConditionUnion, OmitEnum, None]) ->Union[CustomResourceDefinitionCondition, OmitEnum, None]:
    return CustomResourceDefinitionCondition(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceDefinitionNames(value: Union[CustomResourceDefinitionNamesUnion, OmitEnum, None]) ->Union[CustomResourceDefinitionNames, OmitEnum, None]:
    return CustomResourceDefinitionNames(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceDefinitionSpec(value: Union[CustomResourceDefinitionSpecUnion, OmitEnum, None]) ->Union[CustomResourceDefinitionSpec, OmitEnum, None]:
    return CustomResourceDefinitionSpec(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceDefinitionStatus(value: Union[CustomResourceDefinitionStatusUnion, OmitEnum, None]) ->Union[CustomResourceDefinitionStatus, OmitEnum, None]:
    return CustomResourceDefinitionStatus(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceDefinitionVersion(value: Union[CustomResourceDefinitionVersionUnion, OmitEnum, None]) ->Union[CustomResourceDefinitionVersion, OmitEnum, None]:
    return CustomResourceDefinitionVersion(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceSubresourceScale(value: Union[CustomResourceSubresourceScaleUnion, OmitEnum, None]) ->Union[CustomResourceSubresourceScale, OmitEnum, None]:
    return CustomResourceSubresourceScale(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceSubresources(value: Union[CustomResourceSubresourcesUnion, OmitEnum, None]) ->Union[CustomResourceSubresources, OmitEnum, None]:
    return CustomResourceSubresources(**value) if isinstance(value, dict) else value


def optional_converter_CustomResourceValidation(value: Union[CustomResourceValidationUnion, OmitEnum, None]) ->Union[CustomResourceValidation, OmitEnum, None]:
    return CustomResourceValidation(**value) if isinstance(value, dict) else value


def optional_converter_ServiceReference(value: Union[ServiceReferenceUnion, OmitEnum, None]) ->Union[ServiceReference, OmitEnum, None]:
    return ServiceReference(**value) if isinstance(value, dict) else value


def optional_converter_WebhookClientConfig(value: Union[WebhookClientConfigUnion, OmitEnum, None]) ->Union[WebhookClientConfig, OmitEnum, None]:
    return WebhookClientConfig(**value) if isinstance(value, dict) else value


def optional_converter_WebhookConversion(value: Union[WebhookConversionUnion, OmitEnum, None]) ->Union[WebhookConversion, OmitEnum, None]:
    return WebhookConversion(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceColumnDefinition(value: CustomResourceColumnDefinitionUnion) ->CustomResourceColumnDefinition:
    return CustomResourceColumnDefinition(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceConversion(value: CustomResourceConversionUnion) ->CustomResourceConversion:
    return CustomResourceConversion(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceDefinitionCondition(value: CustomResourceDefinitionConditionUnion) ->CustomResourceDefinitionCondition:
    return CustomResourceDefinitionCondition(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceDefinitionNames(value: CustomResourceDefinitionNamesUnion) ->CustomResourceDefinitionNames:
    return CustomResourceDefinitionNames(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceDefinitionSpec(value: CustomResourceDefinitionSpecUnion) ->CustomResourceDefinitionSpec:
    return CustomResourceDefinitionSpec(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceDefinitionStatus(value: CustomResourceDefinitionStatusUnion) ->CustomResourceDefinitionStatus:
    return CustomResourceDefinitionStatus(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceDefinitionVersion(value: CustomResourceDefinitionVersionUnion) ->CustomResourceDefinitionVersion:
    return CustomResourceDefinitionVersion(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceSubresourceScale(value: CustomResourceSubresourceScaleUnion) ->CustomResourceSubresourceScale:
    return CustomResourceSubresourceScale(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceSubresources(value: CustomResourceSubresourcesUnion) ->CustomResourceSubresources:
    return CustomResourceSubresources(**value) if isinstance(value, dict) else value


def required_converter_CustomResourceValidation(value: CustomResourceValidationUnion) ->CustomResourceValidation:
    return CustomResourceValidation(**value) if isinstance(value, dict) else value


def required_converter_ServiceReference(value: ServiceReferenceUnion) ->ServiceReference:
    return ServiceReference(**value) if isinstance(value, dict) else value


def required_converter_WebhookClientConfig(value: WebhookClientConfigUnion) ->WebhookClientConfig:
    return WebhookClientConfig(**value) if isinstance(value, dict) else value


def required_converter_WebhookConversion(value: WebhookConversionUnion) ->WebhookConversion:
    return WebhookConversion(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class CustomResourceColumnDefinition(K8sObject):
    jsonPath: str = attr.ib(metadata={'yaml_name': 'jsonPath'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    description: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'description'}, default=OMIT)
    format: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'format'}, default=OMIT)
    priority: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'priority'}, default=OMIT)


class CustomResourceColumnDefinitionOptionalTypedDict(TypedDict, total=(False)):
    description: str
    format: str
    priority: int


class CustomResourceColumnDefinitionTypedDict(CustomResourceColumnDefinitionOptionalTypedDict, total=(True)):
    jsonPath: str
    name: str
    type: str


CustomResourceColumnDefinitionUnion = Union[CustomResourceColumnDefinition, CustomResourceColumnDefinitionTypedDict]


@attr.s(kw_only=True)
class CustomResourceConversion(K8sObject):
    strategy: str = attr.ib(metadata={'yaml_name': 'strategy'})
    webhook: Union[None, OmitEnum, WebhookConversion] = attr.ib(metadata={'yaml_name': 'webhook'}, converter=optional_converter_WebhookConversion, default=OMIT)


class CustomResourceConversionOptionalTypedDict(TypedDict, total=(False)):
    webhook: WebhookConversion


class CustomResourceConversionTypedDict(CustomResourceConversionOptionalTypedDict, total=(True)):
    strategy: str


CustomResourceConversionUnion = Union[CustomResourceConversion, CustomResourceConversionTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionCondition(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class CustomResourceDefinitionConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class CustomResourceDefinitionConditionTypedDict(CustomResourceDefinitionConditionOptionalTypedDict, total=(True)):
    status: str
    type: str


CustomResourceDefinitionConditionUnion = Union[CustomResourceDefinitionCondition, CustomResourceDefinitionConditionTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionNames(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    plural: str = attr.ib(metadata={'yaml_name': 'plural'})
    categories: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'categories'}, default=OMIT)
    listKind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'listKind'}, default=OMIT)
    shortNames: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'shortNames'}, default=OMIT)
    singular: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'singular'}, default=OMIT)


class CustomResourceDefinitionNamesOptionalTypedDict(TypedDict, total=(False)):
    categories: Sequence[str]
    listKind: str
    shortNames: Sequence[str]
    singular: str


class CustomResourceDefinitionNamesTypedDict(CustomResourceDefinitionNamesOptionalTypedDict, total=(True)):
    kind: str
    plural: str


CustomResourceDefinitionNamesUnion = Union[CustomResourceDefinitionNames, CustomResourceDefinitionNamesTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionSpec(K8sObject):
    group: str = attr.ib(metadata={'yaml_name': 'group'})
    names: CustomResourceDefinitionNames = attr.ib(metadata={'yaml_name': 'names'}, converter=required_converter_CustomResourceDefinitionNames)
    scope: str = attr.ib(metadata={'yaml_name': 'scope'})
    versions: Sequence[CustomResourceDefinitionVersion] = attr.ib(metadata={'yaml_name': 'versions'}, converter=required_list_converter_CustomResourceDefinitionVersion)
    conversion: Union[None, OmitEnum, CustomResourceConversion] = attr.ib(metadata={'yaml_name': 'conversion'}, converter=optional_converter_CustomResourceConversion, default=OMIT)
    preserveUnknownFields: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'preserveUnknownFields'}, default=OMIT)


class CustomResourceDefinitionSpecOptionalTypedDict(TypedDict, total=(False)):
    conversion: CustomResourceConversion
    preserveUnknownFields: bool


class CustomResourceDefinitionSpecTypedDict(CustomResourceDefinitionSpecOptionalTypedDict, total=(True)):
    group: str
    names: CustomResourceDefinitionNames
    scope: str
    versions: Sequence[CustomResourceDefinitionVersion]


CustomResourceDefinitionSpecUnion = Union[CustomResourceDefinitionSpec, CustomResourceDefinitionSpecTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionStatus(K8sObject):
    acceptedNames: Union[None, OmitEnum, CustomResourceDefinitionNames] = attr.ib(metadata={'yaml_name': 'acceptedNames'}, converter=optional_converter_CustomResourceDefinitionNames, default=OMIT)
    conditions: Union[None, OmitEnum, Sequence[CustomResourceDefinitionCondition]] = attr.ib(metadata={'yaml_name': 'conditions'}, converter=optional_list_converter_CustomResourceDefinitionCondition, default=OMIT)
    storedVersions: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'storedVersions'}, default=OMIT)


class CustomResourceDefinitionStatusTypedDict(TypedDict, total=(False)):
    acceptedNames: CustomResourceDefinitionNames
    conditions: Sequence[CustomResourceDefinitionCondition]
    storedVersions: Sequence[str]


CustomResourceDefinitionStatusUnion = Union[CustomResourceDefinitionStatus, CustomResourceDefinitionStatusTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionVersion(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    served: bool = attr.ib(metadata={'yaml_name': 'served'})
    storage: bool = attr.ib(metadata={'yaml_name': 'storage'})
    additionalPrinterColumns: Union[None, OmitEnum, Sequence[CustomResourceColumnDefinition]] = attr.ib(metadata={'yaml_name': 'additionalPrinterColumns'}, converter=optional_list_converter_CustomResourceColumnDefinition, default=OMIT)
    deprecated: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'deprecated'}, default=OMIT)
    deprecationWarning: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'deprecationWarning'}, default=OMIT)
    schema: Union[None, OmitEnum, CustomResourceValidation] = attr.ib(metadata={'yaml_name': 'schema'}, converter=optional_converter_CustomResourceValidation, default=OMIT)
    subresources: Union[None, OmitEnum, CustomResourceSubresources] = attr.ib(metadata={'yaml_name': 'subresources'}, converter=optional_converter_CustomResourceSubresources, default=OMIT)


class CustomResourceDefinitionVersionOptionalTypedDict(TypedDict, total=(False)):
    additionalPrinterColumns: Sequence[CustomResourceColumnDefinition]
    deprecated: bool
    deprecationWarning: str
    schema: CustomResourceValidation
    subresources: CustomResourceSubresources


class CustomResourceDefinitionVersionTypedDict(CustomResourceDefinitionVersionOptionalTypedDict, total=(True)):
    name: str
    served: bool
    storage: bool


CustomResourceDefinitionVersionUnion = Union[CustomResourceDefinitionVersion, CustomResourceDefinitionVersionTypedDict]


@attr.s(kw_only=True)
class CustomResourceSubresourceScale(K8sObject):
    specReplicasPath: str = attr.ib(metadata={'yaml_name': 'specReplicasPath'})
    statusReplicasPath: str = attr.ib(metadata={'yaml_name': 'statusReplicasPath'})
    labelSelectorPath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'labelSelectorPath'}, default=OMIT)


class CustomResourceSubresourceScaleOptionalTypedDict(TypedDict, total=(False)):
    labelSelectorPath: str


class CustomResourceSubresourceScaleTypedDict(CustomResourceSubresourceScaleOptionalTypedDict, total=(True)):
    specReplicasPath: str
    statusReplicasPath: str


CustomResourceSubresourceScaleUnion = Union[CustomResourceSubresourceScale, CustomResourceSubresourceScaleTypedDict]


@attr.s(kw_only=True)
class CustomResourceSubresources(K8sObject):
    scale: Union[None, OmitEnum, CustomResourceSubresourceScale] = attr.ib(metadata={'yaml_name': 'scale'}, converter=optional_converter_CustomResourceSubresourceScale, default=OMIT)
    status: Union[None, OmitEnum, Mapping[str, Any]] = attr.ib(metadata={'yaml_name': 'status'}, default=OMIT)


class CustomResourceSubresourcesTypedDict(TypedDict, total=(False)):
    scale: CustomResourceSubresourceScale
    status: Mapping[str, Any]


CustomResourceSubresourcesUnion = Union[CustomResourceSubresources, CustomResourceSubresourcesTypedDict]


@attr.s(kw_only=True)
class CustomResourceValidation(K8sObject):
    openAPIV3Schema: Union[None, OmitEnum, Any] = attr.ib(metadata={'yaml_name': 'openAPIV3Schema'}, default=OMIT)


class CustomResourceValidationTypedDict(TypedDict, total=(False)):
    openAPIV3Schema: Any


CustomResourceValidationUnion = Union[CustomResourceValidation, CustomResourceValidationTypedDict]


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
class WebhookConversion(K8sObject):
    conversionReviewVersions: Sequence[str] = attr.ib(metadata={'yaml_name': 'conversionReviewVersions'})
    clientConfig: Union[None, OmitEnum, WebhookClientConfig] = attr.ib(metadata={'yaml_name': 'clientConfig'}, converter=optional_converter_WebhookClientConfig, default=OMIT)


class WebhookConversionOptionalTypedDict(TypedDict, total=(False)):
    clientConfig: WebhookClientConfig


class WebhookConversionTypedDict(WebhookConversionOptionalTypedDict, total=(True)):
    conversionReviewVersions: Sequence[str]


WebhookConversionUnion = Union[WebhookConversion, WebhookConversionTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinition(K8sResource):
    apiVersion: ClassVar[str] = 'apiextensions.k8s.io/v1'
    kind: ClassVar[str] = 'CustomResourceDefinition'
    spec: CustomResourceDefinitionSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_CustomResourceDefinitionSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, CustomResourceDefinitionStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_CustomResourceDefinitionStatus, default=OMIT)
