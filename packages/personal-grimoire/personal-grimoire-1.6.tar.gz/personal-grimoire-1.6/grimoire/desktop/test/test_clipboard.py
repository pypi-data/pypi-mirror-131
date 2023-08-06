import unittest

from grimoire.desktop.clipboard import Clipboard


class ClipboardTestCase(unittest.TestCase):
    def test_copy_and_paste(self):
        clipboard_content = "abc"
        Clipboard().set_content(clipboard_content)
        self.assertEqual(Clipboard().get_content(), clipboard_content)


if __name__ == "__main__":
    unittest.main()
