import pandas as pd
from copy import deepcopy

# Load the master team data
_df = pd.read_csv("data/teams.csv")

_original_teams = (
    _df
    .set_index("team")
    .to_dict(orient="index")
)

# Working copy used by the simulator
teams = deepcopy(_original_teams)


def get_teams():
    return teams


def get_team(team):
    return teams[team]


def get_elo(team):
    return teams[team]["elo"]


def set_elo(team, elo):
    teams[team]["elo"] = float(elo)


def apply_elo_overrides(overrides):
    """
    Apply a dictionary of temporary Elo ratings.

    Example:
        {
            "England": 2100,
            "France": 2050
        }
    """

    if overrides is None:
        return

    for team, elo in overrides.items():

        if team in teams:

            teams[team]["elo"] = float(elo)


def reset_elos():
    """
    Restore all Elo ratings from teams.csv.
    """

    global teams

    teams = deepcopy(_original_teams)


def get_all_elo():
    """
    Returns a simple dictionary of
    {team: elo}
    """

    return {
        team: data["elo"]
        for team, data in teams.items()
    }