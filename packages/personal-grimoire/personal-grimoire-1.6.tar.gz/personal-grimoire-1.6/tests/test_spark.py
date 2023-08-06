import pytest

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class Spark(CustomTestCase):
    @pytest.mark.skip(reason="jupyter is now in conda env")
    def test_jupyter_works(self):
        self.conda_env_exists("localspark")
        self.shell_succeed("jupyter lab --help")
