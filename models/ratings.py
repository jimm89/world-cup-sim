import numpy as np

from teams import get_team

BASE_XG = 1.5

HOSTS = {
    "USA",
    "Canada",
    "Mexico",
}


def expected_goals(
    team_1,
    team_2,
):

    elo_1 = get_team(team_1)["elo"]
    elo_2 = get_team(team_2)["elo"]

    elo_diff = elo_1 - elo_2

    # Compress Elo differences slightly to avoid
    # making favourites too dominant.
    elo_multiplier = np.exp(
        elo_diff / 500
    )

    xg_1 = BASE_XG * elo_multiplier
    xg_2 = BASE_XG / elo_multiplier

    if team_1 in HOSTS:
        xg_1 += 0.15

    if team_2 in HOSTS:
        xg_2 += 0.15

    xg_1 = max(0.20, xg_1)
    xg_2 = max(0.20, xg_2)

    return (
        xg_1,
        xg_2,
    )