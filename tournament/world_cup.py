import pandas as pd

from tournament.groups import simulate_group
from tournament.knockout import (
    play_knockout_match
)


def simulate_world_cup(groups):

    qualified = {}

    # GROUP STAGE
    for group_name, teams in groups.items():

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

    round_16_winners = []

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

        round_16_winners.append(
            winner
        )

    # QUARTER FINALS
    quarter_final_winners = []

    for i in range(
        0,
        len(round_16_winners),
        2
    ):

        winner = (
            play_knockout_match(
                round_16_winners[i],
                round_16_winners[i + 1]
            )
        )

        quarter_final_winners.append(
            winner
        )

    # SEMI FINALS
    semi_final_winners = []

    for i in range(
        0,
        len(quarter_final_winners),
        2
    ):

        winner = (
            play_knockout_match(
                quarter_final_winners[i],
                quarter_final_winners[i + 1]
            )
        )

        semi_final_winners.append(
            winner
        )

    # FINAL
    champion = (
        play_knockout_match(
            semi_final_winners[0],
            semi_final_winners[1]
        )
    )

    return champion