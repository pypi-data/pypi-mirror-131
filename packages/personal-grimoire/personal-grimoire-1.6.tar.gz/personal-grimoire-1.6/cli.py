#!/usr/bin/env python
import os
from datetime import datetime

import fire

import grimoire as g
from grimoire.cicd.cicd import CICD
from grimoire.config import LOG_FILE
from grimoire.gyg.cli import GygCli
from grimoire.scripts.theme import Theme
from grimoire.search_run.cli import SearchAndRunCli
from grimoire.shell import shell
from grimoire.smartimmersion.smartimmersion import SmartImmersion
from grimoire.web_start import Ap


class Cli:
    def __init__(self):
        self.gyg = GygCli
        self.desktop_theme = Theme
        # @todo remove this dependency and use search run directly instead
        self.search_run = SearchAndRunCli
        self.si = SmartImmersion
        self.cicd = CICD
        self.api = Api
        self.notebook_install = NotebookInstall

    def about(self):
        print("My personal vault of magic")

    def fix_files(self):
        print("Current python Directory: " + g.s.run_with_result("pwd"))
        g.s.run("black .")
        g.s.run("flake8 .")

    def logs(self):
        shell.run(f"tail -f " + LOG_FILE)

    def log_tail(self):
        shell.run(f"tail -f " + LOG_FILE)


class NotebookInstall:
    def build(self):
        """ build distribution files of the library, found in dist/ folder"""
        self._execute("python3 setup.py sdist bdist_wheel")

    def deploy(self):
        """Deploys the version specified in config.yaml"""

        config = g.yml_content("config.yaml")
        version = config["version"]
        directory_to_deploy_in = config["databricks_directory_to_deploy_to"]

        generated_file = f"personal_grimoire-{version}-py3-none-any.whl"

        time_generated = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        target_file = f"personal_grimoire-{version}_{time_generated}-py3-none-any.whl"

        self._execute(
            f"databricks fs cp dist/{generated_file} {directory_to_deploy_in}/{target_file}"
        )
        print("Deploy done!")

    def ls(self):
        config = g.yml_content("config.yaml")
        directory_to_deploy_in = config["databricks_directory_to_deploy_to"]
        self._execute(f"databricks fs ls {directory_to_deploy_in}/")

    def build_and_deploy(self):
        """
        Build the library to databricks
        """
        self.build()
        self.deploy()

    def _execute(self, cmd):
        print(f"Runnign command: {cmd} ")
        os.system(cmd)


if __name__ == "__main__":
    fire.Fire(Cli)
