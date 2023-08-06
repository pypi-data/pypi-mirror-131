import logging

from grimoire.decorators import notify_exception
from grimoire.desktop.clipboard import Clipboard
from grimoire.desktop.dmenu import Dmenu
from grimoire.shell import shell
from grimoire.string import chomp


class Trello:
    def add_card_dmenu(self):
        result = Dmenu("Add trello card").rofi()
        self.add_card(result)

    def add_card(self, name):
        name = chomp(name)
        cmd = f"trello add-card '{name}' '' -b JeanLife -l 'Inbox & Backlog' -q top"
        logging.info(f"Trello cmd to execute: {cmd}")
        return shell.run(cmd)

    @notify_exception()
    def clipboard(self):
        title = Clipboard().get_content()
        if len(title) < 3:
            raise Exception(f"Clipboard content is empty: {title}")

        self.add_card(title)
