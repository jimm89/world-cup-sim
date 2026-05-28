from models.match import (
    simulate_match
)


def simulate_group(group_teams):

    standings = {
        team: {
            "points": 0,
            "gf": 0,
            "ga": 0
        }
        for team in group_teams
    }

    fixtures = []

    for i in range(
        len(group_teams)
    ):
        for j in range(
            i + 1,
            len(group_teams)
        ):

            team_1 = (
                group_teams[i]
            )

            team_2 = (
                group_teams[j]
            )

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

    # Sort without pandas
    sorted_table = sorted(
        standings.items(),
        key=lambda x: (
            x[1]["points"],
            x[1]["gf"]
            - x[1]["ga"],
            x[1]["gf"]
        ),
        reverse=True
    )

    table = [
        team[0]
        for team in sorted_table
    ]

    return fixtures, table