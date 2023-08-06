from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.authentication.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, Literal, ClassVar
from kdsl.bases import K8sResource, OmitEnum, OMIT, K8sObject


def optional_converter_TokenReviewSpec(value: Union[TokenReviewSpecUnion, OmitEnum, None]) ->Union[TokenReviewSpec, OmitEnum, None]:
    return TokenReviewSpec(**value) if isinstance(value, dict) else value


def optional_converter_TokenReviewStatus(value: Union[TokenReviewStatusUnion, OmitEnum, None]) ->Union[TokenReviewStatus, OmitEnum, None]:
    return TokenReviewStatus(**value) if isinstance(value, dict) else value


def optional_converter_UserInfo(value: Union[UserInfoUnion, OmitEnum, None]) ->Union[UserInfo, OmitEnum, None]:
    return UserInfo(**value) if isinstance(value, dict) else value


def required_converter_TokenReviewSpec(value: TokenReviewSpecUnion) ->TokenReviewSpec:
    return TokenReviewSpec(**value) if isinstance(value, dict) else value


def required_converter_TokenReviewStatus(value: TokenReviewStatusUnion) ->TokenReviewStatus:
    return TokenReviewStatus(**value) if isinstance(value, dict) else value


def required_converter_UserInfo(value: UserInfoUnion) ->UserInfo:
    return UserInfo(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class TokenReviewSpec(K8sObject):
    audiences: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'audiences'}, default=OMIT)
    token: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'token'}, default=OMIT)


class TokenReviewSpecTypedDict(TypedDict, total=(False)):
    audiences: Sequence[str]
    token: str


TokenReviewSpecUnion = Union[TokenReviewSpec, TokenReviewSpecTypedDict]


@attr.s(kw_only=True)
class TokenReviewStatus(K8sObject):
    audiences: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'audiences'}, default=OMIT)
    authenticated: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'authenticated'}, default=OMIT)
    error: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'error'}, default=OMIT)
    user: Union[None, OmitEnum, UserInfo] = attr.ib(metadata={'yaml_name': 'user'}, converter=optional_converter_UserInfo, default=OMIT)


class TokenReviewStatusTypedDict(TypedDict, total=(False)):
    audiences: Sequence[str]
    authenticated: bool
    error: str
    user: UserInfo


TokenReviewStatusUnion = Union[TokenReviewStatus, TokenReviewStatusTypedDict]


@attr.s(kw_only=True)
class UserInfo(K8sObject):
    extra: Union[None, OmitEnum, Mapping[str, Sequence[str]]] = attr.ib(metadata={'yaml_name': 'extra'}, default=OMIT)
    groups: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'groups'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)
    username: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'username'}, default=OMIT)


class UserInfoTypedDict(TypedDict, total=(False)):
    extra: Mapping[str, Sequence[str]]
    groups: Sequence[str]
    uid: str
    username: str


UserInfoUnion = Union[UserInfo, UserInfoTypedDict]


@attr.s(kw_only=True)
class TokenReview(K8sResource):
    apiVersion: ClassVar[str] = 'authentication.k8s.io/v1beta1'
    kind: ClassVar[str] = 'TokenReview'
    spec: TokenReviewSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_TokenReviewSpec)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    status: Union[None, OmitEnum, TokenReviewStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_TokenReviewStatus, default=OMIT)
