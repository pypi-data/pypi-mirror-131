import logging

from grimoire import s


def get_at(array, index, default):
    if index < 0:
        index += len(array)
    if index < 0:
        raise IndexError("list index out of range")
    return array[index] if index < len(array) else default


class Url:
    def __init__(self):
        from grimoire import Logger

        Logger()

    def open(self, free_text_search):
        """
        Envisioned usage:

        open: "gygadmin testing"
        or
        open: "adm tes"
        """
        config = {
            "envs": ["local", "test", "production"],
            "service": ["reco", "fishfarm"],
            "hosts": {
                "local": {
                    "fishfarm": "https://www.gygdev.gygtest.com",
                    "sentry": "https://sentry.gygdev.gygtest.com",
                },
                "test": {
                    "fishfarm": "https://www.testing10.gygtest.com",
                    "gygadmin": "https: // gygadmin.testing10.gygtest.com/",
                },
            },
        }

        asked_env = get_at(free_text_search.split(" "), 1, "")
        env = "local"
        logging.info(f"Environment requested for {asked_env}")
        for i in config["envs"]:
            if asked_env == i:
                env = asked_env
                logging.info(f"Matched env {env}")

        fishfarm_url = config["hosts"][env]["fishfarm"]
        location = 16
        tour_category = 1

        urls = {
            "adp": f"{fishfarm_url}/paris-l16/ultimate-versailles-90-minute-skip-the-line-guided-tour-t175182/",
            "tourcategory": f"{fishfarm_url}/discovery/paris-l16/tours-tc1/?utm_force=0",
        }

        for i in urls:
            if free_text_search.split(" ")[0] == i:
                url = urls[i]
                s.run(f"browser {url}")
