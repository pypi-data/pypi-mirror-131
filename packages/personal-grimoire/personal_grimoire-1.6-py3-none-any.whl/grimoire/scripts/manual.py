#!/usr/bin/env python

from grimoire.search_run.domain.ask_question import AskQuestion
from grimoire.shell import Shell


class ManIt:
    def interactive(self):
        command = AskQuestion().ask("Give the command name")
        Shell().run(f"man {command} || ({command} --help | runFunction vman)")


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(ManIt).start()
