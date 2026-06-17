from simulator import run_simulations
from groups_data import groups

N_SIMS = 10_000

results, runtime = run_simulations(
    groups,
    N_SIMS,
)

print(
    results[
        [
            "team",
            "pot",
            "group",
            "fantasy_score",
        ]
    ].rename(
        columns={
            "team": "Team",
            "pot": "Pot",
            "group": "Group",
            "fantasy_score": "Fantasy_Score",
        }
    ).to_csv(
        index=False,
        float_format="%.2f",
    )
)

print(
    f"Runtime: {runtime:.2f}s"
)