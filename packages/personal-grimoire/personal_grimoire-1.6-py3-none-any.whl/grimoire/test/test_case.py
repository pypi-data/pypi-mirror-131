import logging
import unittest

from grimoire.shell import Shell
from grimoire.shell import shell as s


class CustomTestCase(unittest.TestCase):
    def ss(self, cmd):
        self.shell_succeed(cmd)

    def shell_fail(self, cmd):
        s.disable_exception_on_failure()
        self.assertFalse(s.run(cmd))

    def shell_succeed(self, cmd):
        self.assertTrue(s.run(cmd))

    def shell_returns_json(self, cmd):
        final_command = f"{cmd} | jq ."
        logging.info(f"Shell returns json: {final_command}")
        self.assertTrue(s.run(final_command))

    def check_binary(self, binary):
        self.ss(f"which {binary}")

    def conda_env_exists(self, env_name):
        self.ss(f"conda info  --envs | grep -i {env_name}")

    def assert_process_running(self, name):
        """ runs ps -aux with grep to inspect if a process is running """
        return self.shell_succeed(
            f"test $(ps -aux | grep -i '{name}' | grep -v 'grep' | wc -l ) -ge 1"
        )


if __name__ == "__main__":
    unittest.main()
