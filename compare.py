#!/usr/bin/env python3
"""Price one Seedance 2.0 job at every provider in data/, cheapest first.

    python compare.py                                   # 5 s at 720p, seedance-2.0, no video input
    python compare.py --model seedance-2.0-mini --resolution 480p --seconds 8
    python compare.py --resolution 720p --seconds 10 --reference-video 5
    python compare.py --json

Standard library only. Rates are the ones each provider published on the date in the
data file; a provider that does not offer the tier, or does not publish how video input
is billed, is listed as n/a.
"""
import argparse
import json
import math
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "seedance-2.0-prices-2026-10-07.json"


def load(path=DATA):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def job_cost(provider, model, resolution, seconds, reference_video=0.0):
    """USD for one job, or None when the provider page gives no price for it."""
    prices = provider["models"].get(model)
    if not prices or resolution not in prices["no_video"]:
        return None
    if reference_video <= 0:
        return prices["no_video"][resolution] * seconds
    rule = provider["video_rule"]
    if rule == "same_rate_plus_reference":
        return prices["no_video"][resolution] * (seconds + math.floor(reference_video + 1e-9))
    rate = prices.get("with_video", {}).get(resolution)
    if rate is None:
        return None
    if rule == "output_only":
        return rate * seconds
    if rule == "input_plus_output":
        billed_input = reference_video
        if provider["name"] == "WaveSpeedAI":  # at least 2 s, rounded up to a whole second
            billed_input = math.ceil(max(2.0, reference_video) - 1e-9)
        return rate * (seconds + billed_input)
    return None


def compare(data, model="seedance-2.0", resolution="720p", seconds=5, reference_video=0.0):
    rows = []
    for provider in data["providers"]:
        cost = job_cost(provider, model, resolution, seconds, reference_video)
        computed = resolution in provider["models"].get(model, {}).get("computed", [])
        rows.append({"provider": provider["name"], "usd": None if cost is None else round(cost, 4),
                     "computed": computed, "billing": provider["billing"], "url": provider["url"]})
    return sorted(rows, key=lambda row: (row["usd"] is None, row["usd"] or 0))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="seedance-2.0", choices=["seedance-2.0", "seedance-2.0-fast", "seedance-2.0-mini"])
    parser.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p", "4k"])
    parser.add_argument("--seconds", type=int, default=5, help="output length, 4-15")
    parser.add_argument("--reference-video", type=float, default=0.0, help="total seconds of reference video")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not 4 <= args.seconds <= 15:
        parser.error("Seedance 2.0 renders 4-15 seconds")

    data = load()
    rows = compare(data, args.model, args.resolution, args.seconds, args.reference_video)
    if args.json:
        print(json.dumps({"checked": data["checked"], "model": args.model, "resolution": args.resolution,
                          "seconds": args.seconds, "reference_video": args.reference_video, "rows": rows}, indent=2))
        return 0
    scenario = f"{args.model}, {args.seconds} s at {args.resolution}"
    if args.reference_video:
        scenario += f" + {args.reference_video:g} s of reference video"
    print(f"{scenario} (prices published {data['checked']})")
    for row in rows:
        price = "n/a" if row["usd"] is None else f"${row['usd']:.3f}"
        print(f"  {row['provider']:<30} {price:>8}{' *' if row['computed'] else ''}")
    if any(row["computed"] for row in rows):
        print("  * computed from the provider's token price")
    return 0


if __name__ == "__main__":
    sys.exit(main())
