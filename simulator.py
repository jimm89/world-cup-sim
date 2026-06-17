import time
from collections import defaultdict

import pandas as pd

from teams import (
    apply_elo_overrides,
    reset_elos,
    get_all_elo,
)

from tournament.world_cup import simulate_world_cup

POT_WEIGHTS = {
    1: (1, -4),
    2: (2, -3),
    3: (3, -2),
    4: (4, -1),
}


def run_simulations(
    groups,
    n_sims=10000,
    elo_overrides=None,
):

    reset_elos()
    apply_elo_overrides(
        elo_overrides
    )

    start = time.time()

    goals_for = defaultdict(int)
    goals_against = defaultdict(int)
    champions = defaultdict(int)
    fantasy_bonus = defaultdict(int)

    team_pot = {}
    team_group = {}

    for group_name, teams in groups.items():

        for i, team in enumerate(teams):

            team_pot[team] = i + 1
            team_group[team] = group_name

    for _ in range(n_sims):

        stats = simulate_world_cup(
            groups,
            verbose=(n_sims == 1),
        )

        for team, gf in stats["goals_for"].items():
            goals_for[team] += gf

        for team, ga in stats["goals_against"].items():
            goals_against[team] += ga

        for team, bonus in stats["fantasy_bonus"].items():
            fantasy_bonus[team] += bonus

        champions[
            stats["champion"]
        ] += 1

    current_elos = get_all_elo()

    rows = []

    for team in sorted(team_pot):

        pot = team_pot[team]

        c1, c2 = POT_WEIGHTS[pot]

        avg_gf = goals_for[team] / n_sims
        avg_ga = goals_against[team] / n_sims
        avg_bonus = fantasy_bonus[team] / n_sims

        fantasy_score = (
            c1 * avg_gf
            + c2 * avg_ga
            + avg_bonus
        )

        rows.append(
            {
                "team": team,
                "group": team_group[team],
                "pot": pot,
                "elo": current_elos[team],
                "avg_gf": avg_gf,
                "avg_ga": avg_ga,
                "champion_pct": (
                    champions[team]
                    / n_sims
                    * 100
                ),
                "fantasy_score": fantasy_score,
            }
        )

    df = (
        pd.DataFrame(rows)
        .sort_values(
            "champion_pct",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    runtime = time.time() - start

    return df, runtime