#!/usr/bin/env python

from grimoire.event_sourcing.message import MessageBroker


class FeatureToggle:
    def __init__(self):
        self.broker = MessageBroker(namespace="feature_toggles")

    def list_features(self):
        pass

    def disable(self, feature_name):
        self.broker.produce(
            {"feature_name": feature_name, "toogle_enabled": False},
            topic_name=feature_name,
        )

    def enable(self, feature_name):
        self.broker.produce(
            {"feature_name": feature_name, "toogle_enabled": True},
            topic_name=feature_name,
        )

    def toggle(self, feature_name):
        pass

    def enabled(self, feature_name) -> bool:
        result = self.broker.consume_last(feature_name)

        return result["toogle_enabled"]

    def disabled(self, feature_name) -> bool:
        return not self.enabled(feature_name)


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(FeatureToggle).start()
