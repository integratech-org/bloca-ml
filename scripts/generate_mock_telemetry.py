import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_OUT = str(
    Path(__file__).parent.parent / "data" / "mock" / "mock_telemetry_raw.csv"
)

AMBIENT_TEMP_C = 28.0  # Typical ambient temperature in the workshop, in degrees Celsius
SAMPLE_HZ = 1  # 1 sample per second


def simulate_batch(batch_id: str, rng: np.random.Generator) -> pd.DataFrame:
    target_temp_c = rng.uniform(
        120, 180
    )  # operating target range for compaction_temp_c
    heating_tau = rng.uniform(220, 420)  # time constant for heating phase in seconds
    heating_duration = rng.uniform(600, 1500)  # heating duration in seconds

    peak_pressure = rng.uniform(0.15, 0.6)  # peak hydraulic pressure in MPa
    raw_height = rng.uniform(90, 140)  # initial raw height in mm
    final_height = rng.uniform(50, 60)  # final compressed height in mm
    compression_duration = rng.uniform(20, 60)  # compression duration in seconds

    cooling_tau = rng.uniform(180, 360)  # time constant for cooling phase in seconds
    cooling_duration = rng.uniform(480, 1200)  # cooling duration in seconds

    heater_current_nominal = rng.uniform(2.5, 7.5)  # nominal heater current in Amps

    # ===========================================
    # phase 1 - heating
    # ===========================================
    n_heat = int(heating_duration * SAMPLE_HZ)
    t_heat = np.arange(n_heat) / SAMPLE_HZ

    temp_heat = (
        AMBIENT_TEMP_C
        + (target_temp_c - AMBIENT_TEMP_C)
        * (1 - np.exp(-t_heat / heating_tau))  # newton's law of heating
        + 0.6 * np.sin(t_heat / 15.0)  # sine wave riple
        + rng.normal(0, 0.35, size=n_heat)  # random noise (gaussian)
    )
    current_heat = (
        heater_current_nominal
        + 0.3 * np.sin(t_heat / 4.0)  # sine wave
        + rng.normal(0, 0.15, size=n_heat)  # random noise (gaussian)
    )
    pressure_heat = np.clip(
        rng.normal(0.01, 0.005, size=n_heat), 0, None
    )  # sensor floor noise, ~0 before compression
    height_heat = raw_height + rng.normal(0, 0.4, size=n_heat)

    heat_df = pd.DataFrame(
        {
            "elapsed_s": t_heat,
            "phase": "heating",
            "compaction_temp_c": temp_heat,
            "hydraulic_pressure_mpa": pressure_heat,
            "compressed_height_mm": height_heat,
            "heater_current_a": current_heat,
        }
    )

    # carry last heating temp into compression phase
    temp_at_compression = temp_heat[-1]

    # ===========================================
    # phase 2 - compression
    # ===========================================
    n_comp = int(compression_duration * SAMPLE_HZ)
    frac = np.arange(n_comp) / max(n_comp - 1, 1)
    t_comp = heat_df["elapsed_s"].iloc[-1] + 1 + np.arange(n_comp) / SAMPLE_HZ

    pressure_comp = peak_pressure * (1 - (1 - frac) ** 3) + rng.normal(
        0, peak_pressure * 0.03, size=n_comp
    )  # pressure rises to peak and then stabilizes
    height_comp = (
        raw_height
        - (raw_height - final_height) * (1 - (1 - frac) ** 2)  #
        + rng.normal(0, 0.3, size=n_comp)
    )
    temp_comp = temp_at_compression - 3.5 * frac + rng.normal(0, 0.3, size=n_comp)
    current_comp = heater_current_nominal * np.clip(
        1 - 1.4 * frac, 0, None
    ) + rng.normal(0, 0.1, size=n_comp)

    comp_df = pd.DataFrame(
        {
            "elapsed_s": t_comp,
            "phase": "compression",
            "compaction_temp_c": temp_comp,
            "hydraulic_pressure_mpa": pressure_comp,
            "compressed_height_mm": height_comp,
            "heater_current_a": current_comp,
        }
    )

    temp_at_cool_start = temp_comp[-1]

    # ===========================================
    # phase 3 - cooling
    # ===========================================
    n_cool = int(cooling_duration * SAMPLE_HZ)
    t_cool_rel = np.arange(n_cool) / SAMPLE_HZ
    t_cool = comp_df["elapsed_s"].iloc[-1] + 1 + t_cool_rel

    temp_cool = (
        AMBIENT_TEMP_C
        + (temp_at_cool_start - AMBIENT_TEMP_C)
        * np.exp(-t_cool_rel / cooling_tau)  # Newton's Law of Cooling
        + rng.normal(0, 0.3, size=n_cool)
    )
    pressure_cool = np.clip(rng.normal(0.005, 0.004, size=n_cool), 0, None)  # released
    height_cool = final_height + rng.normal(
        0, 0.15, size=n_cool
    )  # settled, minor noise
    current_cool = np.clip(rng.normal(0.1, 0.08, size=n_cool), 0, None)  # heater off

    cool_df = pd.DataFrame(
        {
            "elapsed_s": t_cool,
            "phase": "cooling",
            "compaction_temp_c": temp_cool,
            "hydraulic_pressure_mpa": pressure_cool,
            "compressed_height_mm": height_cool,
            "heater_current_a": current_cool,
        }
    )

    # ===========================================
    # combine all phases into a single DataFrame
    # ===========================================
    batch_df = pd.concat([heat_df, comp_df, cool_df], ignore_index=True)
    batch_df.insert(0, "batch_id", batch_id)

    # tidy up the data
    batch_df["elapsed_s"] = batch_df["elapsed_s"].round(1)
    batch_df["compaction_temp_c"] = batch_df["compaction_temp_c"].round(2)
    batch_df["hydraulic_pressure_mpa"] = (
        batch_df["hydraulic_pressure_mpa"].clip(lower=0).round(4)
    )
    batch_df["compressed_height_mm"] = batch_df["compressed_height_mm"].round(2)
    batch_df["heater_current_a"] = batch_df["heater_current_a"].clip(lower=0).round(3)

    return batch_df


def main():
    parser = argparse.ArgumentParser(
        description="Generate mock telemetry data for testing."
    )
    parser.add_argument(
        "--out",
        type=str,
        default=DEFAULT_OUT,
        help=f"Output CSV file path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--batches", type=int, default=5, help="Number of batches to simulate"
    )

    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    batch_ids = [f"MOCK-{b:04d}" for b in range(1, args.batches + 1)]
    all_batch = pd.concat(
        [simulate_batch(batch_id, rng) for batch_id in batch_ids], ignore_index=True
    )

    all_batch.to_csv(out_path, index=False)
    print(f"Mock telemetry data generated and saved to {out_path}")


if __name__ == "__main__":
    main()
