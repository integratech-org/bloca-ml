import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

DEFAULT_OUT = str(
    Path(__file__).parent.parent / "data" / "mock" / "mock_telemetry_raw.csv"
)


def aggregate_batches(raw_df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for batch_id, g in raw_df.groupby("batch_id"):
        heat = g.loc[g["phase"] == "heating"]
        comp = g.loc[g["phase"] == "compression"]
        cool = g.loc[g["phase"] == "cooling"]

        if heat.empty or comp.empty or cool.empty:
            continue  # skip incomplete/malformed batches defensively

        records.append(
            {
                "batch_id": batch_id,
                "compaction_temp_c": heat["compaction_temp_c"].tail(10).mean(),
                "hydraulic_pressure_mpa": comp["hydraulic_pressure_mpa"].max(),
                "heating_duration_min": (
                    heat["elapsed_s"].max() - heat["elapsed_s"].min()
                )
                / 60.0,
                "cooling_duration_min": (
                    cool["elapsed_s"].max() - cool["elapsed_s"].min()
                )
                / 60.0,
                "compressed_height_mm": cool["compressed_height_mm"].mean(),
                "heater_current_a": heat["heater_current_a"].mean(),
            }
        )

    agg_df = pd.DataFrame(records)
    if agg_df.empty:
        raise ValueError(
            "No complete batches found after aggregation -- check input CSV."
        )
    return agg_df


def attach_dummy_labels(agg_df: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = agg_df.copy()
    df["compressive_strength_mpa"] = (
        0.03 * df["compaction_temp_c"]
        + 4.0 * df["hydraulic_pressure_mpa"]
        - 0.05 * df["compressed_height_mm"]
        + rng.normal(0, 0.4, size=len(df))
    ).clip(0, 15)
    df["quality_class"] = rng.choice([0, 1, 2], size=len(df), p=[0.7, 0.2, 0.1])
    return df


def main():
    parser = argparse.ArgumentParser(description="Dummy training script.")
    parser.add_argument(
        "--csv",
        type=str,
        default=DEFAULT_OUT,
        help="path to the CSV file containing mock telemetry data",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    raw_df = pd.read_csv(csv_path)
    print("[OK] Loaded raw telemetry data from:", csv_path)

    required_cols = {
        "batch_id",
        "elapsed_s",
        "phase",
        "compaction_temp_c",
        "hydraulic_pressure_mpa",
        "compressed_height_mm",
        "heater_current_a",
    }
    missing = required_cols - set(raw_df.columns)
    if missing:
        raise ValueError(f"CSV missing expected columns: {missing}")
    print("[OK] All expected columns present")

    # ── Aggregate batches ─────────────────────────────────────────────
    agg_df = aggregate_batches(raw_df)
    print("[OK] Aggregated batches. Number of complete batches:", len(agg_df))

    # ── Attach dummy labels ───────────────────────────────────────────
    df = attach_dummy_labels(agg_df)
    print("[OK] Attached dummy labels")

    feature_cols = [
        "compaction_temp_c",
        "hydraulic_pressure_mpa",
        "heating_duration_min",
        "cooling_duration_min",
        "compressed_height_mm",
        "heater_current_a",
    ]
    X = df[feature_cols]
    y = df["compressive_strength_mpa"]

    if len(df) < 4:
        print(
            "[WARNING] Not enough data to split into train/test sets. Using all data for training."
        )
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        print("[OK] Splitting data into train/test sets.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=7
        )

    # ── scikit-learn model ────────────────────────────────────────────
    rf = RandomForestRegressor(n_estimators=100, random_state=7)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    print(
        f"[OK] scikit-learn RandomForestRegressor trained. "
        f"MAE={mean_absolute_error(y_test, rf_pred):.3f} MPa, "
        f"R2={r2_score(y_test, rf_pred):.3f} (synthetic labels, scores are not meaningful)"
    )


if __name__ == "__main__":
    main()
