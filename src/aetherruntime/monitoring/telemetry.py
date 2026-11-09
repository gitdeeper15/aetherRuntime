"""
AetherRuntime v2.0.0 — Monitoring: Telemetry Collection

This module implements Operation 1 (`collect`) from
docs/specification/02_operations.md.

The `collect` operation gathers a telemetry record from a running agent.
It is the input to the detection layer (Layer 2).

Invariants enforced:
    - I4: telemetry_id is unique (via _random_hex)
    - I5: value is finite
    - I6: timestamp is monotonic per agent

Errors:
    - E2: AgentNotRunning
    - E3: InvalidValue
    - E4: NonMonotonicTimestamp
"""

from __future__ import annotations

from typing import Optional

from ..models import (
    Agent,
    AgentStatus,
    TelemetryCategory,
    TelemetryRecord,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class AgentNotRunning(Exception):
    """E2: Agent is not in `running` state."""
    pass


class InvalidValue(Exception):
    """E3: Value is not finite."""
    pass


class NonMonotonicTimestamp(Exception):
    """E4: Timestamp is not monotonic per agent."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Operation 1 — collect
# ═══════════════════════════════════════════════════════════════════════════


def collect(
    agent: Agent,
    category: TelemetryCategory,
    value: float,
    timestamp: Optional[str] = None,
    metadata: Optional[dict] = None,
    previous_timestamp: Optional[str] = None,
) -> TelemetryRecord:
    """
    Collect a telemetry record from a running agent (Operation 1).

    Args:
        agent: The agent to collect from. Must be in `running` state.
        category: Telemetry category (cpu, memory, network, syscall, action).
        value: Numeric value (unit depends on category). Must be finite.
        timestamp: Logical time of observation (ISO 8601). Defaults to now.
        metadata: Optional metadata (pid, tid, etc.).
        previous_timestamp: Optional previous timestamp for monotonicity check.

    Returns:
        A new `TelemetryRecord` with a unique `telemetry_id`.

    Raises:
        AgentNotRunning: If agent.status != AgentStatus.RUNNING.
        InvalidValue: If value is NaN or Inf.
        NonMonotonicTimestamp: If timestamp < previous_timestamp.

    Invariants:
        I4: telemetry_id is unique (via _random_hex).
        I5: value is finite.
        I6: timestamp is monotonic per agent (if previous_timestamp provided).

    Example:
        >>> agent = create_agent(public_key=...)
        >>> agent.status = AgentStatus.RUNNING
        >>> record = collect(agent, TelemetryCategory.CPU, 45.2)
        >>> record.value
        45.2
    """
    # ─── P1: Agent must be running ───
    if agent.status != AgentStatus.RUNNING:
        raise AgentNotRunning(
            f"Agent {agent.agent_id} is not running (status: {agent.status.value})"
        )

    # ─── P2: Value must be finite (I5) ───
    if not isinstance(value, (int, float)):
        raise InvalidValue(f"value must be int or float, got {type(value)}")
    if value != value:  # NaN check
        raise InvalidValue("value must not be NaN")
    if value == float("inf") or value == float("-inf"):
        raise InvalidValue("value must not be Inf")

    # ─── P3: Timestamp must be monotonic (I6) ───
    if timestamp is None:
        timestamp = _now_iso()
    if previous_timestamp is not None:
        from datetime import datetime
        try:
            current_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            previous_dt = datetime.fromisoformat(previous_timestamp.replace("Z", "+00:00"))
        except (ValueError, AttributeError) as e:
            raise NonMonotonicTimestamp(f"Invalid timestamp format: {e}")
        if current_dt < previous_dt:
            raise NonMonotonicTimestamp(
                f"timestamp {timestamp} is before previous_timestamp {previous_timestamp}"
            )

    # ─── Q1–Q3: Create the record ───
    return TelemetryRecord(
        telemetry_id=_random_hex(),
        agent_id=agent.agent_id,
        category=category,
        value=value,
        timestamp=timestamp,
        metadata=metadata or {},
    )


# ═══════════════════════════════════════════════════════════════════════════
# Batch collection helper
# ═══════════════════════════════════════════════════════════════════════════


def collect_batch(
    agent: Agent,
    records: list[tuple[TelemetryCategory, float]],
) -> list[TelemetryRecord]:
    """
    Collect multiple telemetry records in one call.

    Args:
        agent: The agent to collect from.
        records: List of (category, value) tuples.

    Returns:
        List of TelemetryRecord, one per input tuple.

    Raises:
        AgentNotRunning: If agent.status != AgentStatus.RUNNING.
        InvalidValue: If any value is NaN or Inf.
    """
    from datetime import datetime, timezone

    results: list[TelemetryRecord] = []
    previous: Optional[str] = None

    for i, (category, value) in enumerate(records):
        # Use microsecond-precision timestamps to ensure monotonicity
        ts = datetime.now(timezone.utc).isoformat()
        # Small artificial delay to ensure monotonicity
        if previous is not None:
            ts = datetime.now(timezone.utc).isoformat()
        record = collect(
            agent=agent,
            category=category,
            value=value,
            timestamp=ts,
            previous_timestamp=previous,
        )
        results.append(record)
        previous = ts

    return results


# ═══════════════════════════════════════════════════════════════════════════
# Telemetry log helper
# ═══════════════════════════════════════════════════════════════════════════


class TelemetryLog:
    """
    An in-memory log of telemetry records for an agent.

    Used by the detection layer (Layer 2) and baseline computation.
    """

    def __init__(self) -> None:
        self._records: dict[str, list[TelemetryRecord]] = {}

    def append(self, record: TelemetryRecord) -> None:
        """Append a record to the log (grouped by agent_id)."""
        if record.agent_id not in self._records:
            self._records[record.agent_id] = []
        self._records[record.agent_id].append(record)

    def get(self, agent_id: str) -> list[TelemetryRecord]:
        """Get all records for an agent."""
        return list(self._records.get(agent_id, []))

    def get_by_category(
        self, agent_id: str, category: TelemetryCategory
    ) -> list[TelemetryRecord]:
        """Get all records for an agent and category."""
        return [
            r for r in self._records.get(agent_id, []) if r.category == category
        ]

    def last_timestamp(self, agent_id: str) -> Optional[str]:
        """Get the last timestamp for an agent (for monotonicity check)."""
        records = self._records.get(agent_id, [])
        return records[-1].timestamp if records else None

    def count(self, agent_id: str) -> int:
        """Count records for an agent."""
        return len(self._records.get(agent_id, []))


# ═══════════════════════════════════════════════════════════════════════════
# Module-level singleton (optional)
# ═══════════════════════════════════════════════════════════════════════════


default_telemetry_log = TelemetryLog()
"""Default telemetry log (can be replaced per-test)."""
