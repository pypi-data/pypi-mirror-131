import unittest

from grimoire.config import GRIMOIRE_PROJECT_ROOT
from grimoire.file import file_exists


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertTrue(file_exists(GRIMOIRE_PROJECT_ROOT + "/README.md"))


if __name__ == "__main__":
    unittest.main()
