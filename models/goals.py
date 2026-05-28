import numpy as np


MAX_GOALS = 6


def sample_goals(xg):

    goals = np.random.poisson(
        xg
    )

    return min(
        goals,
        MAX_GOALS
    )