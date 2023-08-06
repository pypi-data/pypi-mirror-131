#!/usr/bin/env python
"""
Main doc: https://docs.google.com/document/d/1Dmpl90ZjvmBfKENENQr-J1ngR61pdB9Jx6N6GlJMNns/edit
"""

from joblib import load

from grimoire import Logger, s
from grimoire.smartimmersion.application.register_hard import RegisterHard
from grimoire.smartimmersion.config import PROJECT_ROOT
from grimoire.smartimmersion.domain.scoring.dataset import SourceDataset
from grimoire.smartimmersion.domain.scoring.train import Train
from grimoire.smartimmersion.domain.variations_generator.translator import Translator


class SmartImmersion:
    """
    This program is the entrypoint of the program
    """

    def __init__(self):
        Logger(log_file=PROJECT_ROOT + "/log/main.log")
        Logger.enable_sentry()
        self.dataset = SourceDataset()

    def mlflow_website(self):
        s.run(f' (sleep 5; browser "http://localhost:5002") & ')
        s.run(
            f"cd {PROJECT_ROOT} ; mlflow ui --backend-store-uri sqlite:///mlflow.db -p 5002"
        )

    def stats(self):
        vocabulary = load(PROJECT_ROOT + "/vocabulary.joblib")
        return {
            "vocabulary_size": len(vocabulary),
            "dataset_size": self.dataset.number_of_entries(),
            "translator_working": Translator().is_working(),
        }

    def train(self):
        import os

        os.chdir(PROJECT_ROOT)
        Train().train()
        return self.stats()

    def fix_schema(self):
        SourceDataset()._reapply_save()

    def register_hard(self, content):
        return RegisterHard(self.dataset).register(content)

    def log_tail(self):
        s.run(f"grc tail -f ")

    def edit_config(self):
        s.run(f"runFunction terminal_run 'vim {PROJECT_ROOT}/config.py'")


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(SmartImmersion).start()
