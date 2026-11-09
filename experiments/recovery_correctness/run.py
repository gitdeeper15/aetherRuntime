#!/usr/bin/env python3
"""
Experiment 3 — Recovery Correctness (M6)

Measures the fraction of recovered states that match ground truth.
Based on Proposition 2 and the recovery layer (Layer 5).

The results are saved to results.json.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetherruntime.models import AgentStatus
from aetherruntime.simulation import Node, create_cluster
from aetherruntime.recovery import create_snapshot, recover
from aetherruntime.halt import propose_halt, approve_halt


def main() -> int:
    print("=" * 70)
    print("Experiment 3 — Recovery Correctness (M6)")
    print("=" * 70)
    print()

    results = []
    n_trials = 10

    for trial in range(n_trials):
        nodes = create_cluster(3, seed=42 + trial)
        proposer = nodes[0]
        target = nodes[1]
        reauthorizer = nodes[2]

        # Create snapshot BEFORE halting
        snapshot = create_snapshot(target.agent, b"initial state")

        # Propose + approve halt
        sig = b"\x01" + b"\x00" * 63
        order = propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=sig,
            reason="test anomaly",
            quorum_threshold=0.5,
        )
        for approver in nodes[:2]:
            approve_halt(order, approver.agent, sig, 2)
            if order.is_enforced():
                break

        # Mark target as halted
        target.agent.status = AgentStatus.HALTED

        # Recover
        try:
            record = recover(
                agent=target.agent,
                halt_order=order,
                snapshot=snapshot,
                replay_log=[],
                reauthorizer=reauthorizer.agent,
            )
            results.append({
                "trial": trial,
                "verification_result": record.verification_result,
                "final_status": target.agent.status.value,
            })
            status = "✅ verified" if record.verification_result else "❌ failed"
            print(f"  Trial {trial + 1}: {status}, "
                  f"final_status={target.agent.status.value}")
        except Exception as e:
            results.append({
                "trial": trial,
                "verification_result": False,
                "error": str(e),
            })
            print(f"  Trial {trial + 1}: ❌ {e}")

    # Statistics
    n_verified = sum(1 for r in results if r.get("verification_result"))
    m6_correctness = n_verified / n_trials if n_trials > 0 else 0.0

    output = {
        "experiment": "recovery_correctness",
        "metrics": ["M6"],
        "config": {
            "n_trials": n_trials,
            "n_nodes": 3,
        },
        "results": results,
        "summary": {
            "n_verified": n_verified,
            "n_trials": n_trials,
            "M6_correctness": round(m6_correctness, 4),
        },
    }

    output_path = Path(__file__).parent / "results.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print()
    print(f"✅ Results saved to {output_path}")
    print(f"   M6 (recovery correctness): {m6_correctness:.4f} "
          f"({n_verified}/{n_trials})")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
