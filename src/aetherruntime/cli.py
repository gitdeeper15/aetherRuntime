"""
AetherRuntime v2.0.0 — Command-Line Interface

Usage:
    python -m aetherruntime.cli info
    python -m aetherruntime.cli verify
    python -m aetherruntime.cli simulate --scenario S1 --nodes 5
    python -m aetherruntime.cli experiment --name detection_accuracy
"""

from __future__ import annotations

import argparse
import sys

from .__version__ import (
    __version__,
    __author__,
    __email__,
    __doi__,
    __figshare_doi__,
    __osf_doi__,
    __license__,
    __paper_version__,
    __record_id__,
)


# ═══════════════════════════════════════════════════════════════════════════
# Command: info
# ═══════════════════════════════════════════════════════════════════════════


def cmd_info(args) -> int:
    """Print version, DOI, and record information."""
    print("=" * 70)
    print(f"AetherRuntime v{__version__}")
    print("=" * 70)
    print(f"Author:          {__author__}")
    print(f"Email:           {__email__}")
    print(f"License:         {__license__}")
    print(f"Paper version:   {__paper_version__}")
    print(f"Record ID:       {__record_id__}")
    print(f"DOI (Zenodo):    {__doi__}")
    print(f"DOI (Figshare):  {__figshare_doi__}")
    print(f"DOI (OSF):       {__osf_doi__}")
    print()
    print("AetherRuntime is the sixth functional dimension of the Aether family:")
    print("  AetherGit    (storage)          — 10.5281/zenodo.23966896")
    print("  AetherFlow   (integration)      — 10.5281/zenodo.23979129")
    print("  AetherProof  (verification)     — 10.5281/zenodo.24013124")
    print("  AetherMesh   (decentralization) — 10.5281/zenodo.24038038")
    print("  AetherGovern (governance)       — 10.5281/zenodo.24054524")
    print("  AetherRuntime (runtime assurance) — 10.5281/zenodo.24078477")
    print()
    print("Status: Reference Implementation (v2.0.0).")
    print("        No real-world deployment. Propositions P1–P2 are proof sketches.")
    print("=" * 70)
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# Command: verify
# ═══════════════════════════════════════════════════════════════════════════


def cmd_verify(args) -> int:
    """Run a quick self-check."""
    print("=" * 70)
    print(f"AetherRuntime v{__version__} — self-check")
    print("=" * 70)
    ok = True

    # ─── 1. Ed25519 signature verification ───
    print("[1/5] Signature verification")
    try:
        from .halt.order import _verify_signature
        sig = b"\x01" + b"\x00" * 63  # valid stub
        pub = b"\x01" * 32
        msg = b"test"
        assert _verify_signature(pub, sig, msg), "signature should verify"
        print("      ✅ Signature verifies")
    except Exception as e:
        print(f"      ❌ {e}")
        ok = False

    # ─── 2. Baseline computation ───
    print("[2/5] Baseline computation")
    try:
        from .simulation.node import Node
        from .models import TelemetryCategory
        import random
        node = Node(seed=42)
        node.start()
        rng = random.Random(42)
        for _ in range(20):
            node.collect_telemetry(TelemetryCategory.CPU, rng.gauss(20, 1.0))
        bl = node.update_baseline(
            category=TelemetryCategory.CPU,
            window_size=10,
            baseline_window=20,
        )
        assert bl.sample_count >= 10
        print(f"      ✅ Baseline: mean={bl.parameters['mean']:.2f}, "
              f"std={bl.parameters['std']:.2f}")
    except Exception as e:
        print(f"      ❌ {e}")
        ok = False

    # ─── 3. Detection ───
    print("[3/5] Anomaly detection")
    try:
        record = node.collect_telemetry(TelemetryCategory.CPU, 100.0)
        alert = node.detect_anomaly(record)
        assert alert is not None, "spike should be detected"
        print(f"      ✅ Detected anomaly (confidence={alert.confidence:.2f})")
    except Exception as e:
        print(f"      ❌ {e}")
        ok = False

    # ─── 4. Containment ───
    print("[4/5] Containment")
    try:
        from .containment.policy import contain
        from .models import ContainmentLevel
        policy = contain(
            agent=node.agent,
            alert=alert,
            level=ContainmentLevel.L2_ISOLATE,
            expiry_seconds=300,
        )
        assert policy.level == ContainmentLevel.L2_ISOLATE
        print(f"      ✅ Containment applied: {policy.level.value}")
    except Exception as e:
        print(f"      ❌ {e}")
        ok = False

    # ─── 5. Halt ───
    print("[5/5] Halt and quorum")
    try:
        from .halt.order import propose_halt
        from .halt.quorum import approve_halt
        proposer = Node(seed=99)
        proposer.start()
        target = Node(seed=100)
        target.start()

        sig = b"\x01" + b"\x00" * 63
        order = propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=sig,
            reason="test",
            quorum_threshold=0.67,
        )
        approve_halt(
            halt_order=order,
            approver=proposer.agent,
            approver_signature=sig,
            total_authorized_nodes=1,  # 100% > 67% → quorum
        )
        assert order.is_enforced(), "halt should be enforced"
        print(f"      ✅ Halt enforced (window={order.halt_window_seconds():.6f}s)")
    except Exception as e:
        print(f"      ❌ {e}")
        ok = False

    print("=" * 70)
    if ok:
        print("      ✅ All checks passed")
        return 0
    else:
        print("      ❌ Some checks failed")
        return 1


