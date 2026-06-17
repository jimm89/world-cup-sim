import streamlit as st

from groups_data import groups
from tournament.world_cup import simulate_world_cup

st.set_page_config(
    page_title="Single Tournament",
    page_icon="🎲",
    layout="wide",
)

st.title("🎲 Single Tournament")

st.write(
    "Run one complete simulated FIFA World Cup."
)

if st.button(
    "▶ Simulate Tournament",
    use_container_width=True,
):

    stats = simulate_world_cup(
        groups,
        verbose=False,
    )

    # -------------------------
    # GROUP STAGE
    # -------------------------

    st.header("Group Stage")

    for group in sorted(
        stats["group_fixtures"]
    ):

        st.subheader(
            f"Group {group}"
        )

        fixtures = stats[
            "group_fixtures"
        ][group]

        for (
            team_1,
            goals_1,
            goals_2,
            team_2,
        ) in fixtures:

            st.write(
                f"{team_1} {goals_1}–{goals_2} {team_2}"
            )

        st.markdown("**Table**")

        table = stats[
            "group_tables"
        ][group]

        table_rows = []

        for team, row in table:

            table_rows.append(
                {
                    "Team": team,
                    "Pts": row["points"],
                    "GF": row["gf"],
                    "GA": row["ga"],
                    "GD": row["gf"] - row["ga"],
                }
            )

        st.table(table_rows)

    # -------------------------
    # KNOCKOUT
    # -------------------------

    st.header("Knockout Stage")

    order = [
        "Round of 32",
        "Round of 16",
        "Quarter-finals",
        "Semi-finals",
        "Final",
    ]

    for round_name in order:

        if (
            round_name
            not in stats["knockout_matches"]
        ):
            continue

        st.subheader(
            round_name
        )

        for match in stats[
            "knockout_matches"
        ][round_name]:

            suffix = ""

            if (
                match["method"]
                == "AET"
            ):
                suffix = " (AET)"

            elif (
                match["method"]
                == "PENS"
            ):
                suffix = " (Pens)"

            st.write(
                f'{match["team_1"]} '
                f'{match["goals_1"]}–{match["goals_2"]} '
                f'{match["team_2"]}'
                f'{suffix}'
            )

    st.success(
        f'🏆 Champion: {stats["champion"]}'
    )