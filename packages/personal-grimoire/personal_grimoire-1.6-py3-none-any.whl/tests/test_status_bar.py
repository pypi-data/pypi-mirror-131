import pytest

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.test.test_case import CustomTestCase


@pytest.mark.skipif(
    not CurrentEnvironment().is_local(),
    reason="validation for local machine only",
)
class StatusBar(CustomTestCase):
    def test_system_bar_components(self):
        # get current focus element
        self.shell_returns_json("status_bar.py focus")
        self.shell_returns_json("pace_keeping.py get_i3_status_for_goal sport")
        self.shell_returns_json("status_bar.py cpu_frequency")
        self.shell_returns_json("status_bar.py get_test_results")

    def test_clipboard_preview(self):
        self.shell_succeed("clipboard.py get_content_preview")
