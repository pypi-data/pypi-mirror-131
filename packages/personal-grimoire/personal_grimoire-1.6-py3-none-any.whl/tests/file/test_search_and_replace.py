import unittest

import pytest

from grimoire.file import Replace, file_content, write_file


@pytest.mark.slow
class ReplaceTestCase(unittest.TestCase):
    def test_replace_happy(self):
        file_name = "/tmp/foobar"

        text_from = """abc"""
        write_file(file_name, text_from)

        expected_text = """abcde"""

        Replace().run(file_name, "abc", "abcde")
        self.assertEqual(expected_text, file_content(file_name))


if __name__ == "__main__":
    unittest.main()
