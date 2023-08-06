import logging
import os
from typing import List

import yaml

from grimoire.notification import notify_send
from grimoire.shell import shell


def tmp_filename() -> str:
    import uuid

    return "/tmp/" + str(uuid.uuid4())[:20].replace("-", "")


def write_to_tmp_file(content: str) -> str:
    file_name = tmp_filename()

    write_file(file_name, content)

    return file_name


def write_file(file, data) -> str:
    with open(file, "w+") as f:
        f.write(data)

    return file


def create_file(file_name):
    if os.path.exists(file_name):
        raise Exception("File already exists")

    open(file_name, "w").close()


def append_file(file, data):
    if not file_exists(file):
        raise Exception(f"File does not exist to append to: {file}")
    with open(file, "a+") as f:
        f.write(data)


def append_file_creating(file, data):
    """
    Append to file, if the file si not there create it.
    """

    with open(file, "a+") as f:
        f.write(data)


def file_content(file_name) -> str:
    f = open(file_name)
    return f.read()


def file_get_content(file_name) -> List[str]:
    f = open(file_name)
    return f.readlines()


def create_folder(path):
    from pathlib import Path

    Path(path).mkdir(parents=True, exist_ok=True)


def file_exists(name):
    """
    the correct command is:
    os.path.exists(name)
    """
    return os.path.exists(name)


class Replace:
    delimiter = "^"

    def append_after_placeholder(self, file_name, placeholder, content):
        content = content.translate(str.maketrans({"&": "\\&"}))

        shell.enable_exception_on_failure()

        return self.run(
            file_name,
            placeholder,
            f"{placeholder}\\\\n{content}",
        )

    def run(self, file_name, from_str, to_str):
        if self.delimiter in from_str or self.delimiter in to_str:
            raise Exception(
                f"Replacement wont work because from string or to string contain the sed delimiter = {self.delimiter}"
            )

        final_command = f'sed -i "s{self.delimiter}{from_str}{self.delimiter}{to_str}{self.delimiter}" {file_name}'
        logging.debug(final_command)

        return shell.run(
            final_command,
            verbose=True,
        )


def yaml_content_from_file(filename):
    with open(filename) as f:
        data = yaml.load(f, yaml.FullLoader)

    return data
