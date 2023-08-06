#!/usr/bin/env python
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel

from grimoire.desktop.dmenu import Dmenu
from grimoire.desktop.path import Path
from grimoire.event_sourcing.message import MessageBroker
from grimoire.file import append_file_creating
from grimoire.logging import logging
from grimoire.shell import shell
from grimoire.time import Date, now_str, today_str
from grimoire.time.date import durantion_between_dates

BALANCE_CSV = "/data/grimoire/timewise/domoredoless.csv"
PRIORITIES_CSV = "/data/grimoire/timewise/prioritites.csv"


class Focus:
    def set_new(self):
        focus_title = Dmenu(
            title="New focus:",
            options_file=FileProjectionBuilder.destination,
            accept_empty=False,
        ).rofi()
        event = NewFocus(**{"focus_on": focus_title})

        broker = MessageBroker(TOPIC_NAME)
        broker.register_consumer(
            FileProjectionBuilder().append, catchup_on_history=False
        )
        broker.produce(event.dict())

    def get_current_foucs(self) -> Tuple[str, int]:
        focus = MessageBroker(TOPIC_NAME).consume_last()
        if not focus:
            raise Exception("No focus entry registered")

        now = Date.now()
        execution_date = Date.from_str(focus["generated_date"])
        duration = durantion_between_dates(execution_date, now)
        minutes = duration["minutes"]
        focus_on = focus["focus_on"]

        return focus_on, minutes

    def get_points(self):

        focus = pd.read_json("/data/grimoire/message_topics/focus_entries", lines=True)
        focus = focus.astype({"generated_date": "datetime64"})

        focus_today = focus[(focus["generated_date"] >= today_str())]
        if focus_today.shape[0] == 0:
            return 0

        focus_today["time_spent"] = focus_today.iloc[
            ::-1
        ].generated_date.diff() / np.timedelta64(1, "m")
        focus_today["time_spent"] = focus_today["time_spent"].abs()

        focus_today.at[focus_today.index[-1], "time_spent"] = (
            pd.Timestamp(now_str()) - focus_today.iloc[-1]["generated_date"]
        ) / pd.Timedelta(minutes=1)

        balance = pd.read_csv(BALANCE_CSV)

        focus_on_balance = self.merge_dfs(balance, "What", focus_today, "focus_on")

        score = 0
        score = self.get_priorities_score(score, focus_today)

        for index, row in focus_on_balance.iterrows():
            score += 10 * row["More / Less"] * row["time_spent"]

        return int(score)

    def get_priorities_score(self, score, focus_today):
        priorities = pd.read_csv(PRIORITIES_CSV)
        priorities = priorities.astype({"Date": "datetime64"})
        priorities = priorities[(priorities["Date"] >= today_str())]

        if priorities.shape[0] == 0:
            return score

        priorities = priorities.melt(
            id_vars=["Date"], var_name="Order", value_name="What"
        )

        priorities = priorities.dropna()

        focus_on_priorities = self.merge_dfs(
            priorities, "What", focus_today, "focus_on"
        )

        for index, row in focus_on_priorities.iterrows():
            if row["Order"] == "First":
                score += 1 * 10 * row["time_spent"]
            if row["Order"] == "Second":
                score += 1 * 7 * row["time_spent"]
            if row["Order"] == "Third":
                score += 1 * 5 * row["time_spent"]
            if row["Order"] == "Fourth":
                score += 1 * 3 * row["time_spent"]
            if row["Order"] == "Fifth":
                score += 1 * 2 * row["time_spent"]

        return score

    def merge_dfs(self, df1, df1_col, df2, df2_col):
        df1["join"] = 1
        df2["join"] = 1

        dfFull = df1.merge(df2, on="join").drop("join", axis=1)
        df2.drop("join", axis=1)

        dfFull["match"] = dfFull.apply(
            lambda x: x[df1_col].lower().find(x[df2_col].lower()), axis=1
        ).ge(0)
        return dfFull[dfFull.match]

    def get_status_summary(self):
        import json

        state = "Info"
        return json.dumps(
            {
                "text": f"X: {self.get_points()}",
                "state": state,
            }
        )

    def download_files(self):
        shell.run(
            'ls /home/jean/Downloads/Personal\ Backlog* | xargs -i rm -rf "{}" || true'
        )
        shell.run_with_result(
            "google-chrome "
            "'https://docs.google.com/spreadsheets/d/1rr4loFkBOCfdleAkXR9zOwGCwR73oWBLCSbQmO65mXk/export?format=csv&gid=1562844218'"
        )
        shell.run_with_result(
            "google-chrome 'https://docs.google.com/spreadsheets/d/1rr4loFkBOCfdleAkXR9zOwGCwR73oWBLCSbQmO65mXk/export?format=csv&gid=4959025'"
        )

        import time

        time.sleep(3)

        shell.run(
            f"mv '/home/jean/Downloads/Personal Backlog - Priorities.csv' {PRIORITIES_CSV}"
        )
        shell.run(
            f"mv '/home/jean/Downloads/Personal Backlog - DoMoreDoLess.csv' {BALANCE_CSV}"
        )


TOPIC_NAME = "focus_entries"


class NewFocus(BaseModel):
    focus_on: str


class FileProjectionBuilder:
    destination = f"{Path.GRIMOIRE}/grimoire/desktop/focus/history_projection.txt"

    def append(self, event):
        entry = f"{event['focus_on']}\n"
        append_file_creating(self.destination, entry)
        logging.info(f"Playing event: {event}")


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Focus).start()
