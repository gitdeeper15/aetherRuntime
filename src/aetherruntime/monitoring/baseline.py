"""
AetherRuntime v2.0.0 — Monitoring: Baseline Computation

This module implements Operation 2 (`update_baseline`) from
docs/specification/02_operations.md.

The `update_baseline` operation computes a statistical model of
expected behaviour for an agent's telemetry category. It is the
reference point for anomaly detection (Layer 2).

Invariants enforced:
    - I7: sample_count >= 10
    - I8: parameters contains required keys for model_type

Errors:
    - E5: AgentNotFound
    - E6: InsufficientTelemetry
    - E7: InvalidWindowSize
"""

from __future__ import annotations

import statistics
from datetime import datetime, timezone
from typing import Optional

from ..models import (
    Agent,
    Baseline,
    BaselineModel,
    TelemetryCategory,
    TelemetryRecord,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class AgentNotFound(Exception):
    """E5: Agent does not exist."""
    pass


class InsufficientTelemetry(Exception):
    """E6: Fewer than window_size telemetry records exist."""
    pass


class InvalidWindowSize(Exception):
    """E7: window_size < 10."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Operation 2 — update_baseline
# ═══════════════════════════════════════════════════════════════════════════


def update_baseline(
    agent: Agent,
    category: TelemetryCategory,
    model_type: BaselineModel,
    window_size: int,
    telemetry_records: list[TelemetryRecord],
    existing_baseline: Optional[Baseline] = None,
) -> Baseline:
    """
    Update the baseline model for an agent's telemetry category (Operation 2).

    Args:
        agent: The agent to compute a baseline for.
        category: Telemetry category (cpu, memory, network, syscall, action).
        model_type: Baseline model type (mean_std, zscore, moving_average, seasonal).
        window_size: Number of recent telemetry records to use.
        telemetry_records: All telemetry records for the agent.
        existing_baseline: Optional existing baseline (to preserve baseline_id).

    Returns:
        A new (or updated) `Baseline` with computed parameters.

    Raises:
        AgentNotFound: If agent is None.
        InvalidWindowSize: If window_size < 10.
        InsufficientTelemetry: If fewer than window_size records exist.

    Invariants:
        I7: sample_count >= 10.
        I8: parameters contains all required keys for model_type.

    Example:
        >>> agent = create_agent(public_key=...)
        >>> records = [collect(agent, TelemetryCategory.CPU, 45.0) for _ in range(10)]
        >>> baseline = update_baseline(agent, TelemetryCategory.CPU,
        ...                            BaselineModel.MEAN_STD, 10, records)
        >>> baseline.sample_count
        10
    """
    # ─── P1: Agent exists ───
    if agent is None:
        raise AgentNotFound("agent must not be None")

    # ─── P2: window_size >= 10 (I7) ───
    if window_size < 10:
        raise InvalidWindowSize(
            f"window_size must be >= 10, got {window_size}"
        )

    # ─── P3: Enough telemetry records ───
    relevant = [r for r in telemetry_records if r.category == category]
    if len(relevant) < window_size:
        raise InsufficientTelemetry(
            f"need >= {window_size} records for category {category.value}, "
            f"got {len(relevant)}"
        )

    # Use the most recent `window_size` records
    recent = relevant[-window_size:]
    values = [r.value for r in recent]

    # ─── Compute parameters based on model_type ───
    parameters = _compute_parameters(model_type, values)

    # ─── Create or update baseline ───
    baseline_id = existing_baseline.baseline_id if existing_baseline else _random_hex()

    return Baseline(
        baseline_id=baseline_id,
        agent_id=agent.agent_id,
        category=category,
        model_type=model_type,
        parameters=parameters,
        computed_at=_now_iso(),
        sample_count=len(recent),
    )


def _compute_parameters(model_type: BaselineModel, values: list[float]) -> dict:
    """Compute model parameters from a list of values."""
    if model_type == BaselineModel.MEAN_STD:
        return {
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0.0,
        }

    elif model_type == BaselineModel.ZSCORE:
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        return {
            "mean": mean,
            "std": std,
            "z_scores": [(v - mean) / std if std > 0 else 0.0 for v in values],
        }

    elif model_type == BaselineModel.MOVING_AVERAGE:
        return {
            "window": len(values),
            "values": values,
            "moving_average": statistics.mean(values),
        }

    elif model_type == BaselineModel.SEASONAL:
        # Simple seasonal decomposition: period = 4 (quarterly)
        period = 4
        return {
            "period": period,
            "coefficients": _seasonal_coefficients(values, period),
            "mean": statistics.mean(values),
        }

    else:
        raise ValueError(f"Unknown model_type: {model_type}")


def _seasonal_coefficients(values: list[float], period: int) -> list[float]:
    """Compute simple seasonal coefficients."""
    if len(values) < period:
        return [1.0] * period
    overall_mean = statistics.mean(values)
    if overall_mean == 0:
        return [1.0] * period
    coefficients = []
    for i in range(period):
        seasonal_values = values[i::period]
        if seasonal_values:
            coefficients.append(statistics.mean(seasonal_values) / overall_mean)
        else:
            coefficients.append(1.0)
    return coefficients


# ═══════════════════════════════════════════════════════════════════════════
# Batch baseline helper
# ═══════════════════════════════════════════════════════════════════════════


def update_all_baselines(
    agent: Agent,
    telemetry_records: list[TelemetryRecord],
    model_type: BaselineModel = BaselineModel.MEAN_STD,
    window_size: int = 10,
) -> dict[TelemetryCategory, Baseline]:
    """
    Update baselines for all telemetry categories with sufficient data.

    Args:
        agent: The agent.
        telemetry_records: All telemetry records.
        model_type: Model type (default: mean_std).
        window_size: Window size (default: 10).

    Returns:
        Dict mapping category → Baseline (only for categories with enough data).
    """
    baselines: dict[TelemetryCategory, Baseline] = {}
    for category in TelemetryCategory:
        relevant = [r for r in telemetry_records if r.category == category]
        if len(relevant) >= window_size:
            try:
                baseline = update_baseline(
                    agent=agent,
                    category=category,
                    model_type=model_type,
                    window_size=window_size,
                    telemetry_records=telemetry_records,
                )
                baselines[category] = baseline
            except (InsufficientTelemetry, InvalidWindowSize):
                continue
    return baselines


# ═══════════════════════════════════════════════════════════════════════════
# Baseline registry
# ═══════════════════════════════════════════════════════════════════════════


class BaselineRegistry:
    """
    An in-memory registry of baselines.

    Used by the detection layer (Layer 2) to look up the baseline
    for a given (agent, category) pair.
    """

    def __init__(self) -> None:
        self._baselines: dict[tuple[str, TelemetryCategory], Baseline] = {}

    def put(self, baseline: Baseline) -> None:
        """Register a baseline."""
        key = (baseline.agent_id, baseline.category)
        self._baselines[key] = baseline

    def get(
        self, agent_id: str, category: TelemetryCategory
    ) -> Optional[Baseline]:
        """Get the baseline for an agent and category."""
        return self._baselines.get((agent_id, category))

    def get_all(self, agent_id: str) -> dict[TelemetryCategory, Baseline]:
        """Get all baselines for an agent."""
        return {
            cat: bl
            for (aid, cat), bl in self._baselines.items()
            if aid == agent_id
        }

    def has(self, agent_id: str, category: TelemetryCategory) -> bool:
        """Check if a baseline exists."""
        return (agent_id, category) in self._baselines


# ═══════════════════════════════════════════════════════════════════════════
# Module-level singleton (optional)
# ═══════════════════════════════════════════════════════════════════════════


default_baseline_registry = BaselineRegistry()
"""Default baseline registry (can be replaced per-test)."""
