import numpy as np
from models.ratings import expected_goals


def simulate_match(team_1, team_2):

    xg_1, xg_2 = expected_goals(
        team_1,
        team_2
    )

    goals_1 = np.random.poisson(xg_1)
    goals_2 = np.random.poisson(xg_2)

    return goals_1, goals_2