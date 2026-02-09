import sqlite3
from pathlib import Path

import pandas as pd


# ----------------------------
# Paths
# ----------------------------

GOLD = Path("data/gold")
DB_PATH = Path("warehouse/vct.sqlite")

DB_PATH.parent.mkdir(exist_ok=True)


# ----------------------------
# Connect (Persistent DB)
# ----------------------------

con = sqlite3.connect(DB_PATH)


# ----------------------------
# Helper: Load Parquet -> Table
# ----------------------------

def load_table(name: str, parquet_path: Path) -> None:
    print(f"Loading {name}...")

    df = pd.read_parquet(parquet_path)
    df.to_sql(name, con, if_exists="replace", index=False)


# ----------------------------
# Load Dimensions
# ----------------------------

DIM = GOLD / "dimensions"

load_table("dim_player", DIM / "dim_player.parquet")
load_table("dim_team", DIM / "dim_team.parquet")
load_table("dim_tournament", DIM / "dim_tournament.parquet")
load_table("dim_match", DIM / "dim_match.parquet")
load_table("dim_map", DIM / "dim_map.parquet")
load_table("dim_agent", DIM / "dim_agent.parquet")


# ----------------------------
# Load Facts
# ----------------------------

FACT = GOLD / "facts"

load_table(
    "fact_player_match_map_stats",
    FACT / "fact_player_match_map_stats.parquet",
)

load_table(
    "fact_match_results",
    FACT / "fact_match_results.parquet",
)

load_table(
    "fact_player_competition_stats",
    FACT / "fact_player_competition_stats.parquet",
)

load_table(
    "fact_agent_meta",
    FACT / "fact_agent_meta.parquet",
)


# ----------------------------
# Create Indexes
# ----------------------------

print("Creating indexes...")

con.execute(
    """
CREATE INDEX IF NOT EXISTS idx_fact_player_match
ON fact_player_match_map_stats(match_id, game_id);
"""
)

con.execute(
    """
CREATE INDEX IF NOT EXISTS idx_fact_player
ON fact_player_match_map_stats(player_id);
"""
)

con.execute(
    """
CREATE INDEX IF NOT EXISTS idx_fact_team
ON fact_match_results(winning_team_id);
"""
)


# ----------------------------
# Analyze
# ----------------------------

print("Running ANALYZE...")

con.execute("ANALYZE")


# ----------------------------
# Close
# ----------------------------

con.close()

print("SQLite warehouse ready.")
