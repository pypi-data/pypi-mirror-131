#!/usr/bin/env python
from __future__ import annotations

import logging

from pydantic import BaseModel

from grimoire import Logger
from grimoire.desktop.browser import Browser
from grimoire.desktop.clipboard import Clipboard
from grimoire.desktop.dmenu import Dmenu
from grimoire.event_sourcing.message import MessageBroker
from grimoire.notification import send_notification
from grimoire.shell import shell
from grimoire.string import chomp, emptish


class Translator:
    def __init__(self, engine="google", lang_from="de", lang_to="en"):
        self.engine = engine
        self.lang_from = lang_from
        self.lang_to = lang_to

    def translate(self, text, lang_from=None, lang_to=None):
        translation = self._translate(text)
        if len(translation) < 2:
            raise Exception("Translation too small, probably translator is broken")

        event = TranslatedEntry(**{"text": text, "result": translation})
        MessageBroker("translated_entries").produce(event.dict())

        return translation

    def clipboard(self, lang_from, lang_to):
        """
        Content comes from clipboard
        """
        self.lang_from = lang_from
        self.lang_to = lang_to

        text = Clipboard().get_content()
        result = self.translate(text)
        send_notification(result)
        Clipboard.set_content(result)

    def dmenu(self, lang_from, lang_to):
        self.lang_from = lang_from
        self.lang_to = lang_to

        text = Dmenu(
            f"Translate {self.lang_from} to {self.lang_to}:",
        ).rofi()
        Clipboard().set_content(text)
        result = self.translate(text)
        send_notification(result)

    def translator_clipboard(self):
        text = Clipboard().get_content()
        Clipboard().set_content(text)
        Browser().open(
            f"https://translate.google.com/?sl=de&tl=en&text={text}&op=translate"
        )

    def linguee_dmenu(self):
        text = Dmenu("Linguee:").rofi()
        Clipboard().set_content(text)
        Browser().open(
            f"https://www.linguee.com/english-german/search?source=german&query={text}"
        )

    def linguee_clipboard(self):
        text = Clipboard().get_content()
        Clipboard().set_content(text)
        Browser().open(
            f"https://www.linguee.com/english-german/search?source=german&query={text}"
        )

    def conjulgation_clipboard(self):
        text = Clipboard().get_content()
        Browser().open(f"https://www.verbformen.com/conjugation/?w={text}")

    def conjulgation_dmenu(self):
        text = Dmenu("Conjulgation:").rofi()
        Clipboard().set_content(text)
        Browser().open(f"https://www.verbformen.com/conjugation/?w={text}")

    def _translate(self, text):
        try:
            return self._translate_trans(text)
        except:
            self._translate_browser(text)
            return text

    def _translate_browser(self, text):
        Browser().open(
            f"https://translate.google.com/?sl={self.lang_from}&tl={self.lang_to}&text={text}&op=translate"
        )

    def _translate_trans(self, text):
        """
        Use open source tool called trans to translate the text

        """
        translate_cmd = (
            f'trans {self.lang_from}:{self.lang_to} "{text}" -b -e {self.engine}'
        )
        logging.info(f"Translate command: {translate_cmd}")
        translation = shell.run_with_result(translate_cmd)
        translation = chomp(translation)
        if emptish(translation):
            raise Exception("Translation did not work, empty result")
        logging.info(f"Translate result {translation}")

        return translation


class TranslatedEntry(BaseModel):
    text: str
    result: str


if __name__ == "__main__":
    import fire

    Logger()
    fire.Fire(Translator)
