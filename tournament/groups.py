from itertools import combinations

from models.match import (
    simulate_match
)

from teams import teams


def h2h_sort_key(
    team_name,
    tied_teams,
    standings,
    h2h
):

    h2h_points = 0
    h2h_gd = 0
    h2h_gf = 0

    for opponent in tied_teams:

        if opponent == team_name:
            continue

        match = h2h.get(
            tuple(
                sorted(
                    [team_name, opponent]
                )
            )
        )

        if not match:
            continue

        t1, g1, g2, t2 = match

        if team_name == t1:
            gf = g1
            ga = g2
        else:
            gf = g2
            ga = g1

        h2h_gf += gf
        h2h_gd += (
            gf - ga
        )

        if gf > ga:
            h2h_points += 3
        elif gf == ga:
            h2h_points += 1

    overall = standings[
        team_name
    ]

    return (
        h2h_points,
        h2h_gd,
        h2h_gf,
        overall["gf"]
        - overall["ga"],
        overall["gf"],
        teams[team_name][
            "elo"
        ]
    )


def simulate_group(
    group_teams
):

    standings = {
        team: {
            "points": 0,
            "gf": 0,
            "ga": 0
        }
        for team in group_teams
    }

    h2h = {}
    fixtures = []

    for (
        team_1,
        team_2
    ) in combinations(
        group_teams,
        2
    ):

        g1, g2 = (
            simulate_match(
                team_1,
                team_2
            )
        )

        fixtures.append(
            (
                team_1,
                g1,
                g2,
                team_2
            )
        )

        h2h[
            tuple(
                sorted(
                    [
                        team_1,
                        team_2
                    ]
                )
            )
        ] = (
            team_1,
            g1,
            g2,
            team_2
        )

        standings[
            team_1
        ]["gf"] += g1

        standings[
            team_1
        ]["ga"] += g2

        standings[
            team_2
        ]["gf"] += g2

        standings[
            team_2
        ]["ga"] += g1

        if g1 > g2:

            standings[
                team_1
            ]["points"] += 3

        elif g2 > g1:

            standings[
                team_2
            ]["points"] += 3

        else:

            standings[
                team_1
            ]["points"] += 1

            standings[
                team_2
            ]["points"] += 1

    grouped = {}

    for (
        team,
        stats
    ) in standings.items():

        pts = stats[
            "points"
        ]

        if pts not in grouped:
            grouped[pts] = []

        grouped[
            pts
        ].append(team)

    sorted_points = sorted(
        grouped.keys(),
        reverse=True
    )

    final_table = []

    for pts in (
        sorted_points
    ):

        tied_teams = grouped[
            pts
        ]

        ordered = sorted(
            tied_teams,
            key=lambda t:
            h2h_sort_key(
                t,
                tied_teams,
                standings,
                h2h
            ),
            reverse=True
        )

        for team in ordered:

            final_table.append(
                (
                    team,
                    standings[
                        team
                    ]
                )
            )

    return (
        fixtures,
        final_table
    )