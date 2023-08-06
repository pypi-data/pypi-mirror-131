from datetime import datetime


def durantion_between_dates(then, now=datetime.now()):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return divmod(
            seconds if seconds != None else duration_in_s, 86400
        )  # Seconds in a day = 86400

    def hours(seconds=None):
        return divmod(
            seconds if seconds != None else duration_in_s, 3600
        )  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return divmod(
            seconds if seconds != None else duration_in_s, 60
        )  # Seconds in a minute = 60

    def seconds(seconds=None):
        if seconds != None:
            return divmod(seconds, 1)
        return duration_in_s

    return {
        "years": int(years()[0]),
        "days": int(days()[0]),
        "hours": int(hours()[0]),
        "minutes": int(minutes()[0]),
        "seconds": int(seconds()),
    }


def is_today(datetime):
    return datetime.date() == datetime.today().date()
