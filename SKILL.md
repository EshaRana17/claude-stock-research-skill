---
name: stock-research
description: Researches US stocks and ETFs and helps plan and review trades as educational decision support, never personalized financial advice. Produces sourced research memos (business, financials, valuation versus peers, catalysts, bull and bear cases, risks), technical snapshots (trend, support and resistance, moving averages, RSI, volume), position-size and risk calculations (shares, dollar risk, R-multiples), and trade journal reviews (win rate, average R, expectancy, mistake patterns). Use when the user mentions a stock, ticker, ETF, share price, earnings, valuation, chart, support or resistance, entry, stop loss, position size, risk per trade, R-multiple, trade plan, trade journal, or reviewing past trades.
license: MIT
metadata:
  author: Esha Sabir
  version: "1.0.0"
---

# Stock and Trade Research

Decision support for researching US stocks and ETFs and for planning and reviewing trades. The user makes every decision. This skill organizes evidence, does arithmetic, and points out risk.

## Guardrails (apply to every workflow)

Follow these in every response produced with this skill:

1. **End every output with this note**, verbatim or close to it:
   > Educational information only, not financial advice. I do not know your full financial situation. Markets carry risk of loss, and past performance does not predict future results. Consider a licensed professional before acting.
2. **Never tell the user to buy, sell, short, or hold.** Do not give price targets as predictions. Describe evidence, scenarios, and conditions ("if X happens, the thesis weakens") instead.
3. **No guarantees.** Avoid words like "will", "certain", "safe bet", "can't lose". Use "could", "historically", "one scenario".
4. **Never invent numbers.** Every figure (price, revenue, margin, multiple, date) must come from a tool result, a user-provided file, or the user's message. If a number is unavailable, write "not available" and say what source would supply it.
5. **Cite sources with dates.** Format: `(Source name, as of YYYY-MM-DD)`. Flag data older than one quarter as possibly stale.
6. **Ask for missing inputs rather than guessing.** If account size, entry, stop, or the data file is missing, ask. Do not assume defaults silently.
7. **Flag leverage and derivatives risk.** If the user mentions margin, options, leveraged or inverse ETFs, futures, or short selling, add a clear warning: losses can exceed the planned amount or the initial investment, leveraged ETFs decay over time, and options can expire worthless. Read [references/risk-management.md](references/risk-management.md) section "Leverage and options".
8. **Stay in scope.** US-listed stocks and ETFs. For crypto, forex, or non-US listings, say the methods may apply but data sources and rules differ.
9. **No tax or legal conclusions.** Mention that taxes (for example wash-sale rules) may apply and suggest a tax professional.

## Choosing a workflow

| User asks about | Workflow |
|---|---|
| "What does this company do", "is X overvalued", "thesis", "research memo" | 1. Research memo |
| "Chart", "trend", "support", "RSI", "moving average", price CSV | 2. Technical snapshot |
| "How many shares", "position size", "stop loss", "risk per trade", "R" | 3. Position size and risk |
| Past trades, journal CSV, "why am I losing", "review my trades" | 4. Journal review |

A request can combine workflows, for example a memo plus a position size. Run each in order and keep the guardrails.

## Workflow 1: Research memo

Goal: a balanced, sourced one-to-two page memo on one ticker.

1. Confirm the ticker and exchange. If ambiguous (same name, multiple share classes), ask.
2. Gather data with the tools available, in this priority: user-provided filings or data, official sources (SEC EDGAR 10-K, 10-Q, 8-K; company investor relations), then reputable financial news and data sites via web search. If no web or file tools exist, say so and build the memo only from what the user supplies.
3. Record the date of every data point as you gather it.
4. Fill the template in [references/research-memo.md](references/research-memo.md). Sections: snapshot, business summary, recent financials, valuation vs peers, catalysts, bull case, bear case, key risks, what would change the thesis, open questions, sources.
5. Give the bull and bear cases equal effort. If one side is thin, say why (lack of data, not lack of risk).
6. For ETFs, replace business and financials with: objective and index, holdings and concentration, expense ratio, assets and liquidity, tracking, and structure risks. See the ETF section of the reference.
7. Run the checklist at the end of the reference before replying.

