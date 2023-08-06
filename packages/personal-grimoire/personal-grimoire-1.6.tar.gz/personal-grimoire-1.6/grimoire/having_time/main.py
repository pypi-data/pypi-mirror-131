#!/usr/bin/env python

# from grimoire.time import today
from datetime import date, datetime, timedelta


def days_diff(dt1, dt2):
    return int(abs(dt1 - dt2).days)


def years_diff(dt1, dt2, return_float=False):
    float_result = (abs(dt1 - dt2).days) / 365
    if return_float:
        return float_result
    return int(float_result)


def hours_diff(dt1, dt2, return_float=False):
    float_result = abs(dt1 - dt2).seconds / 3600
    if return_float:
        return float_result
    return int(float_result)


def minutes_diff(dt1, dt2):
    return int((abs(dt1 - dt2).seconds) / 60)


class Work:
    days_month = 22
    hours_day = 8
    start_work_hour = 8
    stop_work_hour = 18
    break_between = 12, 14
    average_lifetime_working_hours = 90000

    def __init__(self, now):
        self.now = now
        self.morning = self.break_between[0] - self.start_work_hour
        self.afternoon = self.stop_work_hour - self.break_between[1]

    def hours_left_today(self):
        if self.now.hour > self.stop_work_hour:
            return 0

        if self.now.hour < self.start_work_hour:
            return self.daily_working_hours

        if (
            self.now.hour > self.start_work_hour
            and self.now.hour < self.break_between[0]
        ):
            return self.break_between[0] - self.now.hour + self.afternoon

        return self.stop_work_hour - self.now.hour

    @property
    def working_days_left(self):
        friday = self.now + timedelta((4 - self.now.weekday()) % 7)
        return days_diff(friday, self.now)

    def hours_week_left(self):
        return self.hours_left_today() + (
            self.working_days_left * self.daily_working_hours
        )

    @property
    def daily_working_hours(self):
        return self.morning + self.afternoon


class HavingTime:
    def __init__(self):
        self.birthday: datetime = datetime.strptime("04-11-1992", "%d-%M-%Y")
        self.career_start = datetime.strptime("01-03-2011", "%d-%M-%Y")
        self.now = datetime.now()
        self.today = datetime.now()
        self.end_of_today = self.today.replace(hour=23, minute=59)
        self.work = Work(self.now)

    def get_all(self):
        average_life_expectancy_germany = 80
        years_of_life = years_diff(self.today, self.birthday)
        years_of_career = years_diff(self.today, self.career_start, return_float=True)
        days_of_career = days_diff(self.today, self.career_start)
        years_left_average = average_life_expectancy_germany - years_of_life
        # worked_hours_already = days_of_career * 8
        # hours_still_to_work = average_lifetime_working_hours - worked_hours_already
        days_of_career = int(years_of_career * 12 * 22)
        hours_of_career = days_of_career * Work.hours_day
        hours_of_career_left = Work.average_lifetime_working_hours - hours_of_career
        percentage_career = int(
            (hours_of_career / Work.average_lifetime_working_hours) * 100
        )

        return {
            "years_of_life": years_of_life,
            "years_left": years_left_average,
            "years_of_career": years_of_career,
            "days_of_career": days_of_career,
            "hours_of_career": hours_of_career,
            "hours_of_career_left": hours_of_career_left,
            "hours_left_today": self.get_hours_left_today(),
            "percentage_career": percentage_career,
            "days_of_career": days_of_career,
            "days_left": years_left_average * 365,
        }

    def get_hours_left_today(self) -> float:
        return hours_diff(self.today, self.end_of_today, return_float=True)


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(HavingTime).start()
