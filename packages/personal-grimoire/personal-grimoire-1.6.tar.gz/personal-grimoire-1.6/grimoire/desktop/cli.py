#!/usr/bin/env python

import fire

from grimoire import Logger
from grimoire.desktop.trello import Trello
from grimoire.desktop.web_search import SearchIt


class DesktopCli:
    def __init__(self):
        Logger()
        self.search = SearchIt
        self.trello = Trello


if __name__ == "__main__":
    fire.Fire(DesktopCli)
