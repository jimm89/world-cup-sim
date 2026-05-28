import pandas as pd
import requests
from io import StringIO


URL = (
    "https://en.wikipedia.org/wiki/"
    "Template:2026_FIFA_World_Cup_third-place_table"
)


def fifa_to_internal(value):

    value = str(value).strip()

    if (
        len(value) == 2
        and value[0] == "3"
        and value[1] in "ABCDEFGHIJKL"
    ):
        return f"{value[1]}3"

    return value


print(
    "Loading FIFA Annex C..."
)

headers = {
    "User-Agent":
    "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers
)

response.raise_for_status()

tables = pd.read_html(
    StringIO(
        response.text
    )
)

target = None

for table in tables:

    cols = list(
        table.columns
    )

    if (
        "1A vs" in cols
        and "1L vs" in cols
    ):
        target = table
        break

if target is None:

    raise ValueError(
        "Could not find "
        "Annex C table"
    )

print(
    "Found Annex C table"
)

rows = []

for _, row in (
    target.iterrows()
):

    groups = []

    # Columns 1–12 contain
    # qualifying groups
    for i in range(
        1,
        13
    ):

        value = str(
            row.iloc[i]
        ).strip()

        if (
            value != "nan"
            and len(value) == 1
            and value
            in "ABCDEFGHIJKL"
        ):
            groups.append(
                value
            )

    groups = sorted(
        groups
    )

    if len(
        groups
    ) != 8:

        continue

    out = {
        "groups":
            "".join(
                groups
            ),

        "A1":
            fifa_to_internal(
                row[
                    "1A vs"
                ]
            ),

        "B1":
            fifa_to_internal(
                row[
                    "1B vs"
                ]
            ),

        "D1":
            fifa_to_internal(
                row[
                    "1D vs"
                ]
            ),

        "E1":
            fifa_to_internal(
                row[
                    "1E vs"
                ]
            ),

        "G1":
            fifa_to_internal(
                row[
                    "1G vs"
                ]
            ),

        "I1":
            fifa_to_internal(
                row[
                    "1I vs"
                ]
            ),

        "K1":
            fifa_to_internal(
                row[
                    "1K vs"
                ]
            ),

        "L1":
            fifa_to_internal(
                row[
                    "1L vs"
                ]
            ),
    }

    rows.append(
        out
    )

df = pd.DataFrame(
    rows
)

df = df.drop_duplicates(
    subset=[
        "groups"
    ]
)

df.to_csv(
    "data/third_place_permutations.csv",
    index=False
)

print(
    f"Saved "
    f"{len(df)} "
    f"real FIFA rows"
)