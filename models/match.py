import random

from models.goals import (
    sample_goals
)

from models.ratings import (
    expected_goals
)


def simulate_match(
    team_1,
    team_2
):

    xg_1, xg_2 = (
        expected_goals(
            team_1,
            team_2
        )
    )

    goals_1 = sample_goals(
        xg_1
    )

    goals_2 = sample_goals(
        xg_2
    )

    # Football-style low score adjustment
    low_score = (
        goals_1 <= 1
        and goals_2 <= 1
    )

    if low_score:

        roll = random.random()

        # boost 0-0 slightly
        if (
            goals_1 == 0
            and goals_2 == 0
            and roll < 0.10
        ):
            return 0, 0

        # boost 1-1 slightly
        if (
            goals_1 == 1
            and goals_2 == 1
            and roll < 0.10
        ):
            return 1, 1

        # slightly suppress open low scores
        if (
            abs(
                goals_1
                - goals_2
            ) == 1
            and roll < 0.08
        ):
            return 1, 1

    return (
        goals_1,
        goals_2
    )