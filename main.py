from collections import Counter

from groups_data import groups
from tournament.world_cup import (
    simulate_world_cup
)

N_SIMS = 1000

champions = Counter()

for _ in range(N_SIMS):

    champion = (
        simulate_world_cup(
            groups
        )
    )

    champions[
        champion
    ] += 1


print(
    f"\nWORLD CUP RESULTS "
    f"({N_SIMS:,} SIMS)\n"
)

for team, wins in (
    champions.most_common()
):

    probability = (
        wins
        / N_SIMS
        * 100
    )

    print(
        f"{team:<15}"
        f"{probability:>6.2f}%"
    )