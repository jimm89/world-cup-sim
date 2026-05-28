from collections import Counter

from groups_data import groups
from tournament.world_cup import (
    simulate_world_cup
)

N_SIMS = 10_000

group_counter = Counter()
quarter_counter = Counter()
semi_counter = Counter()
final_counter = Counter()
champion_counter = Counter()


for _ in range(N_SIMS):

    stats = simulate_world_cup(
        groups
    )

    for team in (
        stats["group"]
    ):
        group_counter[
            team
        ] += 1

    for team in (
        stats["quarter"]
    ):
        quarter_counter[
            team
        ] += 1

    for team in (
        stats["semi"]
    ):
        semi_counter[
            team
        ] += 1

    for team in (
        stats["final"]
    ):
        final_counter[
            team
        ] += 1

    champion_counter[
        stats["champion"]
    ] += 1


all_teams = []

for group in (
    groups.values()
):
    all_teams.extend(
        group
    )


print(
    f"\nWORLD CUP "
    f"({N_SIMS:,} SIMS)\n"
)

for team in sorted(
    all_teams
):

    group_pct = (
        group_counter[team]
        / N_SIMS
        * 100
    )

    qf_pct = (
        quarter_counter[team]
        / N_SIMS
        * 100
    )

    sf_pct = (
        semi_counter[team]
        / N_SIMS
        * 100
    )

    final_pct = (
        final_counter[team]
        / N_SIMS
        * 100
    )

    champion_pct = (
        champion_counter[team]
        / N_SIMS
        * 100
    )

    print(
        f"{team:<15}"
        f"Group: {group_pct:>5.1f}% "
        f"| QF: {qf_pct:>5.1f}% "
        f"| SF: {sf_pct:>5.1f}% "
        f"| Final: {final_pct:>5.1f}% "
        f"| Win: {champion_pct:>5.1f}%"
    )