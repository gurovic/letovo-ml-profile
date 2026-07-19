#!/usr/bin/env python3
"""Build teaching listings.csv from Inside Airbnb Porto (or synthetic fallback).

Primary path (default):
  Download detailed listings.csv.gz for Porto (2024-12-14), cache under data/_cache/,
  filter price outliers, map columns, sample N rows with seed 42.

Fallback:
  If download fails and no cache exists, generate synthetic rows with a clear
  linear signal: price ≈ BASE + COEF * accommodates + review/room offsets + noise.

Usage:
  python generate_listings.py              # try real, else synthetic
  python generate_listings.py --synthetic  # force synthetic
  python generate_listings.py --from-cache # only use cached gz (no network)
"""

from __future__ import annotations

import argparse
import csv
import gzip
import random
import urllib.error
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
CACHE_DIR = DATA_DIR / "_cache"
OUT_CSV = DATA_DIR / "listings.csv"

# Inside Airbnb — Porto, Norte, Portugal (visualisations sibling: detailed data/)
CITY_SLUG = "portugal/norte/porto"
SNAPSHOT = "2024-12-14"
SOURCE_URL = (
    f"https://data.insideairbnb.com/{CITY_SLUG}/{SNAPSHOT}/data/listings.csv.gz"
)
CACHE_GZ = CACHE_DIR / f"porto_{SNAPSHOT}_listings.csv.gz"

N_SAMPLE = 300
SEED = 42

# Price filter (nightly USD/EUR as published); drop empty / extreme outliers
PRICE_MIN = 20.0
PRICE_MAX = 350.0

# Map neighbourhood_cleansed → short English teaching labels
NEIGHBOURHOOD_MAP: dict[str, str] = {
    "Cedofeita, Ildefonso, Sé, Miragaia, Nicolau, Vitória": "center",
    "Bonfim": "old_town",
    "Santa Marinha e São Pedro da Afurada": "riverside",
    "Lordelo do Ouro e Massarelos": "riverside",
    "Aldoar, Foz do Douro e Nevogilde": "riverside",
    "Campanhã": "east",
    "Paranhos": "university",
    "Matosinhos e Leça da Palmeira": "beach",
    "Ramalde": "suburb",
    "Canidelo": "suburb",
    "Mafamude e Vilar do Paraíso": "suburb",
}

ROOM_MAP = {
    "Entire home/apt": "entire",
    "Private room": "private",
    "Shared room": "shared",
    "Hotel room": "private",
}

FIELDNAMES = [
    "listing_id",
    "accommodates",
    "price",
    "number_of_reviews",
    "neighbourhood",
    "room_type",
    "bedrooms",
]

# Synthetic model (fallback) — same spirit as old generate_trips.py
SYN_BASE = 35.0
SYN_COEF_ACC = 18.0
SYN_ROOM_OFFSET = {"entire": 25.0, "private": 0.0, "shared": -15.0}
SYN_NEIGH = ("center", "riverside", "old_town", "beach", "suburb")
SYN_NEIGH_OFFSET = {
    "center": 20.0,
    "riverside": 12.0,
    "old_town": 15.0,
    "beach": 10.0,
    "suburb": 0.0,
}


def parse_price(raw: str) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip().replace("$", "").replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def download_to_cache() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CACHE_GZ.exists() and CACHE_GZ.stat().st_size > 0:
        print(f"using cache: {CACHE_GZ}")
        return CACHE_GZ
    print(f"downloading {SOURCE_URL} ...")
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "letovo-ml-profile-teaching-dataset/1.0"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    CACHE_GZ.write_bytes(data)
    print(f"cached {CACHE_GZ} ({len(data)} bytes)")
    return CACHE_GZ


