#!/usr/bin/env python
from __future__ import annotations

import sys
from dataclasses import dataclass

from pydantic.typing import Literal

from grimoire.config import GRIMOIRE_PROJECT_ROOT
from grimoire.event_sourcing.message import MessageBroker
from grimoire.shell import shell as s

s.enable_exception_on_failure()


class Test:
    """ Run CICD Quality assurance checks """

    def fast(self):
        def real():
            self.compile()
            s.run(f"cd {GRIMOIRE_PROJECT_ROOT} ; pytest -m 'not slow'")

        self._tracking_wrap(real)

    def complete(self):
        self.all()

    def pre_commit(self):
        """
        Runs the manual stage of pre commit
        """
        s.run("pre-commit run --all-files --hook-stage manual")

    def comit(self):
        """
        Perform a git commit only if all tests are passing.
        """
        s.run(
            """
        git diff ; \
        echo -n "Give the commit message please:" && \
        read COMMIT_MESSAGE  && \
        grimoire cicd test complete && \
        git add . && \
        runFunction gitCommit "$COMMIT_MESSAGE" ; \
        runFunction commitAndPush "$COMMIT_MESSAGE"
        """
        )

    def all(self):
        def real():
            self.pre_commit()
            self.compile()
            # now precommit does typecheck as well
            # self.typecheck()
            self.lint()
            s.run("pytest -n 4")

        self._tracking_wrap(real)

    def compile(self):
        s.run("python -m compileall -l grimoire")

    def typecheck(self):
        s.run(
            f"cd {GRIMOIRE_PROJECT_ROOT} ; python -m mypy --config-file mypy.ini grimoire"
        )

    def lint(self):
        s.run(f"cd {GRIMOIRE_PROJECT_ROOT} ; pylint grimoire")

    def _fail_on_false(self, result):
        if not result:
            sys.exit(1)

    def _tracking_wrap(self, f):
        """Logs the results of the test and produces data"""
        test_succeeded = True
        try:
            f()
        except:
            test_succeeded = False
        finally:
            event = ResultOfQATest(test_succeeded=test_succeeded, test_type="fast")

            MessageBroker(ResultOfQATest.TOPIC_NAME).produce(event.__dict__)

        return


@dataclass
class ResultOfQATest:
    test_succeeded: bool
    test_type: Literal["fast", "complete"]
    TOPIC_NAME: str = "test_execution_results"


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Test).start()
