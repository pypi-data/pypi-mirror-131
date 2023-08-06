import unittest

import pytest

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class GYG(CustomTestCase):
    def test_binaries(self):
        self.check_binary("gygkube")
        self.check_binary("aws")

    def test_gygdev(self):
        self.shell_succeed("gygdev --help")

    # def test_kubectl(self):
    # self.shell_succeed("kubectl --context testing10 get all")

    def test_databricks_cli_working(self):
        tropic_version = "6.6"
        self.ss("databricks fs ls dbfs:/temp/jean/grimoire")
        self.ss(
            f" conda run -n dbconnect pip show databricks-connect | grep -i {tropic_version} "
        )
        self.ss("env | grep DATABRICKS_API_TOKEN")
        self.ss(
            'curl "http://dbc-59447477-336d.cloud.databricks.com/api/2.0/mlflow/registered-models/list" -H "Content-Type: application/json" -H "Authorization: Bearer $DATABRICKS_API_TOKEN"'
        )

        # test that the deployment of grimoire as a library can list the deployed arctifacts
        self.ss("grimoire notebook_install ls")

    def test_install_gygenv(self):
        """procedure to get a new gygenv"""
        location = "/tmp/gygenv"
        self.ss(
            f"""
            sudo curl https://s3.eu-central-1.amazonaws.com/archive.gyg.io/gyghub/gygenv.linux_amd64 --output {location}
        """
        )

    def test_login_as_fishfarm_aws(self):
        ""
        self.shell_succeed("gygaws login fishfarm")
        self.shell_succeed(
            "AWS_PROFILE=gygservice-fishfarm aws s3 ls s3://gygdata-shared/derived/search_pipelines/bayesian_cr_score/snapshot/ --summarize --human-readable"
        )


if __name__ == "__main__":
    unittest.main()
