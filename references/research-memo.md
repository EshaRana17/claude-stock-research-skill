# Research memo: template and checklist

Use this file for Workflow 1. Fill every section. Where data is missing, write "not available" and name the source that would supply it. Never estimate a figure without labeling it as an estimate and showing the inputs.

## Contents

- Source priority
- Memo template (stocks)
- ETF variant
- Valuation guidance
- Pre-send checklist

## Source priority

1. Files or data the user provides (state the file name).
2. Primary sources: SEC EDGAR filings (10-K annual, 10-Q quarterly, 8-K events, DEF 14A proxy, Form 4 insider trades), company investor relations pages, earnings releases and call transcripts.
3. Exchange and index provider pages; for ETFs, the issuer's fund page and prospectus.
4. Reputable financial news and data sites found through web search.

Rules:
- Prefer the most recent filing. Note the fiscal period (for example "FY2025" or "Q2 FY2026") because fiscal years differ from calendar years.
- If two sources disagree, show both and say which you used and why.
- Quotes and market data move daily. Always give the as-of date. Never present a price from memory as current.
- Do not use social media posts, message boards, or promotional newsletters as sources of fact. They may be cited only as evidence of sentiment, labeled as such.

## Memo template (stocks)

```markdown
# [Company name] ([TICKER]) research memo
Prepared YYYY-MM-DD. Data as of the dates cited. Educational use only.

## Snapshot
| Item | Value | Source, date |
|---|---|---|
| Price | | |
| Market cap | | |
| Sector / industry | | |
| 52-week range | | |
| Next earnings date | | |

## Business summary
3 to 5 sentences: what the company sells, to whom, how it makes money,
main segments with revenue share, and where it competes.

## Recent financials
| Metric | Latest period | Prior year period | Change |
|---|---|---|---|
| Revenue | | | |
| Gross margin | | | |
| Operating margin | | | |
| Net income / EPS (diluted) | | | |
| Free cash flow | | | |
| Cash and equivalents | | | |
| Total debt | | | |
Note the trend over the last 4 to 8 quarters in one or two sentences.
Mention guidance if the company gave any.

## Valuation context vs peers
| Company | P/E (fwd or TTM, state which) | EV/Sales | EV/EBITDA | Revenue growth | Margin |
|---|---|---|---|---|---|
| [TICKER] | | | | | |
| Peer 1 | | | | | |
| Peer 2 | | | | | |
| Peer 3 | | | | | |
One paragraph: is the multiple above or below peers and its own history,
and what growth or margin difference might explain the gap. Do not call
the stock "cheap" or "expensive" as a conclusion; describe the gap.

## Catalysts (next 6 to 12 months)
- Dated events: earnings, product launches, regulatory decisions,
  index changes, debt maturities, lockup expirations.

## Bull case
3 to 5 points, each tied to evidence above.

## Bear case
3 to 5 points, each tied to evidence above.

## Key risks
Business, financial (leverage, dilution, liquidity), competitive,
regulatory or legal, concentration (customer, supplier, geography),
and governance. Include stock-level risk: volatility, short interest,
low float, or thin trading where relevant.

## What would change the thesis
Specific, observable signals. Example: "Gross margin below X% for two
quarters" or "loss of the largest customer". Give signals for both
directions.

## Open questions
What could not be verified and what the user may want to check.

## Sources
1. Source name, document, URL if available, as of YYYY-MM-DD.

> Educational information only, not financial advice. ...
```

## ETF variant

Replace "Business summary", "Recent financials", and "Valuation" with:

- **Objective and index:** what the fund tracks and how the index is built (market cap weighted, equal weighted, rules based, actively managed).
- **Holdings and concentration:** number of holdings, top 10 weight, sector and country weights.
- **Costs:** expense ratio; note typical bid-ask spread if available.
- **Size and liquidity:** assets under management, average daily volume.
- **Tracking:** tracking difference vs the index over available periods.
- **Structure risks:** leverage or inverse exposure (daily reset decay), use of derivatives or swaps, commodity futures roll costs, currency exposure, closure risk for small funds.
- **Comparable funds:** two or three alternatives tracking similar exposure, with costs.

Keep catalysts, bull and bear cases, risks, and thesis-change signals.

## Valuation guidance

- State the definition of each multiple. Trailing (TTM) uses the last twelve months; forward uses analyst estimates, which can be wrong.
- P/E is meaningless when earnings are negative or near zero; use EV/Sales or EV/Gross profit instead and say why.
- Banks and insurers: use price to book and return on equity. REITs: use price to FFO or AFFO. Early-stage companies: focus on cash runway and dilution.
- Choose peers with similar business models and size. Explain the peer choice in one line.
- Compare against the company's own 5-year range when the data is available.
- Never compute a fair value or price target. Describe scenarios instead, for example "if growth slowed to the peer average, the multiple gap would be harder to justify".

## Pre-send checklist

- [ ] Every number has a source and an as-of date.
- [ ] No number came from memory without a source.
- [ ] Fiscal periods are labeled.
- [ ] Bull and bear cases have comparable depth.
- [ ] Thesis-change signals are observable and specific.
- [ ] No buy, sell, or hold language; no price targets.
- [ ] Data gaps are listed under open questions.
- [ ] Leverage or options risk is flagged if the user mentioned either.
- [ ] Educational note is at the end.
