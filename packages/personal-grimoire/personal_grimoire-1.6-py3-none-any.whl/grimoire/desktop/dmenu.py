import logging
from subprocess import CalledProcessError
from typing import Optional

from grimoire.file import append_file
from grimoire.shell import shell as s
from grimoire.string import chomp, emptish


class Dmenu:
    def __init__(
        self, title="Run: ", history_file=None, options_file=None, accept_empty=False, lines=None
    ):
        self.title = title
        self.history_file = history_file
        self.accept_empty = accept_empty
        self.options_file = options_file
        self.lines = lines

    def rofi(
        self, get_options_cmd: Optional[str] = None, accept_empty: Optional[bool] = None
    ) -> str:

        if accept_empty != None:
            self.accept_empty = accept_empty

        entries_cmd = ""
        if self.history_file:
            entries_cmd = f"tac {self.history_file} | "
        if self.options_file:
            entries_cmd = f"tac {self.options_file} | "


        lines_cmd = " "
        if self.lines != None:
            lines_cmd = f" -l {self.lines} "

        # Tried things that did not work:
        cmd = f"""{entries_cmd} nice -19 rofi\
          -width 1000\
          {lines_cmd} \
          -no-filter\
          -no-lazy-grab -i\
          -show-match\
          -no-sort\
          -dpi 120\
          -no-levenshtein-sort\
          -sorting-method fzf\
          -dmenu\
          -p '{self.title}'"""

        if get_options_cmd:
            cmd = f"{get_options_cmd} | {cmd}"

        try:
            result = s.check_output(cmd)
        except CalledProcessError:
            result = ""
            return result

        logging.info(f"Rofi result: {result}")

        result = chomp(result)
        if emptish(result) and not self.accept_empty:
            raise MenuException.given_empty_value()

        if self.history_file:
            append_file(self.history_file, f"\n{result}\n")

        return result

    def fzf(self, rows):
        self.run_on_terminal = True

        cmd = f"{rows}  | nice -19 fzf"

        logging.info(f"Final cmd: {cmd}")
        return s.run_with_result(cmd)


class MenuException(Exception):
    config = {
        "disable_tray_message": True,
        "enable_notification": True,
        "disable_sentry": True,
    }

    @staticmethod
    def given_empty_value():
        return MenuException("No option selected in rofi!")