# ═══════════════════════════════════════════════════════════════════════════
# Command: simulate
# ═══════════════════════════════════════════════════════════════════════════


def cmd_simulate(args) -> int:
    """Run a scenario."""
    from .simulation import Testbed, TestbedConfig

    print("=" * 70)
    print(f"AetherRuntime v{__version__} — simulate {args.scenario}")
    print("=" * 70)

    config = TestbedConfig(
        n_nodes=args.nodes,
        n_runs=args.runs,
        seed=args.seed,
        anomaly_threshold=args.threshold,
    )
    testbed = Testbed(config)
    result = testbed.run_experiment(args.scenario)

    print()
    print(f"Scenario:        {result['scenario']}")
    print(f"Nodes:           {result['n_nodes']}")
    print(f"Runs:            {result['n_runs']}")
    print(f"Mean anomalies:  {result['mean_anomalies']:.2f}")
    print(f"Median anomalies: {result['median_anomalies']:.2f}")
    print(f"Stdev anomalies: {result['stdev_anomalies']:.2f}")
    print("=" * 70)
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# Command: experiment
# ═══════════════════════════════════════════════════════════════════════════


def cmd_experiment(args) -> int:
    """Run an experiment."""
    from .simulation import (
        TestbedConfig,
        experiment_1_detection_accuracy,
        experiment_2_halt_window,
        experiment_3_recovery_correctness,
    )

    print("=" * 70)
    print(f"AetherRuntime v{__version__} — experiment: {args.name}")
    print("=" * 70)

    config = TestbedConfig(
        n_nodes=args.nodes,
        n_runs=args.runs,
        seed=args.seed,
    )

    if args.name == "detection_accuracy":
        result = experiment_1_detection_accuracy(config)
    elif args.name == "halt_window":
        result = experiment_2_halt_window(config)
    elif args.name == "recovery_correctness":
        result = experiment_3_recovery_correctness(config)
    else:
        print(f"❌ Unknown experiment: {args.name}")
        return 1

    print()
    if "scenarios" in result:
        for scenario, data in result["scenarios"].items():
            print(f"  {scenario}: mean_anomalies={data['mean_anomalies']:.2f}")
    else:
        print(f"  {result['results']['scenario']}: "
              f"mean_anomalies={result['results']['mean_anomalies']:.2f}")
    print("=" * 70)
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════


def main(argv=None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="aetherruntime",
        description=f"AetherRuntime v{__version__} — runtime assurance for the Aether family",
    )
    parser.add_argument("--version", action="version",
                       version=f"aetherruntime {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    # info
    p_info = sub.add_parser("info", help="Print version and record info")
    p_info.set_defaults(func=cmd_info)

    # verify
    p_verify = sub.add_parser("verify", help="Run a self-check")
    p_verify.set_defaults(func=cmd_verify)

    # simulate
    p_sim = sub.add_parser("simulate", help="Run a scenario")
    p_sim.add_argument("--scenario", required=True,
                      choices=["S1", "S2", "S3", "S4", "S5", "S6"],
                      help="Scenario name")
    p_sim.add_argument("--nodes", type=int, default=5, help="Number of nodes")
    p_sim.add_argument("--runs", type=int, default=3, help="Number of runs")
    p_sim.add_argument("--seed", type=int, default=42, help="Random seed")
    p_sim.add_argument("--threshold", type=float, default=2.0,
                      help="Anomaly threshold")
    p_sim.set_defaults(func=cmd_simulate)

    # experiment
    p_exp = sub.add_parser("experiment", help="Run an experiment")
    p_exp.add_argument("--name", required=True,
                      choices=["detection_accuracy", "halt_window",
                               "recovery_correctness"],
                      help="Experiment name")
    p_exp.add_argument("--nodes", type=int, default=5, help="Number of nodes")
    p_exp.add_argument("--runs", type=int, default=3, help="Number of runs")
    p_exp.add_argument("--seed", type=int, default=42, help="Random seed")
    p_exp.set_defaults(func=cmd_experiment)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
