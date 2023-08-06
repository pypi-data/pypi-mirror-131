import pytest

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class MLFlow(CustomTestCase):
    def test_mlflow_cli(self):
        list_experiments = "MLFLOW_TRACKING_URI=databricks mlflow experiments list"
        self.shell_succeed(f"test $( {list_experiments}| wc -l ) -gt 10")

    def test_mlflow_list_runs(self):
        list_runs = (
            "MLFLOW_TRACKING_URI=databricks mlflow runs list --experiment-id=6808719"
        )
        self.shell_succeed(f"test $( {list_runs}| wc -l ) -gt 10")
