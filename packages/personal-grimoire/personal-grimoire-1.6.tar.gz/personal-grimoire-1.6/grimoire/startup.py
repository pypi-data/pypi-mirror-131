from grimoire import Logger
from grimoire.config import LOG_FILE
from grimoire.error_handler import ErrorHandler


class ApplicationStartup:
    def __init__(self):
        self.enable_sentry = False
        self.default_logger = True
        self.run_fire = False

    def with_sentry(self):
        self.enable_sentry = True
        return self

    def without_default_logger(self):
        self.enable_sentry = True
        return self

    def with_grimoire_logger(self):
        self.log_to_file(LOG_FILE)
        return self

    def log_to_file(self, file_name: str):
        Logger(log_file=file_name)
        return self

    def with_fire(self, entrypoint):
        self.run_fire = True
        self.fire_entrypoint = entrypoint
        return self

    def initialize(self):
        import colored_traceback

        colored_traceback.add_hook()

    def start(self):
        try:
            import colored_traceback

            colored_traceback.add_hook()

            if self.run_fire:
                import fire

                fire.Fire(self.fire_entrypoint)
        except BaseException as e:
            ErrorHandler().handle_and_retrow(e)
