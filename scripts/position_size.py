#!/usr/bin/env python3
"""Position size and risk calculator for a single stock or ETF trade.

Computes how many shares fit a fixed-percentage risk budget given an entry
and a stop, then reports dollar risk, position value, and the R-multiple and
reward of each optional target.

Standard library only. Makes no network calls, reads no files, and writes
nothing to disk. Educational use only; this is arithmetic, not advice.

Examples:
    python position_size.py --account 25000 --risk-pct 1 --entry 50 --stop 47.5
    python position_size.py --account 10000 --risk-pct 0.5 --entry 120 \
        --stop 126 --side short --target 108 --json
"""

from __future__ import annotations

import argparse
import json
import math
import sys

DISCLAIMER = (
    "Educational calculation only, not financial advice. Stops are not "
    "guaranteed: gaps and fast markets can fill beyond the stop price."
)

HIGH_RISK_PCT = 2.0


class InputError(ValueError):
    """Raised when the user's inputs are inconsistent or out of range."""


def positive_float(text: str) -> float:
    """argparse type: a finite number greater than zero."""
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a number")
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(f"'{text}' must be a number greater than 0")
    return value


def non_negative_float(text: str) -> float:
    """argparse type: a finite number zero or greater."""
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a number")
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError(f"'{text}' must be a number 0 or greater")
    return value


def infer_side(entry: float, stop: float, side: str | None) -> str:
    """Return 'long' or 'short', checking that the stop is on the losing side."""
    if entry == stop:
        raise InputError("entry and stop cannot be equal; risk per share would be zero")
    implied = "long" if stop < entry else "short"
    if side is None:
        return implied
    if side != implied:
        if side == "long":
            raise InputError(
                f"for a long trade the stop ({stop}) must be below the entry ({entry})"
            )
        raise InputError(
            f"for a short trade the stop ({stop}) must be above the entry ({entry})"
        )
    return side


def calculate(
    account: float,
    risk_pct: float,
    entry: float,
    stop: float,
    side: str | None = None,
    targets: list[float] | None = None,
    max_position_pct: float | None = None,
    commission: float = 0.0,
    fractional: bool = False,
) -> dict:
    """Compute position size and risk figures. Raises InputError on bad input."""
    if not 0 < risk_pct <= 100:
        raise InputError("risk percent must be greater than 0 and at most 100")
    if max_position_pct is not None and not 0 < max_position_pct <= 1000:
        raise InputError("max position percent must be greater than 0 and at most 1000")

    side = infer_side(entry, stop, side)
    targets = targets or []
    for target in targets:
        if side == "long" and target <= entry:
            raise InputError(f"target {target} must be above the entry {entry} for a long")
        if side == "short" and target >= entry:
            raise InputError(f"target {target} must be below the entry {entry} for a short")

    warnings: list[str] = []
    risk_per_share = abs(entry - stop)
    budget = account * risk_pct / 100
    round_trip_cost = 2 * commission
    budget_for_shares = budget - round_trip_cost
    if budget_for_shares <= 0:
        raise InputError(
            f"round-trip commission (${round_trip_cost:,.2f}) uses the whole risk "
            f"budget (${budget:,.2f}); no position fits"
        )

    def size(raw: float) -> float:
        return raw if fractional else float(math.floor(raw))

    shares = size(budget_for_shares / risk_per_share)
    binding = "risk budget"

    cap_pct = max_position_pct if max_position_pct is not None else 100.0
    cap_value = account * cap_pct / 100
    if shares * entry > cap_value:
        shares = size(cap_value / entry)
        binding = (
            f"max position cap ({cap_pct:g}% of account)"
            if max_position_pct is not None
            else "account size (no margin assumed)"
        )

    if shares <= 0:
        raise InputError(
            "the risk budget or position cap is too small to buy one share at this "
            "entry; consider --fractional if your broker supports it"
        )

    position_value = shares * entry
    actual_risk = shares * risk_per_share + round_trip_cost

    if risk_pct > HIGH_RISK_PCT:
        warnings.append(
            f"risking {risk_pct:g}% per trade is above the {HIGH_RISK_PCT:g}% many "
            "risk frameworks use as an upper bound; a losing streak compounds quickly"
        )
    if max_position_pct is not None and max_position_pct > 100:
        warnings.append("a position cap above 100% of the account implies margin (leverage)")
    if risk_per_share / entry < 0.005:
        warnings.append(
            "the stop is within 0.5% of entry; normal price noise may trigger it"
        )
    if binding != "risk budget":
        warnings.append(
            f"size is limited by the {binding}, so actual risk is below the budget"
        )

    target_rows = []
    for target in targets:
        move = (target - entry) if side == "long" else (entry - target)
        target_rows.append(
            {
                "target": round(target, 4),
                "r_multiple": round(move / risk_per_share, 2),
                "reward": round(shares * move - round_trip_cost, 2),
            }
        )

    return {
        "side": side,
        "account": round(account, 2),
        "risk_pct": risk_pct,
        "entry": entry,
        "stop": stop,
        "risk_per_share": round(risk_per_share, 4),
        "risk_budget": round(budget, 2),
        "round_trip_commission": round(round_trip_cost, 2),
        "shares": shares if fractional else int(shares),
        "position_value": round(position_value, 2),
        "position_pct_of_account": round(position_value / account * 100, 2),
        "actual_dollar_risk": round(actual_risk, 2),
        "actual_risk_pct": round(actual_risk / account * 100, 3),
        "binding_constraint": binding,
        "targets": target_rows,
        "warnings": warnings,
        "disclaimer": DISCLAIMER,
    }


