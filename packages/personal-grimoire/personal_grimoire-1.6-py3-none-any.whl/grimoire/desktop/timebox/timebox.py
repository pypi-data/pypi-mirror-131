#!/usr/bin/env python

import logging
import time

import grimoire as g
from grimoire import append_file
from grimoire.desktop.dmenu import Dmenu
from grimoire.shell import Shell
from grimoire.time import Date


class Timebox:
    LOG_FILE = "/home/jean/projects/git_private/timebox_log"

    def __init__(self):
        self.seconds_ellapsed = 0

    def box(self, time):
        self._run(time)

    def dmenu_box(self):

        time = Dmenu(f"Time in minutes: ").rofi()
        logging.info(f"Time specified: {time}")

        self.box(time)

    def _run(self, amount_of_time_min, sound=True):

        if type(amount_of_time_min) == str:
            amount_of_time_min = int(amount_of_time_min)

        entry = f'"timestamp": "{Date.now_str(datetime_format=True)}", "amount_of_time_min": {amount_of_time_min}'
        append_file(Timebox.LOG_FILE, "\n{" + entry + "}")

        time_in_seconds = amount_of_time_min * 60

        self.seconds_ellapsed = 0
        while self.seconds_ellapsed < time_in_seconds:
            percentage_ellapsed = int(self.seconds_ellapsed * 100 / time_in_seconds)
            print(
                "\r"
                + f"Time ellapsed: {g.seconds_to_str(self.seconds_ellapsed)} , Percentage ellapsed {percentage_ellapsed}%",
                end="",
            )
            time.sleep(1)
            self.seconds_ellapsed += 1
        g.notify_send("Box of time over")

        if sound:
            Shell().run_command_no_wait("mpv ~/.timebox_over.mp3")

    def get_time_ellapsed_min(self):
        return self.seconds_ellapsed / 60


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_grimoire_logger().with_fire(Timebox).start()
