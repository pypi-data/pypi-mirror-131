import random


def true_percentage_of_times(percentage_true):
    """
    if you pass 90 it will return true 90% of the time
    """
    return random.randint(0, 100) < percentage_true
