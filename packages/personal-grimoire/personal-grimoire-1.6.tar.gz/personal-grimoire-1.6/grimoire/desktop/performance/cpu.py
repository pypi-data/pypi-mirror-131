#!/usr/bin/env python
from grimoire.ask_question import AskQuestion
from grimoire.observability.metrics import Metrics
from grimoire.shell import shell
from grimoire.string import clean_string


class CPU:
    def set_frequency_dmenu(self):
        frequency = AskQuestion().ask(f"CPU frequency you wanna set:")
        shell.run(f"sudo cpupower frequency-set -f {frequency}Ghz", verbose=True)

    def get_frequency(self) -> int:
        """
        Returns the current frequency of the cpu
        """
        freq = shell.run_with_result(
            'cat /proc/cpuinfo | grep "cpu MHz" | head -n 1 | cut -d ":" -f2'
        )
        result = int(float(clean_string(freq)))

        Metrics.get_datadog_instance().gauge("grimoire.cpu.frequency", result)

        return result


if __name__ == "__main__":
    from grimoire.startup import ApplicationStartup

    ApplicationStartup().with_fire(CPU).start()
