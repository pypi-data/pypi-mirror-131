#!/usr/bin/env python

from grimoire.desktop.clipboard import Clipboard
from grimoire.desktop.dmenu import Dmenu
from grimoire.file import file_content
from grimoire.notification import send_notification
from grimoire.shell import shell as s
from grimoire.string import ends_in_new_line, remove_new_line_end, remove_new_lines
from grimoire.translator.translator import Translator

s.enable_exception_on_failure()


class Anki:
    def create_edit_content_and_create_cloze(self):
        """
        Open a vim session that you can edit, with the result create a cloze
        """
        self.check_anki_not_runnking()
        file_name = remove_new_line_end(s.run_with_result("runFunction editClippboard"))
        content = remove_new_lines(file_content(file_name))

        self.create_luckentext(content)
        send_notification("Card created. Remember to sync!")

    def translate_clipboard_and_add_to_anki(self):
        """
        Open a vim session that you can edit, with the result create a cloze
        """
        self.check_anki_not_runnking()
        clipboard = Clipboard()
        german = clipboard.get_content()
        english = Translator().translate(german)

        Clipboard().set_content(english, enable_notifications=False)

        anki_entry = f"{self.cloze_surround(german)} = {english}"
        self.create_luckentext(anki_entry)

        clipboard.set_content(english)
        send_notification(f"{anki_entry} | Created card")

    def create_from_clipboard_and_dmenu(self):
        self.check_anki_not_runnking()
        content = Clipboard().get_content()
        definition = Dmenu(title="Give the card definition").rofi()
        self.create_card(definition, content)
        send_notification("Card created. Remember to sync!")

    def check_anki_not_runnking(self):
        s.disable_exception_on_failure()
        if s.run("sudo ps -aux | grep '/bin/anki' | grep -v grep "):
            raise AnkiException.anki_is_open()

    def cloze_clipboard(self):
        # surround with close the string in clipboard

        original_content = Clipboard().get_content()

        updated = self.cloze_surround(original_content)

        if not ends_in_new_line(original_content):
            updated = remove_new_line_end(updated)

        Clipboard().set_content(updated)

    def create_card(self, definition, content):
        definition = self.cloze_surround(definition)
        # or Einfach
        self.create_luckentext(f"{definition} {content}")

    def create_luckentext(self, content):
        s.run(f"apy add-single -m 'Lückentext' -d 'MyDeck' '{content}' ''")

    def cloze_surround(self, content):
        return "{{c1::" + content + "}}"


class AnkiException(Exception):
    config = {
        "disable_tray_message": True,
        "enable_notification": True,
        "disable_sentry": True,
    }

    @staticmethod
    def anki_is_open():
        return AnkiException("Anki is open. Close it before send new content.")


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Anki).start()
