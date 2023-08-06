from __future__ import annotations

import attr
import json
import kdsl.core.v1

from kdsl.bases import K8sObject, K8sResource, OMIT, OmitEnum
from typing import Mapping, Union, TypedDict, Any
from base64 import b64encode


@attr.s(kw_only=True)
class RegistryAuth(K8sObject):
    login: str = attr.ib()
    password: str = attr.ib()

    def __asyaml__(self):
        string = ":".join([self.login, self.password]).encode("ascii")
        return b64encode(string).decode("ascii")


class RegistryAuthTypedDict(TypedDict, total=True):
    login: str
    password: str


RegistryAuthUnion = Union[RegistryAuth, RegistryAuthTypedDict]


def required_converter_RegistryAuth(
    value: Mapping[str, RegistryAuthUnion],
) -> Mapping[str, RegistryAuth]:
    return {
        k: RegistryAuth(**v) if isinstance(v, dict) else v for k, v in value.items()
    }


@attr.s(kw_only=True)
class RegistryAuthSecret(K8sResource):
    registries: Mapping[str, RegistryAuth] = attr.ib(
        converter=required_converter_RegistryAuth
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1.optional_converter_ObjectMeta,
        default=OMIT,
    )

    def __asyaml__(self):
        auths = {k: dict(auth=v.__asyaml__()) for k, v in self.registries.items()}
        docker_config = dict(auths=auths)
        contents = b64encode(json.dumps(docker_config).encode("ascii")).decode("ascii")
        secret = kdsl.core.v1.Secret(
            metadata=self.metadata,
            data={".dockerconfigjson": contents},
            type="kubernetes.io/dockerconfigjson",
        )
        return secret.__asyaml__()


def mk_env(
    values: Mapping[str, str] = {}, **kwargs: str
) -> Mapping[str, kdsl.core.v1.EnvVarItem]:
    return {
        k: kdsl.core.v1.EnvVarItem(value=v) for k, v in {**values, **kwargs}.items()
    }
