from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.plugins.application_plugin import ApplicationPlugin

from .command import UpdaterCommand


if TYPE_CHECKING:
    from poetry.console.commands.command import Command


class UpdaterApplicationPlugin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [UpdaterCommand]
