# Seedance 2.0 API Providers Compared (October 2026)

Nine places to call ByteDance's Seedance 2.0 by API, priced on the same jobs from each provider's own page on 2026-10-07, plus the billing rules that change the ranking once you attach a reference video or need more than a few jobs at once.

> **Disclosure:** this comparison is maintained with [ArgoLink](https://argolink.io/gh-seedance-2-0-provider-comparison), one of the nine providers. Every figure links to the provider's page, the raw numbers are in [`data/`](./data/seedance-2.0-prices-2026-10-07.json), and [`compare.py`](./compare.py) recomputes any job, so you can check all of it.

<sub>Last checked: 2026-10-07. Prices change often; re-run the numbers against the linked pages before you commit a budget.</sub>

**Contents:** [Providers](#the-nine-providers) · [5-second clip](#one-5-second-720p-clip) · [Resolutions](#480p-1080p-and-4k) · [Trap 1: per-second units](#trap-1-per-second-does-not-mean-the-same-thing) · [Trap 2: reference video](#trap-2-a-reference-video-reorders-the-table) · [Trap 3: fees](#trap-3-costs-outside-the-rate) · [Trap 4: discounts](#trap-4-discounts-with-an-end-date) · [Trap 5: concurrency](#trap-5-few-providers-publish-concurrency) · [Trap 6: faces](#trap-6-real-faces) · [Which to pick](#which-provider-for-which-job) · [Recompute](#recompute-for-your-own-job)

## The nine providers

| Provider | Billed by | 2.0 | Fast | Mini | 4K | Video input |
|---|---|:-:|:-:|:-:|:-:|---|
| [BytePlus ModelArk](https://docs.byteplus.com/en/docs/modelark/model-pricing) (ByteDance, official) | tokens | ✓ | ✓ | ✓ | ✓ | lower token rate on input + output seconds |
| [OpenRouter](https://openrouter.ai/bytedance/seedance-2.0) | tokens at BytePlus's rates | ✓ | ✓ | ✓ | ✓ | as BytePlus |
| [ArgoLink](https://argolink.io/en/models/seedance-2.0) | output seconds | ✓ | ✓ | ✓ | ✓ | reference seconds added at the normal rate |
| [Replicate](https://replicate.com/bytedance/seedance-2.0) | output seconds | ✓ | ✓ | ✓ | ✓ | higher rate, output seconds only |
| [PiAPI](https://piapi.ai/seedance-2-0) | output seconds | ✓ | ✓ | ✓ | — | not stated on the page |
| [Kie.ai](https://kie.ai/seedance-2-0) | credits per second | ✓ | ✓ | — | ✓ | lower rate on input + output seconds |
| [WaveSpeedAI](https://wavespeed.ai/models/bytedance/seedance-2.0/text-to-video) | output seconds | ✓ | ✓ | ✓ | ✓ | lower rate on input + output seconds |
| [Atlas Cloud](https://www.atlascloud.ai/models/bytedance/seedance-2.0/text-to-video) | tokens | ✓ | — | — | — | lower token rate on input + output seconds |
| [fal](https://fal.ai/models/bytedance/seedance-2.0/text-to-video) | tokens | ✓ | ✓ | ✓ | ✓ | 0.6× rate on input + output seconds |

"—" means the variant or rule was not found on the pages read. At ByteDance, Fast and Mini are 480p/720p models and only the full 2.0 model renders 1080p and 4K; WaveSpeedAI also lists 1080p and 4K prices for its Fast and Mini endpoints, which are left out here.

## One 5-second 720p clip

No video input, 16:9. Sorted by the Seedance 2.0 column.

| Provider | Seedance 2.0 | 2.0 Fast | 2.0 Mini |
|---|---:|---:|---:|
| ArgoLink | **$0.55** | $0.455 | **$0.285** |
| BytePlus ModelArk | $0.76 | $0.605 | $0.378 |
| OpenRouter | $0.76 | **$0.454** | $0.378 |
| Replicate | $0.90 | $0.75 | $0.45 |
| PiAPI | $1.00 | $0.48 | $0.42 |
| Kie.ai | $1.03 | $0.62 | — |
| WaveSpeedAI | $1.20 | $1.00 | $0.60 |
| Atlas Cloud | $1.21 | — | — |
| fal | $1.51 | $1.21 | $0.77 |

<sub>Rate × 5 s at the rates in the [data file](./data/seedance-2.0-prices-2026-10-07.json). OpenRouter adds 5.5% when you buy credits by card, which puts its Fast clip at about $0.479. BytePlus figures come from its token prices and match its own 5-second examples ($0.76, $0.60 and $0.38).</sub>

## 480p, 1080p and 4K

Seedance 2.0, 5 seconds, no video input:

| Provider | 480p | 1080p | 4K |
|---|---:|---:|---:|
| ArgoLink | **$0.265** | **$1.40** | **$2.90** |
| OpenRouter | $0.336 | $1.87 | $3.89 |
| BytePlus ModelArk | $0.35 | $1.87 | $3.89 |
| Replicate | $0.40 | $2.25 | $5.00 |
| Kie.ai | $0.475 | $2.55 | $5.20 |
| PiAPI | $0.50 | $2.50 | — |
| WaveSpeedAI | $0.60 | $3.00 | $6.00 |
| fal | ≈ $0.70 | $3.41 | ≈ $7.78 |

<sub>≈: fal states a token price, not a per-second rate, at 480p and 4K; computed with BytePlus's 16:9 output sizes (864×496 and 3840×2160). OpenRouter's 480p is lower than BytePlus's because its pages price 480p at 854×480. Atlas Cloud's page states only the 720p rate.</sub>

## Trap 1: "per second" does not mean the same thing

| Provider | What one second buys | Rule |
|---|---|---|
| BytePlus, OpenRouter, Atlas Cloud, fal | tokens = (input video s + output s) × width × height × 24 / 1024 | price per token, so the rate follows the exact pixel size |
| ArgoLink | output seconds; reference videos add their length | same rate for both, fraction of a second dropped |
| Replicate | output seconds only | a separate, higher rate when any video is attached |
| Kie.ai, WaveSpeedAI | output seconds, or input + output seconds with video | a separate, lower rate when a video is attached |
| PiAPI | output seconds | video-input billing not on the page read |

Two consequences. At token-priced providers the aspect ratio moves the price a little, because the frame size differs: at 480p, BytePlus renders 1:1 as 640×640 against 864×496 for 16:9, about 4% fewer tokens. And a provider that looks dearer per second can be cheaper for your job, as the next section shows.

## Trap 2: a reference video reorders the table

Seedance 2.0, 10 s at 720p with one 5-second reference video:

| Provider | Cost | Why |
|---|---:|---|
| BytePlus ModelArk | $1.39 | 15 s × $0.0929, the video-input token rate ($4.3 instead of $7.0 per million) |
| OpenRouter | $1.39 | same token rates |
| ArgoLink | $1.65 | 15 s × $0.11, reference seconds at the normal rate |
| Kie.ai | $1.88 | 15 s × $0.125 |
| Replicate | $2.20 | 10 s × $0.22; the reference length is not billed |
| Atlas Cloud | $2.23 | 15 s × $0.1486 |
| WaveSpeedAI | $2.25 | 15 s × $0.15 |
| fal | $2.72 | 15 s × $0.1814 (0.6 × its normal rate) |
| PiAPI | — | not stated |

Without video, ArgoLink is about 27% below BytePlus at 720p; with a reference video, BytePlus's token rate is about 16% below ArgoLink's. BytePlus also applies a minimum token charge when the input includes video, so very short references cost a little more than the formula says. If most of your jobs carry long reference videos, price them with `compare.py` before choosing.

## Trap 3: costs outside the rate

| Provider | What else to budget for |
|---|---|
| BytePlus ModelArk | Seedance 2.0 and 2.5 activate only with a balance above USD 30, a USD 30+ savings plan, or a resource pack |
| OpenRouter | 5.5% fee on card credit purchases (5% for crypto) |
| PiAPI | watermark removal priced separately; subscription plans billed apart from usage; new accounts get $0.50 of free credit |
| Kie.ai | prices marked beta; high-tier top-ups add 10% credit |
| ArgoLink | none found beyond the per-second rate; failed and expired jobs are not billed |

## Trap 4: discounts with an end date

- BytePlus ran enterprise-only discounts on 2.0 Fast (25% off) and 2.0 Mini (60% off) from 7 August to 7 October 2026, 14:00 UTC+8. Individual accounts pay list price, and from today so do enterprises.
- OpenRouter's Fast price on 2026-10-07 was $4.20 per million tokens, which is BytePlus's $5.60 list price less 25%; its 2.0 and Mini prices equal BytePlus's list prices.
- Atlas Cloud lists Seedance 2.0 variants with struck-through "from" prices and promotional discounts of 20–80%; the comparison uses the 720p rate its model page states.

Dated data is the only defence: the file in this repo carries the check date, and every row links to the page it came from.

## Trap 5: few providers publish concurrency

| Provider | Published limit |
|---|---|
| BytePlus ModelArk | 3 jobs at once for individual accounts, 10 for enterprise (4K: 1); 180 / 600 requests a minute |
| fal | new accounts 2 concurrent requests, rising with the last four weeks' spend to 40 on self-serve |
| PiAPI | higher concurrency on its USD 100/month Enterprise plan (number not stated) |
| Atlas Cloud | its page title advertises "Unlimited Concurrency" |
| ArgoLink, OpenRouter, Replicate, Kie.ai, WaveSpeedAI | no Seedance 2.0 limit on the pages read |

If your product queues many users at once, ask the provider for the number in writing before you build on it.

## Trap 6: real faces

| Provider | Faces in reference images or video |
|---|---|
| BytePlus ModelArk | not accepted directly; preset digital characters, trusted outputs of its own models, or an authorised real-person asset workflow |
| PiAPI | `-less-restriction` variants accept face references after review, at about 10% more per second ($0.22 instead of $0.20 at 720p) |
| Kie.ai | its Seedance 2.0 page is titled "with Realistic Human Support" |
| others | not stated on the pages read; content review can still refuse a face |

## Which provider for which job

| If this matters most | Look first at | Because (2026-10-07) |
|---|---|---|
| lowest price per clip without reference video, any resolution | ArgoLink | lowest 2.0 and Mini rates in every table above; on Fast, OpenRouter is a little lower before its 5.5% card fee |
| long reference videos | BytePlus or OpenRouter | video-input token rate is 16% below ArgoLink's per-second rate |
| buying from ByteDance directly | BytePlus ModelArk | official API, published rate limits, USD 30 activation |
| the simplest invoice line | Replicate or PiAPI | flat per-output-second prices |
| face references | PiAPI `-less-restriction`, or BytePlus's authorised-asset workflow | the only published routes |
| one account for many model vendors | OpenRouter | its pricing passes BytePlus's token rates through |

## Recompute for your own job

```bash
python compare.py --model seedance-2.0 --resolution 1080p --seconds 8
python compare.py --model seedance-2.0-mini --resolution 480p --seconds 12
python compare.py --resolution 720p --seconds 10 --reference-video 5
python compare.py --json > quote.json
```

```text
seedance-2.0, 5 s at 1080p (prices published 2026-10-07)
  ArgoLink                         $1.400
  BytePlus ModelArk (official)     $1.871 *
  OpenRouter                       $1.871 *
  Replicate                        $2.250
  …
```

No dependencies. Edit [`data/seedance-2.0-prices-2026-10-07.json`](./data/seedance-2.0-prices-2026-10-07.json) to add a provider or update a rate; keep the date in the file name honest.

## How the numbers were collected

- Each provider's Seedance 2.0 page (and its Fast and Mini pages where they exist) was opened on 2026-10-07 without signing in; rates are copied as published, in USD.
- Token-priced providers were converted to a per-second figure for a 16:9, 24 fps clip using BytePlus's output sizes; where the provider itself states a per-second figure, that figure is used.
- Only the standard tier of each variant is compared: no `-less-restriction`, VIP or draft variants, and no subscriptions.
- A blank means the tier or rule was not found on the page read, not that the provider lacks it.

## FAQ

**Which Seedance 2.0 API is cheapest?**
For Seedance 2.0 and 2.0 Mini without a reference video, ArgoLink was cheapest at every resolution on 2026-10-07 (from $0.053/s at 480p, $0.026/s for Mini). On 2.0 Fast, OpenRouter's rate is a little lower before its 5.5% card fee. With long reference videos, BytePlus and OpenRouter come out ahead.

**Is the official BytePlus API the cheapest?**
Not for plain clips: ArgoLink's rates are 25–27% below BytePlus's list rates from 480p to 4K. For jobs dominated by reference video it is, thanks to its video-input token rate.

**Why do 480p prices differ between BytePlus and OpenRouter when the token rate is the same?**
BytePlus's 16:9 480p frame is 864×496; OpenRouter's pages price 480p at 854×480. The token formula follows the pixels.

**Does generating audio cost extra?**
None of the nine charges extra for the soundtrack: fal states the price is the same with or without audio, and the others publish one rate per resolution.

**Why is fal so much more expensive?**
Its token prices are twice BytePlus's list prices for all three variants ($0.014 vs $0.007 per 1,000 tokens for 2.0).

## License

MIT
