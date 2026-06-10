from collections import defaultdict
import time

from groups_data import groups
from tournament.world_cup import (
    simulate_world_cup
)

N_SIMS = 100000

start = time.time()

goals_for = defaultdict(int)
goals_against = defaultdict(int)
champions = defaultdict(int)
fantasy_bonus = defaultdict(int)

POT_WEIGHTS = {
    1: (1, -4),
    2: (2, -3),
    3: (3, -2),
    4: (4, -1)
}

team_pot = {}
team_group = {}
all_teams = []

# Build metadata
for (
    group_name,
    teams
) in groups.items():

    for i, team in enumerate(
        teams
    ):

        pot = i + 1

        team_pot[
            team
        ] = pot

        team_group[
            team
        ] = group_name

        all_teams.append(
            team
        )

# Simulations
for _ in range(
    N_SIMS
):

    stats = (
        simulate_world_cup(
            groups,
            verbose=(
                N_SIMS == 1
            )
        )
    )

    for (
        team,
        gf
    ) in (
        stats[
            "goals_for"
        ].items()
    ):

        goals_for[
            team
        ] += gf

    for (
        team,
        ga
    ) in (
        stats[
            "goals_against"
        ].items()
    ):

        goals_against[
            team
        ] += ga

    for (
        team,
        bonus
    ) in (
        stats[
            "fantasy_bonus"
        ].items()
    ):

        fantasy_bonus[
            team
        ] += bonus

    champions[
        stats[
            "champion"
        ]
    ] += 1


# CSV header
print(
    "Team,Pot,Group,Fantasy_Score"
)

results = []

for team in all_teams:

    avg_gf = (
        goals_for[
            team
        ]
        / N_SIMS
    )

    avg_ga = (
        goals_against[
            team
        ]
        / N_SIMS
    )

    avg_bonus = (
        fantasy_bonus[
            team
        ]
        / N_SIMS
    )

    pot = (
        team_pot[
            team
        ]
    )

    group = (
        team_group[
            team
        ]
    )

    c1, c2 = (
        POT_WEIGHTS[
            pot
        ]
    )

    fantasy_score = (
        c1 * avg_gf
        + c2 * avg_ga
        + avg_bonus
    )

    results.append(
        (
            fantasy_score,
            team,
            pot,
            group
        )
    )

# Sort highest fantasy score first
results.sort(
    reverse=True
)

for (
    fantasy_score,
    team,
    pot,
    group
) in results:

    print(
        f"{team},"
        f"{pot},"
        f"{group},"
        f"{fantasy_score:.2f}"
    )

end = time.time()

print(
    f"\nRuntime: "
    f"{end - start:.2f}s"
)