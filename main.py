from collections import defaultdict
import time

from groups_data import groups
from tournament.world_cup import (
    simulate_world_cup
)

N_SIMS = 100

start = time.time()

goals_for = defaultdict(int)
goals_against = defaultdict(int)
champions = defaultdict(int)

# Fantasy scoring weights
POT_WEIGHTS = {
    1: (1, -4),
    2: (2, -3),
    3: (3, -2),
    4: (4, -1)
}

# Build team list + pot lookup
all_teams = []
team_pot = {}

for group in groups.values():

    for i, team in enumerate(group):

        pot = i + 1

        all_teams.append(
            team
        )

        team_pot[
            team
        ] = pot

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

    # Goals
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

    # Champion
    champions[
        stats[
            "champion"
        ]
    ] += 1


print(
    f"\nWORLD CUP "
    f"({N_SIMS:,} SIMS)\n"
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

    champion_pct = (
        champions[
            team
        ]
        / N_SIMS
        * 100
    )

    pot = team_pot[
        team
    ]

    c1, c2 = (
        POT_WEIGHTS[
            pot
        ]
    )

    fantasy_score = (
        c1 * avg_gf
        + c2 * avg_ga
    )

    results.append(
        (
            fantasy_score,
            team,
            avg_gf,
            avg_ga,
            champion_pct,
            pot
        )
    )

# Sort by fantasy score
results.sort(
    reverse=True
)

for (
    fantasy_score,
    team,
    avg_gf,
    avg_ga,
    champion_pct,
    pot
) in results:

    print(
        f"{team:<22}"
        f"Pot {pot} | "
        f"GF: {avg_gf:>5.2f} | "
        f"GA: {avg_ga:>5.2f} | "
        f"Champion: {champion_pct:>6.2f}% | "
        f"Fantasy: {fantasy_score:>6.2f}"
    )

end = time.time()

print(
    f"\nRuntime: "
    f"{end - start:.2f}s"
)