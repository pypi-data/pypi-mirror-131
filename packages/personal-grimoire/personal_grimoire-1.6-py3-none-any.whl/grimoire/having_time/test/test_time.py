from datetime import datetime

from grimoire.having_time.main import HavingTime, Work
from grimoire.test.test_case import CustomTestCase


class TestHavingTime(CustomTestCase):
    def test_hours_left(self):
        now = datetime.strptime("2021-02-09 21:27:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        self.assertEqual(0, work.hours_left_today())

        now = datetime.strptime("2021-02-09 06:27:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        self.assertEqual(8, work.hours_left_today())

        now = datetime.strptime("2021-02-09 11:00:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        self.assertEqual(5, work.hours_left_today())

        now = datetime.strptime("2021-02-09 17:00:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        self.assertEqual(1, work.hours_left_today())

    def test_week_days_left(self):
        now = datetime.strptime("2021-02-10 17:00:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        assert work.working_days_left == 2

        now = datetime.strptime("2021-02-12 19:00:00", "%Y-%m-%d %H:%M:%S")
        work = Work(now)
        assert work.working_days_left == 0
