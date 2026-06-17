import random

from models.goals import (
    sample_goals,
)

from models.ratings import (
    expected_goals,
)


def simulate_match(
    team_1,
    team_2,
):

    xg_1, xg_2 = expected_goals(
        team_1,
        team_2,
    )

    goals_1 = sample_goals(xg_1)
    goals_2 = sample_goals(xg_2)

    # Football-style adjustment to make
    # low-scoring draws a little more common.
    if goals_1 <= 1 and goals_2 <= 1:

        r = random.random()

        # Encourage 0-0
        if goals_1 == 0 and goals_2 == 0 and r < 0.10:
            return 0, 0

        # Encourage 1-1
        if goals_1 == 1 and goals_2 == 1 and r < 0.10:
            return 1, 1

        # Reduce 1-0 / 0-1 slightly
        if abs(goals_1 - goals_2) == 1 and r < 0.08:
            return 1, 1

    return (
        goals_1,
        goals_2,
    )