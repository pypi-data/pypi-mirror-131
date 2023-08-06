from typing import Optional, Tuple, Union

from grimoire.shell import shell


def send_notification(message, urgent=False):
    cmd = f"notify-send '{message}'"
    if urgent:
        cmd = f"{cmd} -u critical"
    return shell.run(cmd)


def notify_send(message):
    return send_notification(message)


ButtonName = Union[str]
Command = Union[str]


def send_error_message(message, button: Optional[Tuple[ButtonName, Command]] = None):
    if button:
        shell.run_command_no_wait(
            f"i3-nagbar -m \"{message}\" -b '{button[0]}' '{button[1]}'"
        )
    else:
        shell.run_command_no_wait(f'i3-nagbar -m "{message}"')
