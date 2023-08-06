#!/usr/bin/env python

import json
from json import dumps
from typing import Literal

from grimoire.cicd.quality_assurance import ResultOfQATest
from grimoire.desktop.focus.cli import Focus
from grimoire.desktop.performance.cpu import CPU
from grimoire.event_sourcing.message import MessageBroker
from grimoire.having_time.main import HavingTime
from grimoire.logging import logging
from grimoire.time import Date, durantion_between_dates

StatusType = Literal["Info", "Good", "Warning", "Critical"]


class StatusBar:
    @staticmethod
    def time_left():
        time = HavingTime()
        text = f"T: %.2f, Wt: %.2f, Hw: %.2f" % (
            time.get_hours_left_today(),
            time.work.hours_left_today(),
            time.work.hours_week_left(),
        )
        return json.dumps(
            {
                "text": text,
            }
        )

    @staticmethod
    def cpu_frequency():
        frequency = CPU().get_frequency()
        frequency = frequency / 1000

        state: StatusType = "Good"
        if frequency > 2.0:
            state = "Info"
        if frequency < 1.8:
            state = "Warning"
        if frequency < 1.5:
            state: StatusType = "Critical"

        logging.info({"cpu_frequency": frequency})

        return json.dumps(
            {
                "text": "%.1fGHz" % frequency,
                "state": state,
            }
        )

    @staticmethod
    def focus():
        focus_description, duration = Focus().get_current_foucs()

        result = {
            "text": f"{focus_description} ({duration} min)",
        }

        return dumps(result)

    def get_test_results(self):
        """
        Return the results of the latest execution of grimoire tests

        """

        run_details = MessageBroker(ResultOfQATest.TOPIC_NAME).consume_last()

        now = Date.now()
        execution_date = Date.from_str(run_details["generated_date"])
        duration = durantion_between_dates(execution_date, now)

        state = "Critical"
        status = "Fail"
        if run_details["test_succeeded"]:
            state = "Good"
            status = "Ok"

        result = {
            "text": f"{duration['minutes']}",
            "state": state,
        }
        from json import dumps

        return dumps(result)


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(StatusBar).start()
