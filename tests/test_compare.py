"""The data file is well formed and compare.py reproduces the README's tables."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import compare  # noqa: E402

DATA = compare.load()
RULES = set(DATA["video_rules"])


def cost(provider, *args):
    row = next(r for r in compare.compare(DATA, *args) if r["provider"].startswith(provider))
    return row["usd"]


def test_every_provider_has_a_source_and_known_rule():
    names = [p["name"] for p in DATA["providers"]]
    assert len(names) == len(set(names)) == 9
    for provider in DATA["providers"]:
        assert provider["url"].startswith("https://")
        assert provider["video_rule"] in RULES
        for model, prices in provider["models"].items():
            assert model in {"seedance-2.0", "seedance-2.0-fast", "seedance-2.0-mini"}
            assert all(rate > 0 for rate in prices["no_video"].values())
            if model != "seedance-2.0":
                assert set(prices["no_video"]) <= {"480p", "720p"}, (provider["name"], model)


@pytest.mark.parametrize("provider,args,usd", [
    ("ArgoLink", ("seedance-2.0", "720p", 5), 0.55),
    ("BytePlus", ("seedance-2.0", "720p", 5), 0.756),
    ("Replicate", ("seedance-2.0", "720p", 5), 0.90),
    ("fal", ("seedance-2.0", "720p", 5), 1.512),
    ("BytePlus", ("seedance-2.0", "1080p", 5), 1.8711),
    ("ArgoLink", ("seedance-2.0", "4k", 5), 2.90),
    ("OpenRouter", ("seedance-2.0-fast", "720p", 5), 0.4536),
    ("ArgoLink", ("seedance-2.0-mini", "480p", 5), 0.13),
])
def test_prices_without_video_input(provider, args, usd):
    assert cost(provider, *args) == pytest.approx(usd, abs=1e-4)


@pytest.mark.parametrize("provider,usd", [
    ("ArgoLink", 1.65),      # (10 + 5) x 0.11
    ("BytePlus", 1.3932),    # (10 + 5) x 0.09288
    ("Replicate", 2.20),     # 10 x 0.22: input length not billed
    ("fal", 2.721),          # (10 + 5) x 0.1814
    ("WaveSpeedAI", 2.25),   # (10 + 5) x 0.15
    ("Kie.ai", 1.875),       # (10 + 5) x 0.125
    ("PiAPI", None),         # video-input billing not published on the page read
])
def test_prices_with_a_reference_video(provider, usd):
    result = cost(provider, "seedance-2.0", "720p", 10, 5.0)
    assert result == (None if usd is None else pytest.approx(usd, abs=1e-3))


def test_reference_seconds_round_by_each_providers_rule():
    assert cost("ArgoLink", "seedance-2.0", "720p", 5, 2.4) == pytest.approx(0.77)        # floor: 7 s
    assert cost("WaveSpeedAI", "seedance-2.0", "720p", 5, 1.5) == pytest.approx(1.05)     # min 2 s: 7 s
    assert cost("WaveSpeedAI", "seedance-2.0", "720p", 5, 2.4) == pytest.approx(1.2)      # ceil: 8 s


def test_unoffered_tiers_are_not_priced():
    assert cost("PiAPI", "seedance-2.0", "4k", 5) is None
    assert cost("Kie.ai", "seedance-2.0-mini", "480p", 5) is None
    assert cost("ArgoLink", "seedance-2.0-mini", "1080p", 5) is None


def test_cheapest_first_and_json_output(capsys):
    rows = compare.compare(DATA, "seedance-2.0", "720p", 5)
    priced = [r["usd"] for r in rows if r["usd"] is not None]
    assert priced == sorted(priced)
    assert compare.main(["--json", "--model", "seedance-2.0-mini", "--resolution", "480p"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["checked"] == "2026-10-07" and out["rows"][0]["provider"] == "ArgoLink"
