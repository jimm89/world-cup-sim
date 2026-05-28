from groups_data import groups

from tournament.world_cup import (
    simulate_world_cup
)

quarter_finalists = (
    simulate_world_cup(
        groups
    )
)

print(
    "\nQUARTER FINALISTS\n"
)

for team in (
    quarter_finalists
):

    print(team)