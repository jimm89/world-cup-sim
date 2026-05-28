import random

from models.match import (
    simulate_match
)


def play_knockout_match(
    team_1,
    team_2
):

    g1, g2 = simulate_match(
        team_1,
        team_2
    )

    #print(
        #f"{team_1} {g1}-{g2} "
        #f"{team_2}"
    #)

    if g1 > g2:
        return team_1

    if g2 > g1:
        return team_2

    # penalties
    winner = random.choice(
        [team_1, team_2]
    )

    #print(
        #f"Penalties winner: "
        #f"{winner}"
    #)

    return winner