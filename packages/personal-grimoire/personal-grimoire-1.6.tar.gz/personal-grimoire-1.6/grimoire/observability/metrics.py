import logging

from datadog.dogstatsd import DogStatsd


class Metrics:
    """
    Abstraction for datadog
    """

    _client_instance = None

    @staticmethod
    def get_datadog_instance() -> DogStatsd:
        if Metrics._client_instance is None:
            # the default port is 8125 as stated in the config /etc/datadog-agent/datadog.yaml
            Metrics._client_instance = DogStatsd(host="localhost", port=8125)
        return Metrics._client_instance

    @staticmethod
    def increment(name):
        """already append the reco prefix on the metric name"""
        metric_name = f"grimoire.{name}"
        Metrics.get_datadog_instance().increment(metric_name)
        logging.debug(f"Metric increment: {metric_name}")

    @staticmethod
    def time_function(f, metric_name):
        """
        Register the time it took to execute such a function
        """
        import time

        start = time.time()
        result = f()
        dt = int((time.time() - start) * 1000)
        Metrics.get_datadog_instance().timing(metric_name, dt)
        logging.info(f"Timing registered: {metric_name}, value {dt}")
        return result
