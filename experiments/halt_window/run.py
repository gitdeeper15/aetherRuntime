#!/usr/bin/env python3
"""
Experiment 2 — Halt Window (M5)

Measures the time from detection to halt enforcement (Δt_window).
Based on Proposition 2 (irreducible halt window).

The results are saved to results.json.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetherruntime.models import AgentStatus
from aetherruntime.simulation import Node, create_cluster
from aetherruntime.halt import propose_halt, approve_halt, QuorumTracker


def main() -> int:
    print("=" * 70)
    print("Experiment 2 — Halt Window (M5)")
    print("=" * 70)
    print()

    results = []
    n_trials = 10

    for trial in range(n_trials):
        nodes = create_cluster(5, seed=42 + trial)
        proposer = nodes[0]
        target = nodes[1]

        # Propose halt
        sig = b"\x01" + b"\x00" * 63
        order = propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=sig,
            reason="test anomaly",
            quorum_threshold=0.67,
        )

        # Approve with quorum (4/5 = 80% > 67%)
        approvals = 0
        for approver in nodes[1:5]:
            approve_halt(
                halt_order=order,
                approver=approver.agent,
                approver_signature=sig,
                total_authorized_nodes=5,
            )
            approvals += 1
            if order.is_enforced():
                break

        # Compute halt window
        window = order.halt_window_seconds()
        results.append({
            "trial": trial,
            "approvals": approvals,
            "enforced": order.is_enforced(),
            "window_seconds": window if window is not None else 0.0,
        })

        print(f"  Trial {trial + 1}: approvals={approvals}, "
              f"window={window:.6f}s" if window else
              f"  Trial {trial + 1}: not enforced")

    # Statistics
    enforced_windows = [r["window_seconds"] for r in results if r["enforced"]]
    import statistics

    output = {
        "experiment": "halt_window",
        "metrics": ["M5"],
        "config": {
            "n_trials": n_trials,
            "n_nodes": 5,
            "quorum_threshold": 0.67,
        },
        "results": results,
        "summary": {
            "n_enforced": len(enforced_windows),
            "mean_window_seconds": (
                statistics.mean(enforced_windows) if enforced_windows else 0.0
            ),
            "median_window_seconds": (
                statistics.median(enforced_windows) if enforced_windows else 0.0
            ),
            "min_window_seconds": (
                min(enforced_windows) if enforced_windows else 0.0
            ),
            "max_window_seconds": (
                max(enforced_windows) if enforced_windows else 0.0
            ),
        },
    }

    output_path = Path(__file__).parent / "results.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print()
    print(f"✅ Results saved to {output_path}")
    print(f"   Enforced: {len(enforced_windows)} / {n_trials}")
    if enforced_windows:
        print(f"   Mean window:   {statistics.mean(enforced_windows):.6f}s")
        print(f"   Median window: {statistics.median(enforced_windows):.6f}s")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