def format_report(result: dict) -> str:
    """Render the result as a plain-text report."""
    money = lambda v: f"${v:,.2f}"  # noqa: E731
    shares = result["shares"]
    shares_text = f"{shares:,}" if isinstance(shares, int) else f"{shares:,.4f}"
    lines = [
        "Position size and risk",
        "----------------------",
        f"Side:                 {result['side']}",
        f"Account:              {money(result['account'])}",
        f"Risk per trade:       {result['risk_pct']:g}% = {money(result['risk_budget'])}",
        f"Entry / stop:         {money(result['entry'])} / {money(result['stop'])}",
        f"Risk per share:       {money(result['risk_per_share'])}",
    ]
    if result["round_trip_commission"]:
        lines.append(f"Round-trip commission: {money(result['round_trip_commission'])}")
    lines += [
        f"Shares:               {shares_text}",
        f"Position value:       {money(result['position_value'])} "
        f"({result['position_pct_of_account']:.1f}% of account)",
        f"Dollar risk at stop:  {money(result['actual_dollar_risk'])} "
        f"({result['actual_risk_pct']:.2f}% of account)",
        f"Limited by:           {result['binding_constraint']}",
    ]
    if result["targets"]:
        lines += ["", "Targets", "-------", f"{'Price':>12}  {'R':>6}  {'Reward':>12}"]
        for row in result["targets"]:
            lines.append(
                f"{money(row['target']):>12}  {row['r_multiple']:>5.2f}R  {money(row['reward']):>12}"
            )
    if result["warnings"]:
        lines += ["", "Warnings"]
        lines += [f"- {w}" for w in result["warnings"]]
    lines += ["", result["disclaimer"]]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compute shares, dollar risk, and R-multiples for a trade from a fixed "
            "percentage risk budget. Educational use only."
        )
    )
    parser.add_argument("--account", type=positive_float, required=True,
                        help="account size in dollars")
    parser.add_argument("--risk-pct", type=positive_float, required=True,
                        help="percent of the account to risk on this trade, e.g. 1")
    parser.add_argument("--entry", type=positive_float, required=True,
                        help="planned entry price per share")
    parser.add_argument("--stop", type=positive_float, required=True,
                        help="planned stop-loss price per share")
    parser.add_argument("--side", choices=["long", "short"],
                        help="trade direction; inferred from entry and stop if omitted")
    parser.add_argument("--target", type=positive_float, action="append", default=[],
                        help="target price; repeat for several targets")
    parser.add_argument("--max-position-pct", type=positive_float,
                        help="cap position value at this percent of the account")
    parser.add_argument("--commission", type=non_negative_float, default=0.0,
                        help="commission per order in dollars (counted twice: entry and exit)")
    parser.add_argument("--fractional", action="store_true",
                        help="allow fractional shares instead of rounding down")
    parser.add_argument("--json", action="store_true",
                        help="print machine-readable JSON instead of a text report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = calculate(
            account=args.account,
            risk_pct=args.risk_pct,
            entry=args.entry,
            stop=args.stop,
            side=args.side,
            targets=args.target,
            max_position_pct=args.max_position_pct,
            commission=args.commission,
            fractional=args.fractional,
        )
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
