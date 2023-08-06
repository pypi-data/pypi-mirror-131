import matplotlib.pyplot as plt

from grimoire.datascience import npmap


class Graph:
    @staticmethod
    def plot(x, y):
        """
        pyplot with some niceties on top
        y can be a callaback

        """
        final_y = y
        if callable(y):
            final_y = npmap(y, x)

        plt.plot(x, final_y)
