# Risk management: sizing, stops, and leverage

Use this file for Workflow 3 and whenever the user asks about risk, stops, leverage, or options.

## Contents

- Inputs and validation
- Fixed-fractional sizing
- Worked examples
- Choosing where the stop sits
- Gap and slippage risk
- Portfolio-level checks
- Losing streak math
- Leverage and options
- Output template

## Inputs and validation

Ask for any missing required input. Do not assume.

| Input | Required | Check |
|---|---|---|
| Account size | Yes | Greater than 0. Ask whether it is the whole account or the trading allocation. |
| Risk percent per trade | Yes | Greater than 0. Above 2 percent, note that a losing streak compounds quickly. |
| Entry price | Yes | Greater than 0. |
| Stop price | Yes | Long: below entry. Short: above entry. Not equal to entry. |
| Direction | Yes, or inferred | Infer from entry vs stop and confirm with the user. |
| Targets | Optional | Long: above entry. Short: below entry. |
| Max position percent | Optional | Caps concentration in one name. |
| Commission and fees | Optional | Per order; counted on entry and exit. |

## Fixed-fractional sizing

The method risks the same fraction of the account on each trade, so the dollar risk shrinks after losses and grows after gains.

```
risk_per_share     = |entry - stop|
risk_budget        = account * risk_pct / 100
shares             = floor((risk_budget - round_trip_fees) / risk_per_share)
position_value     = shares * entry
actual_risk        = shares * risk_per_share + round_trip_fees
R (long target)    = (target - entry) / (entry - stop)
R (short target)   = (entry - target) / (stop - entry)
reward at target   = shares * |target - entry| - round_trip_fees
```

Then apply caps in this order:
1. If `position_value` exceeds the max position cap, set `shares = floor(cap_value / entry)`.
2. If no cap is given and `position_value` exceeds the account size, the trade would need margin. Cap at the account size and say so.

When a cap binds, actual risk is below the budget. Report which constraint was binding.

`1R` is the planned loss per share (or per position). A trade that makes twice the planned risk is `+2R`; a full stop-out is `-1R`.

## Worked examples

**Long, risk budget binds.** Account $25,000, risk 1 percent, entry $50.00, stop $47.50, targets $55.00 and $57.50.
- Budget $250.00. Risk per share $2.50. Shares 100. Position $5,000.00 (20.0 percent).
- $55.00 is 2.0R, reward $500.00. $57.50 is 3.0R, reward $750.00.

**Short with fees.** Account $10,000, risk 0.5 percent, short entry $120.00, stop $126.00, target $108.00, $1 per order.
- Budget $50.00. Fees $2.00. Shares floor(48 / 6) = 8. Position $960.00.
- Actual risk 8 x 6 + 2 = $50.00. Target is 2.0R, reward 8 x 12 - 2 = $94.00.

**Cap binds.** Account $20,000, risk 1 percent, entry $400.00, stop $398.00, max position 25 percent.
- Risk budget alone allows 100 shares ($40,000), which exceeds the account.
- Cap $5,000 allows 12 shares ($4,800). Actual risk $24.00 (0.12 percent). Note that a stop this tight relative to price may be hit by normal fluctuation.

## Choosing where the stop sits

The user chooses the stop. You can describe common approaches without recommending one:
- Structure based: beyond a support zone (long) or resistance zone (short), where the trade idea is shown to be wrong.
- Volatility based: a multiple of ATR from entry, so normal noise is less likely to trigger it.
- Time based: exit if the expected move has not happened within a set period.

Point out when a stop is very tight relative to ATR (likely to be hit by noise) or very wide (forces a small position). Never move the stop for the user to make the size "work"; size follows the stop, not the other way around.

## Gap and slippage risk

- A stop order becomes a market order when triggered. If the stock gaps past the stop (for example after earnings), the fill can be much worse than planned.
- Illustrate: with 100 shares, entry $50.00, stop $47.50, an overnight gap to $42.00 makes the loss $800.00 (3.2R) instead of $250.00.
- Flag known events inside the planned holding period: earnings dates, FDA decisions, court rulings, index rebalances.
- Stop-limit orders can avoid a bad fill but may not fill at all.

## Portfolio-level checks

- Total open risk: sum of the dollar risk of all open positions. Many frameworks keep this within a single-digit percent of the account.
- Correlation: several positions in the same sector or theme behave like one larger position.
- Concentration: a single position above 20 to 25 percent of the account makes the outcome depend heavily on one company.
- Liquidity: position size well above a small fraction of average daily volume can be hard to exit.

Present these as considerations, not rules the user must follow.

## Losing streak math

Remaining account after N consecutive losses at risk r percent: `(1 - r/100)^N`.

| Risk per trade | After 5 losses | After 10 losses | After 20 losses |
|---|---|---|---|
| 0.5% | 97.5% | 95.1% | 90.5% |
| 1% | 95.1% | 90.4% | 81.8% |
| 2% | 90.4% | 81.7% | 66.8% |
| 5% | 77.4% | 59.9% | 35.8% |

Recovery needed after a drawdown of d percent: `d / (100 - d)` as a fraction. A 20 percent drawdown needs a 25 percent gain to recover; 50 percent needs 100 percent.

## Leverage and options

Include the relevant warnings whenever these appear:

- **Margin:** borrowed money magnifies gains and losses. A margin call can force selling at a bad time. Losses can exceed the cash in the account. Interest accrues daily.
- **Short selling:** the loss is theoretically unlimited because price can keep rising. Borrow fees, dividend payments owed, recalls, and short squeezes add risk.
- **Leveraged and inverse ETFs:** they reset daily. Over periods longer than a day, returns can differ greatly from the stated multiple of the index, especially in volatile, sideways markets. Most issuers describe them as short-term instruments.
- **Options:** a bought option can lose 100 percent of its premium at expiration. Time decay works against buyers. Implied volatility often falls after earnings. Selling uncovered options can produce losses far larger than the premium received. Sizing by the stock's stop does not translate directly to options; risk the premium or the defined maximum loss instead.
- **Futures and other derivatives:** outside this skill's main scope; say so and give only general risk warnings.

Never suggest leverage, options, or shorting as a way to increase returns.

## Output template

```markdown
## Position size (educational calculation)
| Item | Value |
|---|---|
| Direction | |
| Account | |
| Risk per trade | x% = $ |
| Entry / stop | |
| Risk per share | |
| Shares | |
| Position value | $ (x% of account) |
| Dollar risk at stop | $ (x% of account) |
| Binding constraint | |

| Target | R-multiple | Reward |
|---|---|---|

Steps: [show the arithmetic]
Notes: gap risk, events in the holding period, leverage warnings if any.

> Educational information only, not financial advice. ...
```
