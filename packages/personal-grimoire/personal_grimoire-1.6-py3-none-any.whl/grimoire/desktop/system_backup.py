#!/usr/bin/env python
"""
Procedures to perform and recover backup

Backup and clonning Linux. The purpose of this backup is not to restore old files.
The purpose is to have an always functional linux. Every new backup can delete old files but the premisse
is that the system is working and I want it to work on the same way it was backed-up.
In the future I might explore others kinds of backup as well but this is the most important type.

Details can be found here: https://docs.google.com/document/d/1kfn76oUdH8hZkCwxxxjMlRiFbahbKKjUypk_q56yg24/edit#

"""
import logging

from grimoire.file import file_exists
from grimoire.shell import shell

shell.enable_exception_on_failure()

class Backup:
    """"""

    HD_ID = "295d2c15-4b97-441a-b776-6b2a80821014"
    MOUNT_POINT = f"/run/media/jean/{HD_ID}"
    LOG = f"/run/media/jean/{HD_ID}/backup/log"
    BACKUP_DESTINATION = f"{MOUNT_POINT}/backup"
    FINAL_DESTINATION = f"{BACKUP_DESTINATION}/root-folder"
    EXCLUSIONS = [
        "/swapfile",
        # excludes the content but not the directory
        "/dev/*",
        "/proc",
        "/proc/*",
        "/sys/*",
        "/tmp/*",
        "/run/*",
        "/mnt/*",
        "/media/*",
        # excludes the hole directory
        "/lost+found",
        "/var/cache/pacman/pkg",
        "/home/*/.cache",
        "/home/*/.gvfs",
        "/home/*/.cache",
        "/var/lib/docker/overlay2",
        "/home/*/.local/share/Trash",
    ]

    def perform(self):
        """
        Perform backup
        """
        print(f"Backup destination: {Backup.FINAL_DESTINATION}")

        shell.run(f"sudo blkid | grep '{Backup.HD_ID}'")

        shell.run(
            f"sudo mount /dev/disk/by-uuid/{Backup.HD_ID} {Backup.MOUNT_POINT} || true"
        )
        assert file_exists(Backup.FINAL_DESTINATION)

        logging.info(f"Saving backup in: {Backup.FINAL_DESTINATION}")

        shell.run(f"touch {Backup.LOG}/$(date +%F_%H-%M-%S)")

        command = self._get_command()

        if input(f"Running {command} are you sure? (y/n)") != "y":
            exit()

        shell.run(command)
        shell.run(f"touch {Backup.LOG}/$(date +%F_%H-%M-%S)_end")

    def _get_command(self):

        quoted_exclude = [f'--exclude "{x}"' for x in Backup.EXCLUSIONS]
        exclude_command = " ".join(quoted_exclude)

        # for documentation on the optiosn follow this link: https://wiki.archlinux.org/title/rsync
        command = f"""
            sudo rsync --progress --delete -aAXHv {exclude_command} \
            / {Backup.FINAL_DESTINATION}
        """
        return command


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Backup).start()
