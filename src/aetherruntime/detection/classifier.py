"""
AetherRuntime v2.0.0 — Detection: Anomaly Classifier (Layer 2)

This module implements Operation 3 (`detect`) from
docs/specification/02_operations.md.

The `detect` operation compares a telemetry record against the baseline
and returns an AnomalyAlert if the record deviates beyond the threshold.

Key property (Proposition 1): The verdict is a deterministic function of
the telemetry record and the baseline. No non-local state is consulted.

Invariants enforced:
    - I9: confidence in [0.0, 1.0]
    - I10: telemetry_id refers to existing TelemetryRecord
    - I30: alert references existing Agent and TelemetryRecord
    - O3: detect is deterministic (Proposition 1)
    - X3: verdict reproducible from local state

Errors:
    - E8: TelemetryNotFound
    - E9: BaselineNotFound
    - E10: NonDeterministic (structural; not raised at runtime)
"""

from __future__ import annotations

import math
from typing import Optional

from ..models import (
    AnomalyAlert,
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


class TelemetryNotFound(Exception):
    """E8: TelemetryRecord does not exist."""
    pass


class BaselineNotFound(Exception):
    """E9: No baseline for the (agent, category) pair."""
    pass


class NonDeterministic(Exception):
    """E10: Anomaly predicate depends on non-local state."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Anomaly predicates
# ═══════════════════════════════════════════════════════════════════════════


def _anomaly_predicate(
    telemetry: TelemetryRecord,
    baseline: Baseline,
    threshold: float,
) -> tuple[bool, float]:
    """
    Pure function: (telemetry, baseline, threshold) → (is_anomalous, confidence).

    This is the core of Proposition 1. The predicate reads ONLY from
    the telemetry record and the baseline. No global state.

    Args:
        telemetry: The telemetry record to evaluate.
        baseline: The baseline model for comparison.
        threshold: Anomaly threshold (Θ_max, typically 2.0–3.0 for z-score).

    Returns:
        (is_anomalous, confidence):
            - is_anomalous: True if the value is anomalous.
            - confidence: [0.0, 1.0] how confident the classifier is.
    """
    value = telemetry.value
    params = baseline.parameters
    model = baseline.model_type

    # ─── Mean/std model ───
    if model in (BaselineModel.MEAN_STD, BaselineModel.ZSCORE):
        mean = params["mean"]
        std = params["std"]
        if std == 0:
            # Degenerate case: no variance. Any deviation is anomalous.
            deviation = abs(value - mean)
            if deviation == 0:
                return (False, 1.0)
            return (True, 1.0)
        z = (value - mean) / std
        is_anomalous = abs(z) > threshold
        # Confidence: sigmoid of |z| - threshold
        confidence = _sigmoid(abs(z) - threshold)
        return (is_anomalous, confidence)

    # ─── Moving average model ───
    elif model == BaselineModel.MOVING_AVERAGE:
        moving_avg = params["moving_average"]
        window = params["window"]
        if window == 0 or moving_avg == 0:
            return (False, 0.0)
        deviation = abs(value - moving_avg) / abs(moving_avg)
        is_anomalous = deviation > threshold * 0.1  # 10% * threshold
        confidence = _sigmoid(deviation * 10 - threshold)
        return (is_anomalous, confidence)

    # ─── Seasonal model ───
    elif model == BaselineModel.SEASONAL:
        period = params["period"]
        coeffs = params["coefficients"]
        mean = params["mean"]
        if not coeffs or mean == 0:
            return (False, 0.0)
        # Use the mean coefficient for a simple check
        avg_coeff = sum(coeffs) / len(coeffs)
        expected = mean * avg_coeff
        deviation = abs(value - expected) / abs(expected) if expected != 0 else 0.0
        is_anomalous = deviation > threshold * 0.1
        confidence = _sigmoid(deviation * 10 - threshold)
        return (is_anomalous, confidence)

    else:
        raise ValueError(f"Unknown baseline model: {model}")


def _sigmoid(x: float) -> float:
    """Sigmoid function: 1 / (1 + exp(-x))."""
    if x < -500:
        return 0.0
    if x > 500:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


# ═══════════════════════════════════════════════════════════════════════════
# Operation 3 — detect
# ═══════════════════════════════════════════════════════════════════════════


def detect(
    telemetry: TelemetryRecord,
    baseline: Optional[Baseline] = None,
    threshold: float = 2.0,
) -> Optional[AnomalyAlert]:
    """
    Compare a telemetry record against the baseline (Operation 3).

    Args:
        telemetry: The telemetry record to evaluate.
        baseline: The baseline to compare against. If None, raises BaselineNotFound.
        threshold: Anomaly threshold (Θ_max). Default 2.0 (2-sigma for z-score).

    Returns:
        AnomalyAlert if anomalous, None otherwise.

    Raises:
        TelemetryNotFound: If telemetry is None.
        BaselineNotFound: If baseline is None.

    Invariants:
        I9: confidence in [0.0, 1.0].
        I10: telemetry_id refers to the input telemetry.
        I30: alert references agent_id from telemetry.
        O3: deterministic (Proposition 1).
        X3: reproducible.

    Example:
        >>> alert = detect(telemetry, baseline, threshold=2.0)
        >>> if alert:
        ...     print(f"Anomaly! confidence={alert.confidence:.2f}")
    """
    # ─── E8: Telemetry must exist ───
    if telemetry is None:
        raise TelemetryNotFound("telemetry must not be None")

    # ─── E9: Baseline must exist ───
    if baseline is None:
        raise BaselineNotFound(
            f"No baseline for agent {telemetry.agent_id} "
            f"category {telemetry.category.value}"
        )

    # ─── Verify categories match ───
    if telemetry.category != baseline.category:
        raise ValueError(
            f"category mismatch: telemetry={telemetry.category.value}, "
            f"baseline={baseline.category.value}"
        )

    # ─── O3/X3: Deterministic predicate (Proposition 1) ───
    is_anomalous, confidence = _anomaly_predicate(telemetry, baseline, threshold)

    if not is_anomalous:
        return None

    # ─── Q1: Create AnomalyAlert ───
    return AnomalyAlert(
        alert_id=_random_hex(),
        agent_id=telemetry.agent_id,
        telemetry_id=telemetry.telemetry_id,
        baseline_id=baseline.baseline_id,
        confidence=confidence,
        reason=f"value {telemetry.value:.2f} deviates from baseline "
               f"({baseline.model_type.value})",
        timestamp=_now_iso(),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Batch detection
# ═══════════════════════════════════════════════════════════════════════════


def detect_batch(
    telemetry_records: list[TelemetryRecord],
    baselines: dict[TelemetryCategory, Baseline],
    threshold: float = 2.0,
) -> list[AnomalyAlert]:
    """
    Detect anomalies in multiple telemetry records.

    Args:
        telemetry_records: List of telemetry records.
        baselines: Dict mapping category → Baseline.
        threshold: Anomaly threshold.

    Returns:
        List of AnomalyAlert (may be empty).
    """
    alerts: list[AnomalyAlert] = []
    for record in telemetry_records:
        baseline = baselines.get(record.category)
        if baseline is None:
            continue
        alert = detect(record, baseline, threshold)
        if alert is not None:
            alerts.append(alert)
    return alerts


# ═══════════════════════════════════════════════════════════════════════════
# Detection summary
# ═══════════════════════════════════════════════════════════════════════════


class DetectionSummary:
    """Aggregated detection statistics."""

    def __init__(
        self,
        total: int,
        alerts: list[AnomalyAlert],
    ) -> None:
        self.total = total
        self.alerts = alerts

    @property
    def n_anomalies(self) -> int:
        return len(self.alerts)

    @property
    def anomaly_rate(self) -> float:
        return self.n_anomalies / self.total if self.total > 0 else 0.0

    @property
    def mean_confidence(self) -> float:
        if not self.alerts:
            return 0.0
        return sum(a.confidence for a in self.alerts) / len(self.alerts)

    def __repr__(self) -> str:
        return (
            f"DetectionSummary(total={self.total}, "
            f"anomalies={self.n_anomalies}, "
            f"rate={self.anomaly_rate:.3f})"
        )


def summarize_detection(
    telemetry_records: list[TelemetryRecord],
    baselines: dict[TelemetryCategory, Baseline],
    threshold: float = 2.0,
) -> DetectionSummary:
    """Run detection and return a summary."""
    alerts = detect_batch(telemetry_records, baselines, threshold)
    return DetectionSummary(total=len(telemetry_records), alerts=alerts)
