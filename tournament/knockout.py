import numpy as np

from models.match import simulate_match
from models.ratings import expected_goals


def play_knockout_match(
    team_1,
    team_2,
    return_details=False,
):

    # 90 minutes
    g1, g2 = simulate_match(team_1, team_2)

    if g1 > g2:
        winner = team_1
        method = "FT"

    elif g2 > g1:
        winner = team_2
        method = "FT"

    else:

        xg_1, xg_2 = expected_goals(
            team_1,
            team_2,
        )

        et_g1 = np.random.poisson(
            xg_1 * 0.33
        )

        et_g2 = np.random.poisson(
            xg_2 * 0.33
        )

        g1 += et_g1
        g2 += et_g2

        if g1 > g2:
            winner = team_1
            method = "AET"

        elif g2 > g1:
            winner = team_2
            method = "AET"

        else:

            p = np.clip(
                0.5 + (xg_1 - xg_2) * 0.08,
                0.35,
                0.65,
            )

            if np.random.random() < p:
                winner = team_1
            else:
                winner = team_2

            method = "PENS"

    if return_details:

        return {
            "team_1": team_1,
            "team_2": team_2,
            "goals_1": g1,
            "goals_2": g2,
            "winner": winner,
            "method": method,
        }

    return winner