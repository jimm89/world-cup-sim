from collections import Counter

from tournament.groups import (
    simulate_group
)


def simulate_group_monte_carlo(
    group_teams,
    n_sims=10_000
):

    qualification_counter = (
        Counter()
    )

    group_winner_counter = (
        Counter()
    )

    for _ in range(n_sims):

        _, table = simulate_group(
            group_teams
        )

        qualified = (
            table.head(2)
            .index
            .tolist()
        )

        winner = table.index[0]

        group_winner_counter[
            winner
        ] += 1

        for team in qualified:
            qualification_counter[
                team
            ] += 1

    return (
        qualification_counter,
        group_winner_counter
    )