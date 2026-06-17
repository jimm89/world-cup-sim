import streamlit as st

from simulator import run_simulations
from groups_data import groups

st.set_page_config(
    page_title="FIFA 2026 World Cup Simulator",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ FIFA 2026 World Cup Simulator")

st.write(
    "Monte Carlo simulation of the 2026 FIFA World Cup."
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.header("Simulation")

n_sims = st.sidebar.number_input(
    "Number of simulations",
    min_value=1,
    max_value=100000,
    value=10000,
    step=1000,
)

if st.sidebar.button(
    "▶ Run Simulation",
    use_container_width=True,
):

    with st.spinner("Running simulations..."):

        results, runtime = run_simulations(
            groups,
            n_sims,
        )

    st.session_state["results"] = results
    st.session_state["runtime"] = runtime
    st.session_state["n_sims"] = n_sims

# ----------------------------------------------------
# Nothing run yet
# ----------------------------------------------------

if "results" not in st.session_state:

    st.info(
        "Click **Run Simulation** to begin."
    )
    st.stop()

results = st.session_state["results"]
runtime = st.session_state["runtime"]
n_sims = st.session_state["n_sims"]

# ----------------------------------------------------
# Header metrics
# ----------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Simulations",
    f"{n_sims:,}"
)

c2.metric(
    "Teams",
    len(results)
)

c3.metric(
    "Runtime",
    f"{runtime:.2f}s"
)

st.divider()

# ----------------------------------------------------
# Top contenders
# ----------------------------------------------------

st.subheader("🏆 Championship Favourites")

top10 = (
    results
    .sort_values(
        "champion_pct",
        ascending=False,
    )
    .head(10)
)

for _, row in top10.iterrows():

    st.progress(
        row["champion_pct"] / 100,
        text=f'{row["team"]}  ({row["champion_pct"]:.2f}%)'
    )

st.divider()

# ----------------------------------------------------
# Chart + table
# ----------------------------------------------------

left, right = st.columns([1, 2])

with left:

    st.subheader("Champion %")

    chart = (
        results
        .sort_values(
            "champion_pct",
            ascending=False,
        )
        .set_index("team")
    )

    st.bar_chart(
        chart["champion_pct"]
    )

with right:

    st.subheader("Teams")

    display = (
        results[
            [
                "team",
                "group",
                "pot",
                "champion_pct",
                "avg_gf",
                "avg_ga",
            ]
        ]
        .rename(
            columns={
                "team": "Team",
                "group": "Group",
                "pot": "Pot",
                "champion_pct": "Champion %",
                "avg_gf": "Avg Goals For",
                "avg_ga": "Avg Goals Against",
            }
        )
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )

st.download_button(
    "📥 Download CSV",
    display.to_csv(index=False),
    "world_cup_results.csv",
    "text/csv",
)