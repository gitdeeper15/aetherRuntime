"""AetherRuntime — Detection layer (Layer 2)."""

from .classifier import (
    detect,
    detect_batch,
    summarize_detection,
    DetectionSummary,
    TelemetryNotFound,
    BaselineNotFound,
    NonDeterministic,
)
from .alert import (
    AlertRegistry,
    AlertStats,
    validate_alert_against_telemetry,
    filter_alerts_by_confidence,
    group_alerts_by_agent,
    latest_alert_for_agent,
)

__all__ = [
    "detect",
    "detect_batch",
    "summarize_detection",
    "DetectionSummary",
    "TelemetryNotFound",
    "BaselineNotFound",
    "NonDeterministic",
    "AlertRegistry",
    "AlertStats",
    "validate_alert_against_telemetry",
    "filter_alerts_by_confidence",
    "group_alerts_by_agent",
    "latest_alert_for_agent",
]
