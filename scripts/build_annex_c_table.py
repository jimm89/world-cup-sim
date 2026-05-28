import pandas as pd
from itertools import combinations

# Dynamic winner slots in FIFA bracket
SLOTS = [
    "A1",
    "B1",
    "D1",
    "E1",
    "G1",
    "I1",
    "K1",
    "L1"
]

# Official allowed third-place groups
ALLOWED = {
    "A1": set("CEFHI"),
    "B1": set("EFGIJ"),
    "D1": set("BEFIJ"),
    "E1": set("ABCDF"),
    "G1": set("AEHIJ"),
    "I1": set("CDFGH"),
    "K1": set("DEIJL"),
    "L1": set("EHIJK"),
}

GROUPS = list("ABCDEFGHIJKL")


def assign_slot(
    remaining,
    allowed
):
    """
    Deterministic assignment:
    chooses highest-ranked
    remaining group that
    FIFA allows.
    """

    valid = sorted(
        list(
            remaining & allowed
        )
    )

    if not valid:
        return None

    return valid[0]


rows = []

for combo in combinations(
    GROUPS,
    8
):

    combo_set = set(combo)

    row = {
        "groups":
            "".join(combo)
    }

    remaining = set(combo)

    for slot in SLOTS:

        pick = assign_slot(
            remaining,
            ALLOWED[slot]
        )

        if pick is None:
            row[slot] = ""
        else:
            row[
                slot
            ] = (
                f"{pick}3"
            )
            remaining.remove(
                pick
            )

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
    f"rows"
)