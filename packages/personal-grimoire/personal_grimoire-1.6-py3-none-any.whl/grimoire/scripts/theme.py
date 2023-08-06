#!/usr/bin/env python



from grimoire import Logger, s
from grimoire.databases.cache import Cache
from grimoire.event_sourcing.message import MessageBroker


class Theme:
    def __init__(self):
        self.broker = MessageBroker(topic_name="theme_archlinux")
        Logger()
        self._cache = Cache()

    def to_dark(self):
        self._cache.set("current_theme", "dark")
        self.broker.produce({"theme": "dark"})

        kitty = """
        cd ~/.config/kitty ;\
         rm -rf ~/.config/kitty/theme.conf ;\
          ln -s ./kitty-themes/themes/Solarized_Dark_-_Patched.conf ~/.config/kitty/theme.conf
        """

        s.run(kitty)

    def to_light(self):
        self._cache.set("current_theme", "light")
        self.broker.produce({"theme": "light"})

        kitty = """
        cd ~/.config/kitty ;\
         rm -rf ~/.config/kitty/theme.conf ;\
         ln -s ./kitty-themes/themes/Solarized_Light.conf ~/.config/kitty/theme.conf
        """

        s.run(kitty)

    def get_current_theme(self):

        cached_theme = self._cache.get("current_theme")

        if cached_theme:
            return cached_theme

        theme = self.broker.consume_last()["theme"]
        self._cache.set("current_theme", theme)

        return theme


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(Theme).start()
