#!/usr/bin/env python

from grimoire.notification import send_notification
from grimoire.shell import shell
from grimoire.string import chomp, remove_new_lines


class Clipboard:
    def get_content(self):
        result = shell.run_with_result("xsel --clipboard --output")
        result = chomp(result)

        return result

    def get_content_preview(self):

        content = self.get_content()
        content = content.strip(" \t\n\r")
        content = remove_new_lines(content)
        content_len = len(content)
        desized_preview_size = 10
        size_of_preview = (
            desized_preview_size if desized_preview_size < content_len else content_len
        )

        final_content = content[0:size_of_preview]
        suffix = " ..." if len(content) > size_of_preview else ""
        return f"{final_content}{suffix}"

    def set_content(self, content, enable_notifications=True):
        if enable_notifications:
            send_notification(f"Content copied: {content}")

        def shellquote(s):
            return "'" + s.replace("'", "'\\''") + "'"

        cmd = f"echo {shellquote(content)} | xsel --clipboard --input"
        return shell.run(cmd)


if __name__ == "__main__":
    import fire

    fire.Fire(Clipboard)
