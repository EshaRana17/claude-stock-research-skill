# Technical snapshot: methods and template

Use this file for Workflow 2. Technical analysis describes past price and volume behavior. It does not predict outcomes. Say so in every snapshot.

## Contents

- Data requirements
- Trend
- Support and resistance
- Moving averages
- RSI
- Volume
- Plain-English glossary
- Output template
- Caveats to include

## Data requirements

- Columns: date, open, high, low, close, volume. Use adjusted close when splits or dividends occurred in the range; say which you used.
- Sort ascending by date. Drop duplicate dates. Report gaps in the data.
- Minimum bars: 20 for a short-term read, 50 for the 50-day average, 200 for the 200-day average. If there are not enough bars, skip that indicator and say why.
- State the timeframe (daily, weekly, intraday) and the date range.
- If no data is available, explain what to provide (for example a daily CSV export of the last 12 months from a broker or charting site) and stop.

## Trend

Assess on the chosen timeframe:

- **Uptrend:** a sequence of higher swing highs and higher swing lows, price above a rising 50-day average.
- **Downtrend:** lower swing highs and lower swing lows, price below a falling 50-day average.
- **Range:** swing highs and lows roughly flat; averages flat and intertwined.

A swing high is a bar whose high is the highest of the N bars on each side (N = 3 to 5 for daily data). A swing low is the mirror. Report the last two of each with dates.

Also report the percent change over 1 month, 3 months, and 12 months when the data covers them, and distance from the 52-week high and low.

## Support and resistance

- Support is a price zone where declines have repeatedly stopped; resistance is where advances have repeatedly stopped.
- Build zones, not single prices: cluster swing lows (or highs) that fall within about 1 to 2 percent of each other, or within one average true range.
- Rank zones by number of touches, recency, and volume at the touches.
- Note round numbers and prior gaps as possible reference levels, labeled as weaker.
- A broken resistance zone often becomes a reference for support and the reverse. Phrase this as a tendency, not a rule.
- Report the nearest two zones above and below the last close, with the distance in percent.

## Moving averages

- Simple moving average (SMA): mean of the last N closes. Exponential (EMA) weights recent closes more: `EMA_t = close_t * k + EMA_{t-1} * (1 - k)`, with `k = 2 / (N + 1)`.
- Common lengths: 20 (short term), 50 (intermediate), 200 (long term).
- Report: last close vs each average (above or below, percent distance), slope of each (rising, flat, falling over the last 10 bars), and recent crossovers with dates.
- 50 crossing above 200 is often called a "golden cross"; below is a "death cross". Both lag price substantially. Mention that.

## RSI

Relative Strength Index, 14 periods (Wilder):

```
change_t = close_t - close_{t-1}
gain_t = max(change_t, 0); loss_t = max(-change_t, 0)
first avg_gain = mean(gain over first 14 changes); same for avg_loss
then avg_gain_t = (avg_gain_{t-1} * 13 + gain_t) / 14; same for avg_loss
RS = avg_gain / avg_loss
RSI = 100 - 100 / (1 + RS)        (RSI = 100 when avg_loss is 0)
```

Interpretation:
- Above 70 is commonly read as "overbought", below 30 as "oversold". In strong trends RSI can stay in these zones for weeks, so they are not signals on their own.
- In uptrends RSI often holds above 40; in downtrends it often stays below 60.
- Divergence: price makes a new high while RSI makes a lower high (or the mirror for lows). It suggests weakening momentum, not a reversal.

## Volume

- Compare recent volume with its 20-day or 50-day average. Report the ratio.
- Volume above average on up days and below average on pullbacks is often read as accumulation; the reverse as distribution.
- Breakouts through a zone on low volume are less convincing than on high volume.
- Very high volume spikes often coincide with news; check for an earnings date or announcement and mention it.
- Thinly traded stocks (low average dollar volume) have wider spreads and larger slippage. Flag this.

## Plain-English glossary

Use these one-line explanations the first time a term appears:

- **Moving average:** the average closing price over the last N days, used to smooth out daily noise.
- **Support:** a price area where buyers have stepped in before.
- **Resistance:** a price area where sellers have stepped in before.
- **RSI:** a 0 to 100 score of how strong recent gains were compared with recent losses.
- **Divergence:** when price and an indicator move in opposite directions.
- **Average true range (ATR):** the typical daily price range, including gaps.

## Output template

```markdown
# [TICKER] technical snapshot
Data: [source], [timeframe], [start date] to [end date], [N] bars.
Last close: $X.XX on YYYY-MM-DD.

## Summary
2 to 3 sentences describing the current structure in plain English.

## Trend
## Support and resistance
| Zone | Type | Touches | Distance from last close |
## Moving averages
| Average | Value | Close vs average | Slope |
## Momentum (RSI 14)
## Volume
## What would confirm or invalidate this picture
- Confirm: ...
- Invalidate: ...

## Caveats
...

> Educational information only, not financial advice. ...
```

## Caveats to include

- Indicators are calculated from past prices and lag.
- Patterns fail often; there is no reliable win rate for any single signal.
- News, earnings, and macro events can override any chart structure.
- Values computed without code execution are approximate.
- Different data providers may show slightly different values due to adjustments.