def load_from_gz(gz_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with gzip.open(gz_path, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            nb_src = (raw.get("neighbourhood_cleansed") or "").strip()
            if nb_src not in NEIGHBOURHOOD_MAP:
                continue
            room_src = (raw.get("room_type") or "").strip()
            if room_src not in ROOM_MAP:
                continue
            price = parse_price(raw.get("price") or "")
            if price is None or price < PRICE_MIN or price > PRICE_MAX:
                continue
            acc_s = (raw.get("accommodates") or "").strip()
            if not acc_s.isdigit():
                continue
            accommodates = int(acc_s)
            if accommodates < 1 or accommodates > 12:
                continue
            rev_s = (raw.get("number_of_reviews") or "0").strip()
            try:
                n_reviews = int(float(rev_s))
            except ValueError:
                n_reviews = 0
            bed_s = (raw.get("bedrooms") or "").strip()
            if bed_s == "" or bed_s.lower() == "nan":
                # reasonable default from accommodates for teaching completeness
                bedrooms = max(1, min(accommodates // 2, 6))
            else:
                try:
                    bedrooms = int(float(bed_s))
                except ValueError:
                    continue
                if bedrooms < 0:
                    continue
                bedrooms = max(0, min(bedrooms, 8))

            rows.append(
                {
                    "listing_id": f"L{int(raw['id']) % 100000:04d}",
                    "accommodates": accommodates,
                    "price": round(price, 1),
                    "number_of_reviews": max(0, n_reviews),
                    "neighbourhood": NEIGHBOURHOOD_MAP[nb_src],
                    "room_type": ROOM_MAP[room_src],
                    "bedrooms": bedrooms,
                    "_src_id": raw["id"],
                }
            )
    return rows


def sample_rows(rows: list[dict[str, object]], n: int, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    # unique by source id before sampling
    by_id: dict[str, dict[str, object]] = {}
    for r in rows:
        by_id[str(r["_src_id"])] = r
    pool = list(by_id.values())
    if len(pool) < n:
        raise RuntimeError(f"only {len(pool)} clean rows after filter; need {n}")
    chosen = rng.sample(pool, n)
    # stable teaching ids L0001.. after shuffle order from sample
    out: list[dict[str, object]] = []
    for i, r in enumerate(sorted(chosen, key=lambda x: str(x["_src_id"])), start=1):
        out.append(
            {
                "listing_id": f"L{i:04d}",
                "accommodates": r["accommodates"],
                "price": r["price"],
                "number_of_reviews": r["number_of_reviews"],
                "neighbourhood": r["neighbourhood"],
                "room_type": r["room_type"],
                "bedrooms": r["bedrooms"],
            }
        )
    # re-shuffle with seed so file order is reproducible but not sorted by id alone
    rng2 = random.Random(seed)
    rng2.shuffle(out)
    for i, r in enumerate(out, start=1):
        r["listing_id"] = f"L{i:04d}"
    return out


def generate_synthetic(n: int = N_SAMPLE, seed: int = SEED) -> list[dict[str, object]]:
    rng = random.Random(seed)
    rooms = ("entire", "private", "shared")
    rows: list[dict[str, object]] = []
    for i in range(1, n + 1):
        accommodates = rng.randint(1, 8)
        bedrooms = max(1, min((accommodates + 1) // 2, 5))
        n_reviews = rng.randint(0, 200)
        neighbourhood = rng.choice(SYN_NEIGH)
        room_type = rng.choices(rooms, weights=[0.7, 0.25, 0.05], k=1)[0]
        review_boost = min(n_reviews, 100) * 0.08
        noise = rng.gauss(0, 12.0)
        price = (
            SYN_BASE
            + SYN_COEF_ACC * accommodates
            + SYN_ROOM_OFFSET[room_type]
            + SYN_NEIGH_OFFSET[neighbourhood]
            + review_boost
            + noise
        )
        price = max(PRICE_MIN, round(price, 1))
        rows.append(
            {
                "listing_id": f"L{i:04d}",
                "accommodates": accommodates,
                "price": price,
                "number_of_reviews": n_reviews,
                "neighbourhood": neighbourhood,
                "room_type": room_type,
                "bedrooms": bedrooms,
            }
        )
    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def build_real(*, allow_download: bool) -> list[dict[str, object]]:
    if allow_download:
        gz = download_to_cache()
    else:
        if not CACHE_GZ.exists():
            raise FileNotFoundError(f"no cache at {CACHE_GZ}")
        gz = CACHE_GZ
        print(f"using cache (no download): {gz}")
    pool = load_from_gz(gz)
    print(f"clean pool size: {len(pool)}")
    return sample_rows(pool, N_SAMPLE, SEED)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="force synthetic generation (no download)",
    )
    parser.add_argument(
        "--from-cache",
        action="store_true",
        help="use cached gz only; no network",
    )
    args = parser.parse_args()

    source = "synthetic"
    if args.synthetic:
        rows = generate_synthetic()
    else:
        try:
            rows = build_real(allow_download=not args.from_cache)
            source = "inside_airbnb_porto"
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError) as e:
            print(f"real download/build failed: {e!r}")
            print("falling back to synthetic (seed=42)")
            rows = generate_synthetic()
            source = "synthetic"

    write_csv(rows, OUT_CSV)
    # quick sanity: correlation-ish print
    acc = [int(r["accommodates"]) for r in rows]
    price = [float(r["price"]) for r in rows]
    mean_a = sum(acc) / len(acc)
    mean_p = sum(price) / len(price)
    cov = sum((a - mean_a) * (p - mean_p) for a, p in zip(acc, price)) / len(acc)
    var_a = sum((a - mean_a) ** 2 for a in acc) / len(acc)
    corr = cov / (var_a**0.5 * (sum((p - mean_p) ** 2 for p in price) / len(price)) ** 0.5)
    print(f"source={source}  corr(accommodates, price)≈{corr:.3f}")


if __name__ == "__main__":
    main()
