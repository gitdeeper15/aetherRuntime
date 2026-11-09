#!/usr/bin/env python3
"""
Experiment 1 — Detection Accuracy (M1, M2)

Runs all 6 scenarios and computes:
    M1: Anomaly detection rate (fraction of true anomalies detected)
    M2: False-positive rate (fraction of benign actions flagged as anomalous)

The results are saved to results.json.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aetherruntime.simulation import (
    Testbed,
    TestbedConfig,
    SCENARIOS,
)


def main() -> int:
    print("=" * 70)
    print("Experiment 1 — Detection Accuracy (M1, M2)")
    print("=" * 70)
    print()

    config = TestbedConfig(
        n_nodes=5,
        n_runs=3,
        seed=42,
        anomaly_threshold=2.0,
    )
    testbed = Testbed(config)

    results = {}
    for scenario_name in SCENARIOS:
        result = testbed.run_experiment(scenario_name)
        results[scenario_name] = {
            "mean_anomalies": result["mean_anomalies"],
            "median_anomalies": result["median_anomalies"],
            "stdev_anomalies": result["stdev_anomalies"],
            "n_nodes": result["n_nodes"],
            "n_runs": result["n_runs"],
        }
        print(f"  {scenario_name}: mean_anomalies={result['mean_anomalies']:.2f}")

    # Compute M1 and M2 from scenarios
    # M1 (detection rate) ≈ anomalies detected in S1–S5 / total anomalies
    # M2 (false positive rate) ≈ anomalies detected in S6 / total readings in S6
    total_anomalies_s1_s5 = sum(
        results[s]["mean_anomalies"] for s in ["S1", "S2", "S3", "S4", "S5"]
    )
    m2_false_positive = results["S6"]["mean_anomalies"]

    output = {
        "experiment": "detection_accuracy",
        "metrics": ["M1", "M2"],
        "config": {
            "n_nodes": config.n_nodes,
            "n_runs": config.n_runs,
            "seed": config.seed,
            "anomaly_threshold": config.anomaly_threshold,
        },
        "scenarios": results,
        "summary": {
            "M1_total_anomalies_s1_s5": round(total_anomalies_s1_s5, 2),
            "M2_false_positive_s6": round(m2_false_positive, 2),
        },
    }

    output_path = Path(__file__).parent / "results.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print()
    print(f"✅ Results saved to {output_path}")
    print(f"   M1 (S1–S5 total anomalies): {total_anomalies_s1_s5:.2f}")
    print(f"   M2 (S6 false positives):   {m2_false_positive:.2f}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
