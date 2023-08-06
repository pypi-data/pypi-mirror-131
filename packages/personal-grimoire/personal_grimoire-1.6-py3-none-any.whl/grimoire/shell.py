import os
import subprocess
from typing import List, Union
import logging


class Shell:
    def __init__(self, dry_run=False):
        self._dry_run = dry_run or os.getenv("DRY_RUN", False)
        self.throw_exception_on_failure = False
        self.print_command = False

    def enable_exception_on_failure(self):
        self.throw_exception_on_failure = True
        return self

    def disable_exception_on_failure(self):
        self.throw_exception_on_failure = False
        return self

    def enable_print_command(self):
        self.print_command = True
        return self

    def disable_print_command(self):
        self.print_command = False
        return self

    def run(
        self, cmd, dry_run=False, verbose=False, print_command=None
    ) -> Union[bool, List[bool]]:

        if verbose:
            print(f"Cmd: {cmd}")

        if print_command != None:
            self.print_command = print_command

        logging.debug(f"Command to execute: {cmd}")
        if dry_run or self._dry_run:
            return True

        if isinstance(cmd, list):
            return list(map(self.run_command, cmd))
        else:
            return self.run_command(cmd)

    def run_command(self, cmd, dry_run=False) -> bool:
        message = f'=> Command to run: "{cmd}"'
        logging.debug(message)

        if self._dry_run or dry_run:
            return True

        if self.print_command:
            os.system(f"echo '{message}'")

        result = os.system(cmd)
        success = result == 0

        if not success and self.throw_exception_on_failure:
            raise Exception(
                f"Shell command failed with status code: ({result}) for command ('{cmd}')"
            )

        return success

    def check_output(self, cmd, dry_run=False):
        return self.run_with_result(cmd, dry_run)

    def run_with_result(self, cmd, dry_run=False, verbose=False, print_command=None):
        """
        run a command and returns it's output
        """
        log = f"Command to run: '{cmd}, dry_run: {dry_run}'"
        if verbose:
            logging.debug(log)

        if print_command != None:
            self.print_command = print_command

        if self._dry_run or dry_run:
            return

        result = subprocess.check_output(cmd, shell=True)

        return result.decode("utf-8")

    def run_command_no_wait(self, cmd, dry_run=False) -> None:
        logging.debug(f"Command to run without waiting: '{cmd}'")

        if self._dry_run or dry_run:
            return
        subprocess.Popen(
            cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True
        )


shell = Shell()
