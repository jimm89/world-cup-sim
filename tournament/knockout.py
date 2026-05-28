import random
import numpy as np

from models.match import (
    simulate_match
)


def play_knockout_match(
    team_1,
    team_2
):

    # 90 minutes
    g1, g2 = simulate_match(
        team_1,
        team_2
    )

    if g1 > g2:
        return team_1

    if g2 > g1:
        return team_2

    # Extra time (~1/3 match)
    et_g1 = np.random.poisson(
        0.33
    )

    et_g2 = np.random.poisson(
        0.33
    )

    g1 += et_g1
    g2 += et_g2

    if g1 > g2:
        return team_1

    if g2 > g1:
        return team_2

    # Penalties
    return random.choice(
        [team_1, team_2]
    )