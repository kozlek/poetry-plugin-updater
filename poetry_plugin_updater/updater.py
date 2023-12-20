from __future__ import annotations

import string
from typing import TYPE_CHECKING, Any

import requests

if TYPE_CHECKING:
    from tomlkit import TOMLDocument

PYPI_URL_TEMPLATE = "https://pypi.org/pypi/%(project)s/json"


def get_updated_version(project: str, version: str) -> str:
    for i, c in enumerate(version):
        if c in string.digits:
            index = i
            break
    else:
        raise ValueError(f"Cannot parse `{version}`.")

    latest_version = requests.get(PYPI_URL_TEMPLATE % {"project": project}).json()["info"]["version"]
    return f"{version[:index]}{latest_version}"


def update_dependencies_group(deps: dict[str, Any]) -> None:
    for project, version_or_dict in deps.items():
        if project == "python":
            continue

        if isinstance(version_or_dict, str):
            deps[project] = get_updated_version(project, version_or_dict)
        else:
            version_or_dict["version"] = get_updated_version(project, version_or_dict["version"])


def update_pyproject_file(pyproject_file: TOMLDocument) -> None:
    poetry_content = pyproject_file["tool"]["poetry"]

    update_dependencies_group(poetry_content["dependencies"])
    for group, group_data in poetry_content.get("group", {}).items():
        if dependencies := group_data.get("dependencies"):
            update_dependencies_group(dependencies)
