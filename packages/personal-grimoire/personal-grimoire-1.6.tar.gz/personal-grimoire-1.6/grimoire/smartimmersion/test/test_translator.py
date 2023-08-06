import os
import unittest

import pytest
from mock import patch

from grimoire.smartimmersion.domain.variations_generator.translator import Translator


@pytest.mark.skipif("CI_ENV" in os.environ, reason="implement redis first")
class TranslatorTestCase(unittest.TestCase):
    def test_happy_path(self):
        """
        Asserts that happy path works
        """
        with patch.object(Translator, "real_translation") as real_translation:

            translated_result = "translated_by_real_translator"

            real_translation.side_effect = lambda x: translated_result
            translator = Translator(disable_cache=True)
            result = translator.translate_word("foobarbar")
            self.assertEqual(result, translated_result)

    def test_number(self):
        """
        Asserts that numbers are skipped while translating
        """
        with patch.object(Translator, "real_translation") as real_translation:
            to_translate_string = "123456"
            translator = Translator()
            result = translator.translate_word(to_translate_string)

            assert result == to_translate_string
            assert not real_translation.called

    def test_raise_error_when_translated_words_count_is_differnet_from_source_words(
        self,
    ):
        """
        when the translation contains more than 1 word in the result we want an error
        """
        with patch.object(Translator, "real_translation") as real_translation:
            real_translation.side_effect = lambda x: "foobar baz"
            translator = Translator(disable_cache=True)

            with self.assertRaises(Exception) as context:
                translator.translate_word("foobar")
                assert "Translation return more than 1 word" == context.exception

            assert real_translation.called


if __name__ == "__main__":
    unittest.main()
