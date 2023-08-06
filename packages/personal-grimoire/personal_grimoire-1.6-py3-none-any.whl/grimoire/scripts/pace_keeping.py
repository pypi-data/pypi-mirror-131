#!/usr/bin/env python

from __future__ import annotations

from json import dumps

from grimoire.databases.cache import Cache
from grimoire.event_sourcing.message import MessageBroker
from grimoire.notification import send_notification
from grimoire.pace_keeping.goals import goals
from grimoire.scripts.feature_toggle import FeatureToggle
from grimoire.time.date import durantion_between_dates
from grimoire.time.time import Date


class PaceKeeping:
    TOPIC_NAME = "pace_keeping_events"

    def __init__(self):
        self.goals = goals

    def register(self, goal_name):
        if not goal_name in self.goals:
            raise Exception("Goal not found")
        MessageBroker(PaceKeeping.TOPIC_NAME + "_" + goal_name).produce(
            {"event_name": goal_name}
        )
        send_notification("Entry registered successfully")

    def get_i3_status_for_goal(self, goal_name):

        goal = Goal(goal_name)
        state = "Good"
        message = goal.status_message

        time_overdue = goal.get_time_overdue()
        if time_overdue:
            state = "Info"
            message = "{}+{:.1f}".format(message, time_overdue)

        result = {"text": message, "state": state}

        if FeatureToggle().disabled("pace_keeping_status_bar") or goal.disabled:
            result = {"text": ""}

        return dumps(result)

    def get_ordered_key(self, position):
        """ return the nth goal sorted by the position set on the configuration"""
        goals = []
        for key, goal in self.goals.items():
            if "disabled" in goal:
                continue
            goal["key"] = key
            goal["order"] = goal["order"] if "order" in goal else 666
            goals.append(goal)

        goals.sort(key=lambda x: x["order"])

        return goals[position - 1]["key"]

    def get_most_overdue(self, position):
        """ return the nth goal sorted by the position set on the configuration"""
        goals = []
        for key, goal_data in self.goals.items():
            goal = Goal(key)
            if goal.disabled:
                continue

            goal_data["overdueness"] = goal.get_time_overdue()
            goal_data["key"] = key
            goals.append(goal_data)

        goals.sort(key=lambda x: x["overdueness"], reverse=True)

        return goals[position - 1]["key"]


class Goal:
    def __init__(self, name):
        self.name = name
        self.key = name
        self.goal = goals[name]
        self.hours_to_repeat = self.goal["hours_to_repeat"]
        self.status_message = self.goal["status_message"]
        self.disabled = True if "disabled" in self.goal else False

    def get_time_overdue(self):
        """return how many hours passed above the goal"""
        now = Date.now()
        time_ellapsed = durantion_between_dates(self.get_latest_execution_date(), now)
        time_ellapsed = time_ellapsed["hours"] + (time_ellapsed["minutes"] / 60)

        if time_ellapsed > self.hours_to_repeat:
            return time_ellapsed - self.hours_to_repeat

        return 0

    def get_latest_execution_date(self):
        try:
            run_details = MessageBroker(
                PaceKeeping.TOPIC_NAME + "_" + self.name
            ).consume_last()
            execution_date = Date.from_str(run_details["generated_date"])
        except:
            # @todo add the start date of the goal itself so we start counting there
            # if no execution date is there we assume the beginning of the usage of this program
            if "start_date" in self.goal:
                execution_date = Date.from_str(self.goal["start_date"])
            else:
                execution_date = Date.from_str("2021-04-07 00:00:00")

        return execution_date


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(PaceKeeping).start()
