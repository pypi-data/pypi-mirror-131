#!/usr/bin/env python

from grimoire.shell import shell


class FileHandler:

    """FileHandler."""

    def open_ide(self, file_to_open, for_language="python"):

        if for_language == "java":
            shell.run(f"intellij-idea-ultimate-edition {file_to_open}")
            return

        shell.run(f"pycharm {file_to_open}")

    def open_vim(self, file_to_open, new_window=True):
        """open_vim.

        :param file_to_open:
        """
        if new_window:
            shell.run(
                f'MY_TITLE=NewTerm runFunction terminalRun "myvim {file_to_open}" '
            )
        else:
            shell.run(f"myvim {file_to_open}")


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(FileHandler).start()
