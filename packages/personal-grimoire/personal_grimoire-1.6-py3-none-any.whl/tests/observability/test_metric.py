import pytest
from datadog.dogstatsd import DogStatsd

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class MetricSendTest(CustomTestCase):
    def test_send(self):
        statsd = DogStatsd(host="localhost", port="8126")
        statsd.increment("jean.test_increment_python")

    def test_on_terminal(self):
        self.shell_succeed(
            'echo "jean.test_increment_terminal:1|c" | nc -w 1 -u localhost 8125'
        )
