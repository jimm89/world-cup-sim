import pandas as pd

df = pd.read_csv(
    "data/teams.csv"
)

teams = (
    df.set_index("team")
    .to_dict(orient="index")
)