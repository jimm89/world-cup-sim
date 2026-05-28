import numpy as np

from models.match import (
    simulate_match
)

from models.ratings import (
    expected_goals
)


def play_knockout_match(
    team_1,
    team_2
):

    # 90 minutes
    g1, g2 = (
        simulate_match(
            team_1,
            team_2
        )
    )

    if g1 > g2:
        return team_1

    if g2 > g1:
        return team_2

    # EXTRA TIME
    xg_1, xg_2 = (
        expected_goals(
            team_1,
            team_2
        )
    )

    # 30 mins ≈ 1/3 match
    # slight favourite edge
    et_xg_1 = (
        xg_1
        * 0.33
    )

    et_xg_2 = (
        xg_2
        * 0.33
    )

    et_g1 = np.random.poisson(
        et_xg_1
    )

    et_g2 = np.random.poisson(
        et_xg_2
    )

    g1 += et_g1
    g2 += et_g2

    if g1 > g2:
        return team_1

    if g2 > g1:
        return team_2

    # PENALTIES
    # stronger teams slightly better
    xg_diff = (
        xg_1 - xg_2
    )

    team_1_prob = (
        0.5
        + (
            xg_diff * 0.08
        )
    )

    team_1_prob = min(
        max(
            team_1_prob,
            0.35
        ),
        0.65
    )

    if np.random.random() < (
        team_1_prob
    ):
        return team_1

    return team_2