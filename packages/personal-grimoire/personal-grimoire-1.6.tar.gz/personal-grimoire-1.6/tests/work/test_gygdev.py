import unittest

import pytest

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class GYGDev(CustomTestCase):
    def test_docker(self):
        """
        Docker should always be enabled. But with few containers running
        """
        self.shell_succeed(
            "sudo systemctl status docker | grep -i Active | grep -v dead"
        )


if __name__ == "__main__":
    unittest.main()
