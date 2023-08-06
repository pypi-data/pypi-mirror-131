from pathlib import Path
from typing import Mapping, Union
from dotenv import dotenv_values

EnvMapping = Mapping[str, str]
PathLike = Union[Path, str, bytes]


def load_env_file(path: PathLike) -> EnvMapping:
    rich_path: Path = Path(path).resolve(strict=True)
    assert rich_path.is_file(), f"{rich_path} is not a file"

    return dotenv_values(path, verbose=True)


def load_env_dir(path: PathLike) -> Mapping[str, EnvMapping]:
    rich_path: Path = Path(path).resolve(strict=True)
    assert rich_path.is_dir(), f"{rich_path} is not a directory"

    return {x.name: load_env_file(str(x)) for x in rich_path.iterdir()}
