import unittest

from grimoire.gyg.databricks_notebook import DatabricksNotebook


class MyTestCase(unittest.TestCase):
    def test_databricks_notebook_api(self):

        self.assertTrue(hasattr(DatabricksNotebook({"spark": None}), "sql"))


if __name__ == "__main__":
    unittest.main()
