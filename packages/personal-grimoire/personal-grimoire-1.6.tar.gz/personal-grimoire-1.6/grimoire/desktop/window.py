import logging

from grimoire.shell import shell


class Window:
    """ Responsible for finding the right window to focus on"""

    def focus(self, match, match_type="title", focus_last=False) -> bool:

        """returns true if succeeded"""
        if match_type == "title":
            cmd = f'wmctrl -a "{match}" '
        elif match_type == "class":
            cmd = f'wmctrl -a "{match}" -x '
        elif focus_last:
            cmd = f"focus_last.sh {match}"
        else:
            cmd = f'wmctrl -a "{match}" || wmctrl -a "{match} -x" '

        result = shell.run_command(cmd)

        logging.info(f"Attempt to focus on window command '{cmd}', result: '{result}'")

        if result:
            logging.info("Match succeded")
        else:
            logging.info("Match failed")

        return result
