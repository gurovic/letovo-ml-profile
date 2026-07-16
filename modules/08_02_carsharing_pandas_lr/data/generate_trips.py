#!/usr/bin/env python3
"""Generate synthetic carsharing trips CSV (reproducible)."""

from __future__ import annotations

import csv
import random
from pathlib import Path

ZONES = ("center", "suburb", "airport")
VEHICLES = ("economy", "comfort")

# duration_min ≈ BASE + COEF_DIST * distance + zone/hour noise
BASE = 5.0
COEF_DIST = 2.4
ZONE_OFFSET = {"center": 3.0, "suburb": 0.0, "airport": 8.0}
HOUR_PEAK = {7, 8, 9, 17, 18, 19}


def main() -> None:
    random.seed(42)
    rows: list[dict[str, object]] = []
    for i in range(1, 201):
        distance = round(random.uniform(1.0, 24.0), 1)
        hour = random.randint(0, 23)
        zone = random.choice(ZONES)
        vehicle = random.choice(VEHICLES)
        peak = 4.0 if hour in HOUR_PEAK else 0.0
        comfort = 2.0 if vehicle == "comfort" else 0.0
        noise = random.gauss(0, 3.0)
        duration = (
            BASE
            + COEF_DIST * distance
            + ZONE_OFFSET[zone]
            + peak
            + comfort
            + noise
        )
        duration = max(8.0, round(duration, 1))
        rows.append(
            {
                "trip_id": f"T{i:04d}",
                "distance_km": distance,
                "duration_min": duration,
                "hour": hour,
                "zone": zone,
                "vehicle_type": vehicle,
            }
        )

    out = Path(__file__).resolve().parent / "trips.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "trip_id",
                "distance_km",
                "duration_min",
                "hour",
                "zone",
                "vehicle_type",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
