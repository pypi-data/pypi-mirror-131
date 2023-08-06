import logging

from grimoire.decorators import log_call
from grimoire.shell import shell
from grimoire.string import generate_identifier


class Shortcut:
    def reset(self):
        """ reset existing shortcuts, necesary only for gnome"""
        shell.run_command(
            "gsettings reset-recursively org.gnome.settings-daemon.plugins.media-keys"
        )

    @log_call
    def register(self, cmd, shortcut):
        name = generate_identifier(cmd)
        shortcut_cmd = f'set_custom_shortcut.py "{name}" "{cmd}" "{shortcut}"'
        logging.info(f"Register shortcut command: {shortcut_cmd}")
        shell.run_command(shortcut_cmd)


class FromGnomeToI3:
    pass
