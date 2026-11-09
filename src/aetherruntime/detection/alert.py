"""
AetherRuntime v2.0.0 — Detection: Alert Management (Layer 2)

This module provides an in-memory registry for AnomalyAlerts and
helpers for querying them.

The alert registry is used by the containment layer (Layer 3) to
look up alerts that trigger containment policies.

Invariants enforced:
    - I9: confidence in [0.0, 1.0]
    - I10: telemetry_id refers to existing TelemetryRecord
    - I30: alert references existing Agent and TelemetryRecord
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

from ..models import (
    Agent,
    AnomalyAlert,
    TelemetryRecord,
)


# ═══════════════════════════════════════════════════════════════════════════
# Alert registry
# ═══════════════════════════════════════════════════════════════════════════


class AlertRegistry:
    """
    An in-memory registry of AnomalyAlerts.

    Used by the containment layer to look up alerts that trigger
    containment policies.

    Indexes:
        - by_agent: dict[agent_id → list[AnomalyAlert]]
        - by_telemetry: dict[telemetry_id → AnomalyAlert]
        - by_id: dict[alert_id → AnomalyAlert]
    """

    def __init__(self) -> None:
        self._by_agent: dict[str, list[AnomalyAlert]] = defaultdict(list)
        self._by_telemetry: dict[str, AnomalyAlert] = {}
        self._by_id: dict[str, AnomalyAlert] = {}

    def put(self, alert: AnomalyAlert) -> None:
        """Register an alert."""
        if alert.alert_id in self._by_id:
            raise ValueError(f"alert_id {alert.alert_id} already registered")
        self._by_agent[alert.agent_id].append(alert)
        self._by_telemetry[alert.telemetry_id] = alert
        self._by_id[alert.alert_id] = alert

    def get(self, alert_id: str) -> Optional[AnomalyAlert]:
        """Get an alert by ID."""
        return self._by_id.get(alert_id)

    def get_by_telemetry(self, telemetry_id: str) -> Optional[AnomalyAlert]:
        """Get the alert for a telemetry record."""
        return self._by_telemetry.get(telemetry_id)

    def get_by_agent(self, agent_id: str) -> list[AnomalyAlert]:
        """Get all alerts for an agent."""
        return list(self._by_agent.get(agent_id, []))

    def get_unresolved(self, agent_id: str) -> list[AnomalyAlert]:
        """Get all alerts for an agent (alias for get_by_agent)."""
        return self.get_by_agent(agent_id)

    def count(self) -> int:
        """Count all alerts."""
        return len(self._by_id)

    def count_by_agent(self, agent_id: str) -> int:
        """Count alerts for an agent."""
        return len(self._by_agent.get(agent_id, []))

    def clear(self) -> None:
        """Clear all alerts."""
        self._by_agent.clear()
        self._by_telemetry.clear()
        self._by_id.clear()


# ═══════════════════════════════════════════════════════════════════════════
# Alert helpers
# ═══════════════════════════════════════════════════════════════════════════


def validate_alert_against_telemetry(
    alert: AnomalyAlert,
    telemetry: TelemetryRecord,
) -> bool:
    """
    Validate that an alert is consistent with a telemetry record.

    Returns:
        True if valid, False otherwise.
    """
    if alert.telemetry_id != telemetry.telemetry_id:
        return False
    if alert.agent_id != telemetry.agent_id:
        return False
    if not (0.0 <= alert.confidence <= 1.0):
        return False
    return True


def filter_alerts_by_confidence(
    alerts: list[AnomalyAlert],
    min_confidence: float = 0.5,
) -> list[AnomalyAlert]:
    """Filter alerts by minimum confidence."""
    return [a for a in alerts if a.confidence >= min_confidence]


def group_alerts_by_agent(
    alerts: list[AnomalyAlert],
) -> dict[str, list[AnomalyAlert]]:
    """Group alerts by agent_id."""
    result: dict[str, list[AnomalyAlert]] = defaultdict(list)
    for alert in alerts:
        result[alert.agent_id].append(alert)
    return dict(result)


def latest_alert_for_agent(
    alerts: list[AnomalyAlert],
    agent_id: str,
) -> Optional[AnomalyAlert]:
    """Return the latest alert for an agent (by timestamp)."""
    agent_alerts = [a for a in alerts if a.agent_id == agent_id]
    if not agent_alerts:
        return None
    from datetime import datetime
    agent_alerts.sort(
        key=lambda a: datetime.fromisoformat(a.timestamp.replace("Z", "+00:00")),
        reverse=True,
    )
    return agent_alerts[0]


# ═══════════════════════════════════════════════════════════════════════════
# Alert statistics
# ═══════════════════════════════════════════════════════════════════════════


class AlertStats:
    """Aggregated statistics for a list of alerts."""

    def __init__(self, alerts: list[AnomalyAlert]) -> None:
        self.alerts = alerts

    @property
    def total(self) -> int:
        return len(self.alerts)

    @property
    def mean_confidence(self) -> float:
        if not self.alerts:
            return 0.0
        return sum(a.confidence for a in self.alerts) / len(self.alerts)

    @property
    def max_confidence(self) -> float:
        if not self.alerts:
            return 0.0
        return max(a.confidence for a in self.alerts)

    @property
    def min_confidence(self) -> float:
        if not self.alerts:
            return 0.0
        return min(a.confidence for a in self.alerts)

    @property
    def unique_agents(self) -> int:
        return len(set(a.agent_id for a in self.alerts))

    def __repr__(self) -> str:
        return (
            f"AlertStats(total={self.total}, "
            f"mean_confidence={self.mean_confidence:.3f}, "
            f"unique_agents={self.unique_agents})"
        )
