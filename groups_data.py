import pandas as pd


df = pd.read_csv(
    "data/groups.csv"
)

groups = (
    df.groupby("group")
    ["team"]
    .apply(list)
    .to_dict()
)