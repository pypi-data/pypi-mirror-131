import os
import unittest

import pytest

from grimoire.config import GRIMOIRE_PROJECT_ROOT


class CliApiTestCase(unittest.TestCase):
    @pytest.mark.slow
    def test_help(self):

        """
        test that the help command of each major cli command exits successfully
        Is a minimal way of making sure that the important interfaces are preserved
        and that at least a compilation error is not being triggered.
        """
        self.assertEqual(0, os.system(f"{GRIMOIRE_PROJECT_ROOT}/grimoire/gyg/cli.py"))
