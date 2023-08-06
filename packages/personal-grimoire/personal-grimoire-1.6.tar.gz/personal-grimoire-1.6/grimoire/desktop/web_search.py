import logging

from grimoire.decorators import notify_exception
from grimoire.desktop.browser import Browser
from grimoire.desktop.clipboard import Clipboard
from grimoire.desktop.dmenu import Dmenu
from grimoire.desktop.path import Path
from grimoire.event_sourcing.message import MessageBroker
from grimoire.file import append_file_creating
from grimoire.notification import notify_send
from grimoire.shell import shell
from grimoire.string import emptish


class FileProjectionBuilder:
    destination = f"{Path.GRIMOIRE}/grimoire/desktop/history_projection.txt"

    def append(self, event):
        entry = f"{event['query']}\n"
        append_file_creating(self.destination, entry)
        logging.info(f"Playing event: {event}")


class SearchIt:
    def dmenu(self):

        query = Dmenu(
            "Google term", options_file=FileProjectionBuilder.destination
        ).rofi()

        if emptish(query):
            notify_send("Empty query. quitting")
            return

        event_sourcing = MessageBroker("search_queries")
        event_sourcing.register_consumer(
            FileProjectionBuilder().append, catchup_on_history=False
        )
        event_sourcing.produce({"query": query})

        self.search(query)

    def search(self, term: str):
        logging.info(f"Matched search, term: {term}")
        return shell.run_command_no_wait(f"runFunction googleIt '{term}'")

    @notify_exception()
    def clipboard(self):
        content = Clipboard().get_content()
        if len(content) < 3:
            raise Exception(f"Clipboard content is empty: {content}")

        self.search(content)

    @notify_exception()
    def maps_clipboard(self):
        content = Clipboard().get_content()
        if len(content) < 3:
            raise Exception(f"Clipboard content is empty: {content}")

        Clipboard().set_content(content)
        Browser().open(f"https://www.google.com/maps/place/{content}")
