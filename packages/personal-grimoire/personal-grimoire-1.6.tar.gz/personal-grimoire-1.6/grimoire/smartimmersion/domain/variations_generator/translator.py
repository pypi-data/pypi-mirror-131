import logging
import random

from grimoire import s
from grimoire.core.redis import SimpleKeyValueDb
from grimoire.string import StringManipulation


class Translator:
    def __init__(self, disable_cache=False, exceptions=None, settings=None):
        self.db = SimpleKeyValueDb()
        engines = [
            "google",
        ]
        self.disable_cache = disable_cache
        self.engine = random.choice(engines)
        logging.debug(f"Picked engine is: {self.engine}")
        self.exceptions = exceptions
        self.remote_api_disabled = (
            settings.DISABLE_TRANSLATIONS_API if settings else False
        )

    def translate_word(self, text):
        text = text.replace('"', '\\"')

        if self.exceptions and self.exceptions.manual_tranlation(text):
            return self.exceptions.manual_tranlation(text)

        if text.isnumeric():
            logging.info(f"Will not translate numbers {text}")
            return text

        if len(text) <= 2:
            logging.info(f"Will not translate smaller than 3 chars strings: {text}")
            return text

        if self.exceptions and self.exceptions.should_not_translate(text):
            logging.info(f"Matching not translateable text {text}")
            return text

        translation = self.db.load(text) if not self.disable_cache else None

        if translation:
            return translation

        if self.remote_api_disabled:
            return text

        if not translation:
            translation = self.real_translation(text)

        if len(translation) < 2:
            logging.warning(
                f"Translation of word {text} too small, considered error: {translation} returning original key"
            )
            return text

        if len(text.split(" ")) != len(translation.split(" ")):
            raise Exception(
                f"Translation return more than 1 word: ({text}) => ({translation}) "
            )

        self.db.save(text, translation)

        return translation

    def real_translation(self, text):
        translation = s.run_with_result(f'trans en:de "{text}" -b -e ' + self.engine)
        translation = StringManipulation.chomp(translation)

        return translation

    def is_working(self):
        result = s.run_with_result('trans en:de "library" -b -e google')

        return result != "\n"
