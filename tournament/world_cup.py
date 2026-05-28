import pandas as pd

from tournament.groups import (
    simulate_group
)

from tournament.knockout import (
    play_knockout_match
)


def simulate_world_cup(
    groups
):

    qualified = {}

    # GROUP STAGE
    for (
        group_name,
        teams
    ) in groups.items():

        _, table = simulate_group(
            teams
        )

        top_two = (
            table.head(2)
            .index
            .tolist()
        )

        qualified[
            f"{group_name}1"
        ] = top_two[0]

        qualified[
            f"{group_name}2"
        ] = top_two[1]

    # ROUND OF 16
    bracket = pd.read_csv(
        "data/bracket.csv"
    )

    quarter_finalists = []

    for _, row in (
        bracket.iterrows()
    ):

        team_1 = qualified[
            row["team_1"]
        ]

        team_2 = qualified[
            row["team_2"]
        ]

        winner = (
            play_knockout_match(
                team_1,
                team_2
            )
        )

        quarter_finalists.append(
            winner
        )

    return quarter_finalists