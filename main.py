from collections import Counter
import matplotlib.pyplot as plt

from models.match import simulate_match
from models.ratings import expected_goals

TEAM_1 = "England"
TEAM_2 = "Brazil"

N_SIMS = 100_000

score_counter = Counter()

team_1_wins = 0
team_2_wins = 0
draws = 0


for _ in range(N_SIMS):

    g1, g2 = simulate_match(
        TEAM_1,
        TEAM_2
    )

    score_counter[(g1, g2)] += 1

    if g1 > g2:
        team_1_wins += 1
    elif g2 > g1:
        team_2_wins += 1
    else:
        draws += 1


xg_1, xg_2 = expected_goals(
    TEAM_1,
    TEAM_2
)

print(f"{TEAM_1} xG: {xg_1:.2f}")
print(f"{TEAM_2} xG: {xg_2:.2f}")

print(f"{TEAM_1} win %: {team_1_wins / N_SIMS:.2%}")
print(f"{TEAM_2} win %: {team_2_wins / N_SIMS:.2%}")
print(f"Draw %: {draws / N_SIMS:.2%}")


top_scores = score_counter.most_common(10)

labels = [
    f"{s[0]}-{s[1]}"
    for s, _ in top_scores
]

values = [
    c / N_SIMS * 100
    for _, c in top_scores
]


plt.figure(figsize=(10, 5))
plt.bar(labels, values)

plt.title(
    f"Most likely scorelines\n"
    f"{TEAM_1} vs {TEAM_2}"
)

plt.ylabel("Probability (%)")
plt.xlabel("Scoreline")

plt.tight_layout()
plt.savefig("score_distribution.png")
print("Saved chart as score_distribution.png")