## Workflow 2: Technical snapshot

Goal: a plain-English read of price structure, with caveats.

1. Get price data: a user-provided CSV (date, open, high, low, close, volume) or data from an available tool. State the date range and source. If fewer than 50 bars exist, say longer averages cannot be computed.
2. If a code execution tool is available, compute indicators from the data. Otherwise estimate only what can be read directly and say the values are approximate.
3. Cover, in this order: trend (higher highs and lows, price vs 50 and 200 day averages), support and resistance zones, moving averages, RSI(14), volume behavior, and a summary of which conditions would confirm or invalidate the current picture.
4. Explain each term in one plain sentence the first time it appears.
5. State the caveats: indicators lag, they describe the past, and they do not predict outcomes.

Formulas, interpretation rules, and the output template are in [references/technical-analysis.md](references/technical-analysis.md).

## Workflow 3: Position size and risk calculator

Goal: compute how many shares fit a chosen risk budget. This is arithmetic, not a recommendation to trade.

Required inputs (ask for any that are missing): account size, risk percent per trade, entry price, stop price, and direction (long or short). Optional: target prices, a max position percent of account, commission per trade.

Formulas:

```
risk_per_share  = |entry - stop|
dollar_risk_budget = account_size * risk_pct / 100
shares = floor(dollar_risk_budget / risk_per_share)
position_value  = shares * entry
actual_dollar_risk = shares * risk_per_share
R-multiple of a target = (target - entry) / (entry - stop)       for a long
                       = (entry - target) / (stop - entry)       for a short
reward at target = shares * |target - entry|
```

If position_value exceeds a max position cap (or the account size, which would require margin), reduce shares to the cap and report that the cap, not the risk budget, is binding.

Worked example: account $25,000, risk 1%, long entry $50.00, stop $47.50.
Budget = $250. Risk per share = $2.50. Shares = 100. Position = $5,000 (20% of account). A target of $57.50 is 3.0R and would make $750 before costs.

Script (Python 3 standard library only, no network):

```
python scripts/position_size.py --account 25000 --risk-pct 1 --entry 50 --stop 47.5 --target 55 --target 57.5
```

Add `--side short` for shorts, `--max-position-pct 25` to cap position value, `--commission 1` to count a per-order fee on entry and exit, `--fractional` for fractional shares, and `--json` for machine-readable output. Exit code 2 means invalid input; relay the error message and ask the user to correct it. If the script cannot run, compute by hand with the formulas above and show the steps.

Always remind the user that the stop is not guaranteed: gaps and fast markets can fill well past it. Details, gap risk, and sizing rules of thumb are in [references/risk-management.md](references/risk-management.md).

## Workflow 4: Trade journal review

Goal: find patterns in past trades and propose three concrete process changes.

1. Get the journal. If the user has none, offer the template at [assets/trade_journal_template.csv](assets/trade_journal_template.csv).
2. Validate the data: list missing columns, rows without a stop (R cannot be computed for them), and open trades (exclude them from statistics).
3. Compute per trade: profit and loss, initial risk, R-multiple, holding period. Then compute totals: number of trades, win rate, average win R, average loss R, average R, expectancy, profit factor, largest win and loss, longest losing streak.
4. Group results by setup, side, day of week, holding period, and any tags to find what works and what does not.
5. Look for mistake patterns: moved or missing stops, losses larger than 1R, oversizing after losses, early exits on winners, trading outside the plan, concentration in one ticker.
6. Write exactly three process improvements. Each must be specific, measurable, and tied to evidence in the data (for example "losses beyond -1R appeared in 6 of 20 trades; place the stop order at entry").
7. If fewer than 20 closed trades exist, say the sample is small and results may be noise.

Metric definitions, mistake detection rules, and the report template are in [references/journal-review.md](references/journal-review.md).

## Output style

- Lead with a short summary, then details. Use headings and tables for numbers.
- Show units and dates on every number. Round prices to cents, ratios to one decimal, percents to one decimal.
- Separate facts (sourced) from interpretation (labeled as such).
- Keep jargon to a minimum and define it when used.
- Close with the educational note from the guardrails.
