import pandas as pd

from tournament.groups import (
    simulate_group
)

from tournament.knockout import (
    play_knockout_match
)

from models.match import (
    simulate_match
)


PATHS = pd.read_csv(
    "data/knockout_paths.csv"
)

THIRD_PLACE_TABLE = (
    pd.read_csv(
        "data/third_place_permutations.csv"
    )
)

DYNAMIC_SLOTS = [
    "A1",
    "B1",
    "D1",
    "E1",
    "G1",
    "I1",
    "K1",
    "L1"
]


def play_round(
    teams,
    stats,
    verbose=False,
    round_name=""
):

    winners = []

    if verbose:

        print(f"\n{round_name.upper()}")

    round_matches = []

    for i in range(
        0,
        len(teams),
        2
    ):

        team_1 = teams[i]
        team_2 = teams[i + 1]

        g1, g2 = simulate_match(
            team_1,
            team_2
        )

        # Track goals

        stats["goals_for"][team_1] = (
            stats["goals_for"].get(team_1, 0)
            + g1
        )

        stats["goals_against"][team_1] = (
            stats["goals_against"].get(team_1, 0)
            + g2
        )

        stats["goals_for"][team_2] = (
            stats["goals_for"].get(team_2, 0)
            + g2
        )

        stats["goals_against"][team_2] = (
            stats["goals_against"].get(team_2, 0)
            + g1
        )

        if g1 > g2:

            winner = team_1
            method = "FT"

        elif g2 > g1:

            winner = team_2
            method = "FT"

        else:

            details = play_knockout_match(
                team_1,
                team_2,
                return_details=True,
            )

            winner = details["winner"]
            method = details["method"]

            loser = (
                team_2
                if winner == team_1
                else team_1
            )

            stats["fantasy_bonus"][winner] = (
                stats["fantasy_bonus"].get(winner, 0)
                + 3
            )

            stats["fantasy_bonus"][loser] = (
                stats["fantasy_bonus"].get(loser, 0)
                - 3
            )

            g1 = details["goals_1"]
            g2 = details["goals_2"]

        round_matches.append(
            {
                "team_1": team_1,
                "team_2": team_2,
                "goals_1": g1,
                "goals_2": g2,
                "winner": winner,
                "method": method,
            }
        )

        winners.append(winner)

        if verbose:

            suffix = (
                ""
                if method == "FT"
                else f" ({method})"
            )

            print(
                f"{team_1} {g1}-{g2} {team_2}"
                f" → {winner}{suffix}"
            )

    stats.setdefault(
        "knockout_matches",
        {}
    )[round_name] = round_matches

    return winners


def simulate_world_cup(
    groups,
    verbose=False
):

    stats = {
        "group": [],
        "round_32": [],
        "round_16": [],
        "quarter": [],
        "semi": [],
        "final": [],
        "champion": None,
        "goals_for": {},
        "goals_against": {},
        "fantasy_bonus": {},

        # New fields for UI
        "group_fixtures": {},
        "group_tables": {},
        "knockout_matches": {},
    }

    qualified = {}
    third_place = []

    if verbose:

        print(
            "\nGROUP STAGE"
        )

    # GROUP STAGE
    for (
        group_name,
        teams
    ) in groups.items():

        fixtures, table = (
            simulate_group(
                teams
            )
        )

        stats["group_fixtures"][group_name] = fixtures
        stats["group_tables"][group_name] = table

        # Track goals
        for (
            t1,
            g1,
            g2,
            t2
        ) in fixtures:

            stats[
                "goals_for"
            ][t1] = (
                stats[
                    "goals_for"
                ].get(
                    t1,
                    0
                ) + g1
            )

            stats[
                "goals_against"
            ][t1] = (
                stats[
                    "goals_against"
                ].get(
                    t1,
                    0
                ) + g2
            )

            stats[
                "goals_for"
            ][t2] = (
                stats[
                    "goals_for"
                ].get(
                    t2,
                    0
                ) + g2
            )

            stats[
                "goals_against"
            ][t2] = (
                stats[
                    "goals_against"
                ].get(
                    t2,
                    0
                ) + g1
            )

        if verbose:

            print(
                f"\nGroup "
                f"{group_name}"
            )

            for (
                t1,
                g1,
                g2,
                t2
            ) in fixtures:

                print(
                    f"{t1} "
                    f"{g1}-{g2} "
                    f"{t2}"
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

    third_place_sorted = sorted(
        third_place,
        key=lambda x: (
            x["points"],
            x["gd"],
            x["gf"]
        ),
        reverse=True
    )

    best_third = (
        third_place_sorted[:8]
    )

    groups_key = "".join(
        sorted(
            [
                x["group"]
                for x in best_third
            ]
        )
    )

    mapping_row = (
        THIRD_PLACE_TABLE[
            THIRD_PLACE_TABLE[
                "groups"
            ]
            == groups_key
        ]
        .iloc[0]
    )

    slot_lookup = {}

    for (
        key,
        team
    ) in qualified.items():

        slot_lookup[
            key
        ] = team

    third_lookup = {
        x["group"]:
        x["team"]
        for x in best_third
    }

    for slot in (
        DYNAMIC_SLOTS
    ):

        third_ref = (
            mapping_row[
                slot
            ]
        )

        if pd.isna(
            third_ref
        ):
            continue

        third_group = (
            str(
                third_ref
            )[0]
        )

        if (
            third_group
            in third_lookup
        ):

            slot_lookup[
                f"{slot}_OPP"
            ] = (
                third_lookup[
                    third_group
                ]
            )

    knockout_teams = []

    for _, row in (
        PATHS.iterrows()
    ):

        knockout_teams.append(
            slot_lookup[
                row["source"]
            ]
        )

    round_16 = play_round(
        knockout_teams,
        stats,
        verbose,
        "Round of 32"
    )

    quarter = play_round(
        round_16,
        stats,
        verbose,
        "Round of 16"
    )

    semi = play_round(
        quarter,
        stats,
        verbose,
        "Quarter-finals"
    )

    finalists = play_round(
        semi,
        stats,
        verbose,
        "Semi-finals"
    )

    final = play_knockout_match(
        finalists[0],
        finalists[1],
        return_details=True,
    )

    stats["knockout_matches"]["Final"] = [
        final
    ]

    stats["champion"] = final["winner"]

    return stats