from grimoire.shell import shell as s
from grimoire.smartimmersion.domain.scoring.dataset import DataSourceEntry
from grimoire.smartimmersion.domain.sentence import Sentence
from grimoire.translator.translator import Translator as GrimoireTranslator


class RegisterHard:
    def __init__(self, dataset):
        self.dataset = dataset

    def register(self, content):
        content = Sentence(content)

        if len(content.text) < 2:
            raise Exception(f"Content in clipboard is too small: {content.text}")

        translated = GrimoireTranslator().translate(content.text)
        translated_sentence = Sentence(translated)

        if translated_sentence.len() == content.len():
            entry = DataSourceEntry(translated, content.text, 0)
            self.dataset.save_entry(entry)
            s.run_command_no_wait("grimoire si train")
        else:
            raise TranslationError.size_does_not_match(content, translated_sentence)

        return translated


class TranslationError(Exception):
    config = {
        "disable_tray_message": True,
        "enable_notification": True,
    }

    @staticmethod
    def size_does_not_match(content, translated_sentence):
        return TranslationError(
            f"Size of sentence and translated sentence do not match, will not save it Sentence {content.text}, {translated_sentence.text}"
        )
