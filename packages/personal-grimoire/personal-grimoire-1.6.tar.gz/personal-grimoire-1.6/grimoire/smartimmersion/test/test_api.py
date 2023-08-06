import unittest

import pytest

from grimoire import s
from grimoire.current_enviroment import CurrentEnvironment
from grimoire.smartimmersion.config import API_PORT


@pytest.mark.skipif(
    True,
    reason="api disabled for now",
)
@pytest.mark.slow
@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="implement redis first",
)
class GrimoireApiTestCase(unittest.TestCase):
    def test_api(self):
        result = s.run_with_result(
            f"curl 'http://localhost:{API_PORT}/translate?q=translate' --max-time 3"
        )
        # when the sentence is too small it should trow an error
        # while generating vartiations and return the one received
        assert result == "translate"

    def test_api_real(self):
        result = s.run(
            f"""curl http://localhost:{API_PORT}/translate \
            --max-time 3 \
            --data-urlencode "q=Herbert Raymond McMaster is able to look back on a long career in the United States Army. When the Iron Curtain fell in Europe, he was stationed in Bavaria as an officer in an Armored Cavalry Regiment that patrolled the border between West and East Germany. In February 1991, he commanded a battle during the Gulf War in Kuwait in which 28 Iraqi tanks were destroyed within minutes." -X GET -G
            """
        )
        assert result is True
