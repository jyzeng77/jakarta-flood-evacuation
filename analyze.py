import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent


def percent_change(start, end):
    return round(float((end - start) / start * 100), 1)


def main():
    daily = pd.read_csv(
        ROOT / "data/january_2020_daily.csv",
        parse_dates=["date"],
        index_col="date",
        dtype={
            "reported_evacuees": "int64",
            "reported_sites": "int64",
            "flooded_rw": "Int64",
        },
    ).sort_index()
    months = pd.read_csv(
        ROOT / "data/flood_months_2014_2020.csv",
        index_col="month",
        dtype={"affected_rw": "int64", "peak_reported_evacuees": "int64"},
    )

    expected_dates = pd.date_range("2020-01-01", "2020-01-07", freq="D")
    if not daily.index.equals(expected_dates) or months.index.has_duplicates:
        raise ValueError("Expected one record per day in the first week and per listed month.")
    if (daily["reported_sites"] <= 0).any() or (daily < 0).any().any():
        raise ValueError("Daily counts must be nonnegative, with at least one site per day.")
    if (months <= 0).any().any():
        raise ValueError("Historical counts must be positive.")

    peak_date = daily["reported_evacuees"].idxmax()
    peak = daily.loc[peak_date]
    first = daily.iloc[0]
    final = daily.iloc[-1]
    january = months.loc["2020-01"]
    february = months.loc["2020-02"]
    if peak["reported_evacuees"] != january["peak_reported_evacuees"]:
        raise ValueError("The daily and monthly sources disagree on January's peak count.")

    daily["evacuees_per_reported_site"] = (
        daily["reported_evacuees"] / daily["reported_sites"]
    )
    load_date = daily["evacuees_per_reported_site"].idxmax()
    # Spearman correlation is the Pearson correlation of the ranks.
    ranks = months.rank().to_numpy()
    rank_correlation = np.corrcoef(ranks, rowvar=False)[0, 1]

    summary = {
        "peak_evacuees_date": peak_date.date().isoformat(),
        "peak_reported_evacuees": int(peak["reported_evacuees"]),
        "reported_sites_at_peak": int(peak["reported_sites"]),
        "first_day_to_peak_evacuees_pct_change": percent_change(
            first["reported_evacuees"], peak["reported_evacuees"]
        ),
        "first_day_to_peak_sites_pct_change": percent_change(
            first["reported_sites"], peak["reported_sites"]
        ),
        "peak_to_next_day_evacuees_pct_change": percent_change(
            peak["reported_evacuees"],
            daily.loc[peak_date + pd.Timedelta(days=1), "reported_evacuees"],
        ),
        "highest_evacuees_per_reported_site_date": load_date.date().isoformat(),
        "highest_evacuees_per_reported_site": round(
            float(daily.loc[load_date, "evacuees_per_reported_site"]), 1
        ),
        "last_day_flooded_rw": int(final["flooded_rw"]),
        "last_day_reported_evacuees": int(final["reported_evacuees"]),
        "last_day_reported_sites": int(final["reported_sites"]),
        "historical_months": len(months),
        "affected_rw_vs_peak_evacuees_spearman": round(float(rank_correlation), 3),
        "jan_to_feb_affected_rw_pct_change": percent_change(
            january["affected_rw"], february["affected_rw"]
        ),
        "jan_to_feb_peak_evacuees_pct_change": percent_change(
            january["peak_reported_evacuees"], february["peak_reported_evacuees"]
        ),
    }

    output = ROOT / "results"
    output.mkdir(exist_ok=True)
    daily.to_csv(output / "daily_metrics.csv", float_format="%.2f", date_format="%Y-%m-%d")
    report = json.dumps(summary, indent=2, allow_nan=False)
    (output / "summary.json").write_text(report + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
