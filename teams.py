import pandas as pd


teams_df = pd.read_csv(
    "data/teams.csv"
)

elo_df = pd.read_csv(
    "data/real_elo.csv"
)

df = teams_df.merge(
    elo_df,
    on="team",
    how="left",
    suffixes=("", "_real")
)

df["elo"] = (
    df["elo_real"]
    .fillna(df["elo"])
)

df = df.drop(
    columns=["elo_real"]
)

teams = (
    df.set_index("team")
    .to_dict(orient="index")
)