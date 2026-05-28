import numpy as np
from teams import teams

BASE_XG = 1.35


HOSTS = [
    "USA",
    "Canada",
    "Mexico"
]


def expected_goals(
    team_1,
    team_2
):

    t1 = teams[team_1]
    t2 = teams[team_2]

    elo_diff = (
        t1["elo"]
        - t2["elo"]
    )

    elo_multiplier = np.exp(
        elo_diff / 800
    )

    xg_1 = (
        BASE_XG
        * t1["attack"]
        * t2["defence"]
        * elo_multiplier
    )

    xg_2 = (
        BASE_XG
        * t2["attack"]
        * t1["defence"]
        / elo_multiplier
    )

    if team_1 in HOSTS:
        xg_1 += 0.15

    if team_2 in HOSTS:
        xg_2 += 0.15

    return xg_1, xg_2