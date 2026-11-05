# stock-research: a Claude Agent Skill for stock and trade research

An open-source [Agent Skill](https://agentskills.io) that helps Claude research US stocks and ETFs and help you plan and review trades responsibly. It is decision support for learning and organizing your own thinking. It does not tell you what to buy or sell.

## What it does

| Workflow | You get |
|---|---|
| Research memo | Business summary, recent financials, valuation context vs peers, catalysts, bull and bear cases, key risks, and what would change the thesis. Every number is sourced and dated; missing data is marked "not available" instead of guessed. |
| Technical snapshot | Trend, support and resistance zones, moving averages, RSI, and volume, explained in plain English with caveats. Works from a price CSV you provide or data Claude can fetch with its own tools. |
| Position size and risk | Shares, dollar risk, position value, and R-multiples for your targets from account size, risk percent, entry, and stop. Includes a small Python calculator; the formulas are also in the skill so it works without code. |
| Trade journal review | Win rate, average R, expectancy, profit factor, drawdown, mistake patterns, and three concrete process improvements, from a CSV or notes of your past trades. |

Built-in guardrails: every answer ends with an educational, not-financial-advice note; no buy, sell, or hold calls; no price targets or guarantees; warnings for margin, shorting, leveraged ETFs, and options; and Claude asks for missing inputs instead of guessing.

## Example prompts

- "Write a research memo on COST. Compare valuation with WMT, TGT, and BJ."
- "Here is a CSV of SPY daily prices for the last year. Give me a technical snapshot."
- "My account is $30,000 and I risk 1 percent per trade. Long entry 84.20, stop 80.90, targets 90 and 95. How many shares?"
- "Review my trade journal (attached) and tell me what patterns are costing me."
- "I want to trade TQQQ. What risks should I understand first?"

## Repository layout

```
claude-stock-research-skill/
  SKILL.md                         Instructions Claude loads when the skill triggers
  references/
    research-memo.md               Memo template, valuation guidance, checklist
    technical-analysis.md          Indicator formulas, interpretation, template
    risk-management.md             Sizing math, stops, gap risk, leverage and options
    journal-review.md              Metrics, mistake detection, report template
  scripts/
    position_size.py               Position size calculator (Python 3 stdlib only)
  assets/
    trade_journal_template.csv     Starter journal with example rows
  agent.json                       Manifest (no network, no env vars)
  LICENSE                          MIT
  README.md
```

Claude reads only `SKILL.md` when the skill activates and opens a reference file only when a workflow needs it (progressive disclosure), which keeps context use low.

## Install

The skill's `name` is `stock-research`. The Agent Skills specification requires the folder that contains `SKILL.md` to have the same name, so install it into a folder called `stock-research`.

### Claude Code

Personal (all projects on this machine):

```bash
git clone https://github.com/EshaRana17/claude-stock-research-skill.git
mkdir -p ~/.claude/skills
cp -r claude-stock-research-skill ~/.claude/skills/stock-research
```

Project (shared with everyone who uses the repository):

```bash
mkdir -p .claude/skills
cp -r claude-stock-research-skill .claude/skills/stock-research
```

Start a new Claude Code session. Claude picks the skill up automatically when you mention a stock, ticker, trade, position size, or journal. You can also invoke it directly with `/stock-research`.

### Claude.ai (web and desktop apps)

1. Package the folder as a ZIP whose top-level folder is `stock-research` and contains `SKILL.md`. For example, from the parent directory:
   ```bash
   cp -r claude-stock-research-skill stock-research
   zip -r stock-research.zip stock-research -x "*/.git/*"
   ```
2. In Claude, open **Customize > Skills**, click the **+** button, choose **Create skill**, then **Upload a skill**, and select the ZIP. (Older help pages called this area Settings > Capabilities; the Anthropic help article "Using Skills in Claude" has the current steps.)
3. Make sure code execution is enabled, which skills require on Claude.ai, and that the skill is toggled on.

Custom skills are available on paid plans. Skills uploaded to Claude.ai do not sync to Claude Code or the API; install each surface separately.

### Other SKILL.md-compatible agents

Any agent that implements the open Agent Skills format can use this folder as is. Copy the `stock-research` folder into that agent's skills directory (check its documentation for the path). The frontmatter uses only standard fields (`name`, `description`, `license`, `metadata`). If an agent cannot run Python, the skill still works: the sizing formulas are written out in `SKILL.md`.

## Using the calculator directly

Requires Python 3.8 or later. No packages to install.

```bash
python scripts/position_size.py --account 25000 --risk-pct 1 --entry 50 --stop 47.5 --target 55 --target 57.5
```

```
Shares:               100
Position value:       $5,000.00 (20.0% of account)
Dollar risk at stop:  $250.00 (1.00% of account)
Limited by:           risk budget
...
      $55.00   2.00R       $500.00
      $57.50   3.00R       $750.00
```

Options: `--side long|short` (inferred from entry and stop if omitted), `--target` (repeatable), `--max-position-pct`, `--commission` (per order, counted on entry and exit), `--fractional`, `--json`. Run with `--help` for details. Invalid input exits with code 2 and a clear message.

## Security

- The skill makes **no network calls of its own**. `scripts/position_size.py` uses only the Python standard library, does not import any networking module, reads no files, writes nothing to disk, and needs no environment variables or API keys. `agent.json` declares `"network": []` and `"env": []`.
- Any web research happens through tools your agent already has (for example web search) and under that agent's own permission prompts. The skill never asks for brokerage credentials and never places orders.
- No shell commands in the skill modify your system.
- This skill was scanned on AgenticMart: <https://agenticmart.org/verified>.

You are encouraged to read every file before installing; the whole skill is a few hundred lines of Markdown and one short Python script.

## Disclaimer

This project is for educational and informational purposes only. It is not financial, investment, tax, or legal advice, and it is not a recommendation to buy, sell, or hold any security. The authors are not licensed financial advisors. Outputs may be incomplete, outdated, or wrong, including data retrieved by the AI from third-party sources. Trading and investing involve risk of loss, including loss of more than your initial investment when using margin, short selling, or derivatives. Past performance does not predict future results. Verify all information independently and consider consulting a licensed professional before making financial decisions. You are solely responsible for your decisions.

## Contributing

Issues and pull requests are welcome. Please keep contributions original, dependency free, and consistent with the guardrails above.

## License

[MIT](LICENSE). Copyright (c) 2026 Esha Sabir.
