from groups_data import groups
from tournament.world_cup import (
    simulate_world_cup
)

qualified = (
    simulate_world_cup(
        groups
    )
)

print(
    "\nQUALIFIED TEAMS\n"
)

for group, teams in (
    qualified.items()
):

    print(
        f"Group {group}: "
        f"{teams}"
    )