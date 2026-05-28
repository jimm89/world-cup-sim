import pandas as pd

# Official FIFA columns
COLUMNS = [
    "groups",
    "A1",
    "B1",
    "D1",
    "E1",
    "G1",
    "I1",
    "K1",
    "L1"
]

rows = []

# We will paste FIFA Annex C
# mappings here shortly

df = pd.DataFrame(
    rows,
    columns=COLUMNS
)

df.to_csv(
    "data/third_place_permutations.csv",
    index=False
)

print(
    f"Saved "
    f"{len(df)} rows"
)