# Trade journal review: metrics and report

Use this file for Workflow 4. The goal is better process, not judging the user. Focus on decisions the user controls: sizing, stops, entries, exits, and following the plan.

## Contents

- Expected columns
- Data cleaning
- Per-trade calculations
- Summary metrics
- Breakdowns
- Mistake patterns
- Writing the three improvements
- Report template

## Expected columns

The template at `assets/trade_journal_template.csv` uses these columns:

| Column | Meaning |
|---|---|
| trade_id | Unique number |
| date_open, date_close | YYYY-MM-DD; date_close empty if still open |
| ticker | Symbol |
| side | long or short |
| setup | User's name for the strategy, for example breakout or pullback |
| entry_price, exit_price | Average fill prices |
| shares | Number of shares |
| initial_stop | Stop price planned at entry |
| planned_target | Optional |
| fees | Total commissions and fees for the round trip |
| followed_plan | yes or no |
| emotion | Optional one word, for example calm, fomo, revenge |
| notes | Free text |

If the user's file uses other names, map them and state the mapping. If the user gives free-text notes instead of a CSV, extract the same fields and list anything you could not find.

## Data cleaning

Before computing, report:
- Rows with a missing exit (open trades): exclude from statistics, list them.
- Rows with no initial_stop: R cannot be computed; include them in dollar statistics only and count them.
- Rows where the stop is on the wrong side of the entry: likely a data error; ask.
- Duplicate trade_ids, impossible dates (close before open), zero or negative prices or shares.

Never fill missing values with guesses.

## Per-trade calculations

```
direction  = +1 for long, -1 for short
pnl        = direction * (exit_price - entry_price) * shares - fees
risk_1r    = |entry_price - initial_stop| * shares
r_multiple = pnl / risk_1r
hold_days  = date_close - date_open (calendar days)
```

A trade is a win if pnl > 0, a loss if pnl < 0, and breakeven if pnl = 0. State how breakevens are treated (excluded from win rate denominator or counted as non-wins) and be consistent.

## Summary metrics

| Metric | Formula |
|---|---|
| Closed trades | count |
| Win rate | wins / closed trades |
| Average win (R and $) | mean of winning trades |
| Average loss (R and $) | mean of losing trades |
| Average R | mean r_multiple across trades with a stop |
| Expectancy (R) | win_rate * avg_win_R + (1 - win_rate) * avg_loss_R (avg_loss_R is negative); equals Average R when breakevens are zero |
| Expectancy ($) | total net pnl / closed trades |
| Profit factor | sum of winning pnl / absolute sum of losing pnl |
| Payoff ratio | average win $ / absolute average loss $ |
| Largest win and loss | by $ and by R |
| Max consecutive losses | longest losing streak by close date |
| Max drawdown | largest peak-to-trough drop in cumulative pnl |
| Total net pnl | sum of pnl |

Interpretation hints:
- A positive expectancy in R means the process made money per unit of risk in this sample. It does not guarantee future results.
- A low win rate can still be profitable with large average wins, and the reverse.
- Under 20 closed trades: call the sample small. Under 50: call conclusions tentative.

If a code execution tool is available, compute with code (Python standard library `csv` module is enough). Otherwise compute by hand for small files and show the totals so the user can check them.

## Breakdowns

Group by each of these when the column exists and has at least 3 trades per group:
- setup
- side
- ticker (top 5 by count)
- holding period buckets: same day, 1 to 5 days, 6 to 20 days, over 20 days
- followed_plan yes vs no
- emotion tag
- day of week of entry

For each group report count, win rate, average R, and total pnl. Highlight the best and worst groups, noting sample size.

## Mistake patterns

Check for each and report the count and the trades involved:

| Pattern | Detection rule |
|---|---|
| Stop not honored | r_multiple below -1.2 (allowing for some slippage) |
| No stop planned | initial_stop missing |
| Cutting winners early | winners exiting below planned_target with r_multiple under 1 while planned target R was 2 or more |
| Oversizing | risk_1r more than 1.5 times the median risk_1r |
| Revenge or tilt trading | a trade opened the same day as, or the day after, a loss and sized larger than the median; or emotion tagged revenge or fomo |
| Plan drift | followed_plan = no, compare its average R with followed_plan = yes |
| Concentration | one ticker or setup accounts for most of the losses |
| Overtrading | days with an unusually high trade count compared with the user's normal, and their results |
| Fee drag | fees above about 10 percent of gross profit |

Describe patterns neutrally, as observations about the data.

## Writing the three improvements

Each improvement must:
1. Cite the evidence (numbers from this journal).
2. State one specific behavior change.
3. Include a measurable check for the next review.

Example format:
- **Evidence:** 5 of 18 losses were worse than -1.2R, costing a combined -4.6R beyond plan.
- **Change:** enter the stop order at the same time as the entry order.
- **Measure:** zero losses beyond -1.2R in the next 20 trades, excluding overnight gaps.

Do not suggest specific tickers, trades, or market calls. Improvements are about process: sizing, stops, entries, exits, record keeping, review cadence, and rule following.

## Report template

```markdown
# Trade journal review
Data: [file], [N] rows, [date range]. Closed trades analyzed: [n].
Excluded: [open trades], [rows without stop for R metrics].

## Summary
2 to 3 sentences.

## Key metrics
| Metric | Value |

## What worked
## What did not work
## Mistake patterns
| Pattern | Count | Impact (R or $) | Trades |

## Three process improvements
1. ...
2. ...
3. ...

## Data notes and limits

> Educational information only, not financial advice. ...
```
