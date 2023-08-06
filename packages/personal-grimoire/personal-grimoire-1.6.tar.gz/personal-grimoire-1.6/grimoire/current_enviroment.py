import os


class CurrentEnvironment:
    """Answer the question on which enviroment the system is running"""

    def __init__(self):

        self._is_production = False
        self._is_local = "USER" in os.environ and os.environ["USER"] == "jean"
        self._is_ci = False

    def is_local(self):
        return self._is_local

    def is_ci(self):
        return self._is_ci

    def is_production(self):
        return self._is_production
