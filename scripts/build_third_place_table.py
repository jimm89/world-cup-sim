from itertools import combinations
import pandas as pd


GROUPS = list("ABCDEFGHIJKL")


def placeholder_mapping(
    qualifying_groups
):
    """
    Temporary mapping.
    We will replace this
    with FIFA Annex C.
    """

    thirds = sorted(
        qualifying_groups
    )

    return {
        "A1": f"{thirds[0]}3",
        "B1": f"{thirds[1]}3",
        "D1": f"{thirds[2]}3",
        "E1": f"{thirds[3]}3",
        "G1": f"{thirds[4]}3",
        "I1": f"{thirds[5]}3",
        "K1": f"{thirds[6]}3",
        "L1": f"{thirds[7]}3",
    }


rows = []

for combo in combinations(
    GROUPS,
    8
):

    combo_key = "".join(combo)

    mapping = (
        placeholder_mapping(
            combo
        )
    )

    row = {
        "groups":
            combo_key
    }

    row.update(mapping)

    rows.append(row)


df = pd.DataFrame(
    rows
)

df.to_csv(
    "data/third_place_permutations.csv",
    index=False
)

print(
    f"Built "
    f"{len(df)} "
    f"permutations"
)