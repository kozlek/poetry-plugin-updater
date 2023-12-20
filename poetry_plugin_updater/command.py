from __future__ import annotations

from poetry.console.commands.group_command import GroupCommand

from .updater import update_pyproject_file


class UpdaterCommand(GroupCommand):
    name = "updater"
    description = "Update pyproject.toml dependency versions to the latest."

    def handle(self) -> int:
        pyproject_file = self.poetry.pyproject.data
        update_pyproject_file(pyproject_file)
        self.poetry.file.write(pyproject_file)
        return 0
