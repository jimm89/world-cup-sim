from tournament.groups import (
    simulate_group
)


def simulate_world_cup(
    groups
):

    qualified = {}

    for group_name, teams in (
        groups.items()
    ):

        _, table = simulate_group(
            teams
        )

        top_two = (
            table.head(2)
            .index
            .tolist()
        )

        qualified[
            group_name
        ] = top_two

    return qualified