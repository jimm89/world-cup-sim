import pandas as pd

from tournament.groups import (
    simulate_group
)

from tournament.knockout import (
    play_knockout_match
)


PATHS = pd.read_csv(
    "data/knockout_paths.csv"
)


def play_round(teams):

    winners = []

    for i in range(
        0,
        len(teams),
        2
    ):

        winner = (
            play_knockout_match(
                teams[i],
                teams[i + 1]
            )
        )

        winners.append(
            winner
        )

    return winners


def simulate_world_cup(
    groups
):

    stats = {
        "group": [],
        "round_32": [],
        "round_16": [],
        "quarter": [],
        "semi": [],
        "final": [],
        "champion": None
    }

    qualified = {}
    third_place = []

    # GROUP STAGE
    for (
        group_name,
        teams
    ) in groups.items():

        _, table = (
            simulate_group(
                teams
            )
        )

        winner = table[0][0]
        runner_up = table[1][0]
        third = table[2]

        qualified[
            f"{group_name}1"
        ] = winner

        qualified[
            f"{group_name}2"
        ] = runner_up

        stats[
            "group"
        ].extend(
            [winner, runner_up]
        )

        third_place.append(
            {
                "group":
                    group_name,
                "team":
                    third[0],
                "points":
                    third[1]["points"],
                "gd":
                    (
                        third[1]["gf"]
                        - third[1]["ga"]
                    ),
                "gf":
                    third[1]["gf"]
            }
        )

    # BEST THIRD-PLACE TEAMS
    third_place_sorted = sorted(
        third_place,
        key=lambda x: (
            x["points"],
            x["gd"],
            x["gf"]
        ),
        reverse=True
    )

    best_third = [
        x["team"]
        for x in (
            third_place_sorted[:8]
        )
    ]

    stats[
        "group"
    ].extend(
        best_third
    )

    # SLOT LOOKUP
    slot_lookup = {}

    for (
        key,
        team
    ) in qualified.items():

        slot_lookup[
            key
        ] = team

    for i, team in enumerate(
        best_third,
        start=1
    ):

        slot_lookup[
            f"Third{i}"
        ] = team

    # ROUND OF 32 BRACKET
    knockout_teams = []

    for _, row in (
        PATHS.iterrows()
    ):

        knockout_teams.append(
            slot_lookup[
                row["source"]
            ]
        )

    stats[
        "round_32"
    ].extend(
        knockout_teams
    )

    # ROUND OF 32
    round_16 = (
        play_round(
            knockout_teams
        )
    )

    stats[
        "round_16"
    ].extend(
        round_16
    )

    # ROUND OF 16
    quarter_finalists = (
        play_round(
            round_16
        )
    )

    stats[
        "quarter"
    ].extend(
        quarter_finalists
    )

    # QUARTERS
    semi_finalists = (
        play_round(
            quarter_finalists
        )
    )

    stats[
        "semi"
    ].extend(
        semi_finalists
    )

    # SEMIS
    finalists = (
        play_round(
            semi_finalists
        )
    )

    stats[
        "final"
    ].extend(
        finalists
    )

    # FINAL
    champion = (
        play_knockout_match(
            finalists[0],
            finalists[1]
        )
    )

    stats[
        "champion"
    ] = champion

    return stats