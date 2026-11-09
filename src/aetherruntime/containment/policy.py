"""
AetherRuntime v2.0.0 — Containment: Policy (Layer 3)

This module implements Operation 4 (`contain`) from
docs/specification/02_operations.md.

The `contain` operation applies a containment policy to an anomalous agent,
restricting its resources without destroying forensic evidence.

Invariants enforced:
    - I11: level is one of four defined levels
    - I12: expiry > created_at
    - I13: restrictions contains all required keys for level
    - I31: policy references existing AnomalyAlert

Errors:
    - E11: AlertNotFound
    - E12: InvalidLevel
    - E13: ExpiryInPast
    - E14: AlreadyContained
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from ..models import (
    Agent,
    AgentStatus,
    AnomalyAlert,
    ContainmentLevel,
    ContainmentPolicy,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class AlertNotFound(Exception):
    """E11: Alert does not exist."""
    pass


class InvalidLevel(Exception):
    """E12: level not in {L1, L2, L3, L4}."""
    pass


class ExpiryInPast(Exception):
    """E13: expiry <= created_at."""
    pass


class AlreadyContained(Exception):
    """E14: Agent already contained at higher level."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Default restrictions for each level (I13)
# ═══════════════════════════════════════════════════════════════════════════


DEFAULT_RESTRICTIONS: dict[ContainmentLevel, dict] = {
    ContainmentLevel.L1_THROTTLE: {
        "cpu_percent": 10.0,
        "memory_mb": 512,
        "network": "allow",
        "filesystem": "read-write",
    },
    ContainmentLevel.L2_ISOLATE: {
        "cpu_percent": 10.0,
        "memory_mb": 256,
        "network": "deny",
        "filesystem": "read-only",
    },
    ContainmentLevel.L3_QUARANTINE: {
        "cpu_percent": 5.0,
        "memory_mb": 128,
        "network": "deny",
        "filesystem": "sandboxed",
    },
    ContainmentLevel.L4_FREEZE: {
        "cpu_percent": 0.0,
        "memory_mb": 0,
        "network": "deny",
        "filesystem": "frozen",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# Operation 4 — contain
# ═══════════════════════════════════════════════════════════════════════════


def contain(
    agent: Agent,
    alert: AnomalyAlert,
    level: ContainmentLevel,
    expiry_seconds: int = 300,
    restrictions: Optional[dict] = None,
    existing_policy: Optional[ContainmentPolicy] = None,
) -> ContainmentPolicy:
    """
    Apply a containment policy to an anomalous agent (Operation 4).

    Args:
        agent: The agent to contain.
        alert: The AnomalyAlert that triggered containment.
        level: Containment level (L1, L2, L3, L4).
        expiry_seconds: How long containment lasts (default 300 = 5 min).
        restrictions: Optional custom restrictions. Defaults to DEFAULT_RESTRICTIONS[level].
        existing_policy: Optional existing policy (for re-containment).

    Returns:
        A new ContainmentPolicy.

    Raises:
        AlertNotFound: If alert is None.
        InvalidLevel: If level is not a valid ContainmentLevel.
        ExpiryInPast: If expiry <= created_at.
        AlreadyContained: If agent is already contained at same/higher level.

    Invariants:
        I11: level is valid.
        I12: expiry > created_at.
        I13: restrictions contains all required keys.
        I31: policy references existing alert.

    Example:
        >>> policy = contain(agent, alert, ContainmentLevel.L2_ISOLATE)
        >>> policy.level
        <ContainmentLevel.L2_ISOLATE: 'L2_isolate'>
    """
    # ─── E11: Alert must exist ───
    if alert is None:
        raise AlertNotFound("alert must not be None")

    # ─── E12: Level must be valid (I11) ───
    if not isinstance(level, ContainmentLevel):
        raise InvalidLevel(f"level must be ContainmentLevel, got {type(level)}")

    # ─── E14: Agent not already contained at higher level ───
    if agent.status == AgentStatus.CONTAINED and existing_policy is not None:
        if _level_rank(level) <= _level_rank(existing_policy.level):
            raise AlreadyContained(
                f"Agent {agent.agent_id} already contained at "
                f"{existing_policy.level.value} (>= {level.value})"
            )

    # ─── I12: expiry > created_at ───
    now = datetime.now(timezone.utc)
    created_at = now.isoformat()
    expiry_dt = now + timedelta(seconds=expiry_seconds)
    expiry = expiry_dt.isoformat()

    if expiry_dt <= now:
        raise ExpiryInPast(f"expiry must be > created_at")

    # ─── I13: restrictions contains required keys ───
    if restrictions is None:
        restrictions = dict(DEFAULT_RESTRICTIONS[level])
    required = {"cpu_percent", "memory_mb", "network", "filesystem"}
    missing = required - set(restrictions.keys())
    if missing:
        raise ValueError(f"restrictions missing keys: {missing}")

    # ─── Q1: Create ContainmentPolicy ───
    policy = ContainmentPolicy(
        policy_id=_random_hex(),
        agent_id=agent.agent_id,
        alert_id=alert.alert_id,
        level=level,
        restrictions=restrictions,
        expiry=expiry,
        created_at=created_at,
    )

    # ─── Q3: Update agent status ───
    agent.status = AgentStatus.CONTAINED

    return policy


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _level_rank(level: ContainmentLevel) -> int:
    """Return a numeric rank for a containment level (higher = stricter)."""
    ranks = {
        ContainmentLevel.L1_THROTTLE: 1,
        ContainmentLevel.L2_ISOLATE: 2,
        ContainmentLevel.L3_QUARANTINE: 3,
        ContainmentLevel.L4_FREEZE: 4,
    }
    return ranks[level]


def release(
    agent: Agent,
    policy: ContainmentPolicy,
) -> None:
    """
    Release an agent from containment (reversal).

    Args:
        agent: The agent to release.
        policy: The policy to release.

    Invariants:
        - X5: Containment policy is reversible.
    """
    if agent.agent_id != policy.agent_id:
        raise ValueError(
            f"agent {agent.agent_id} does not match policy agent {policy.agent_id}"
        )
    agent.status = AgentStatus.RUNNING


def is_expired(policy: ContainmentPolicy) -> bool:
    """Check if a containment policy has expired."""
    now = datetime.now(timezone.utc)
    expiry_dt = datetime.fromisoformat(policy.expiry.replace("Z", "+00:00"))
    return now >= expiry_dt


# ═══════════════════════════════════════════════════════════════════════════
# Containment registry
# ═══════════════════════════════════════════════════════════════════════════


class ContainmentRegistry:
    """An in-memory registry of containment policies."""

    def __init__(self) -> None:
        self._policies: dict[str, ContainmentPolicy] = {}
        self._by_agent: dict[str, list[ContainmentPolicy]] = {}

    def put(self, policy: ContainmentPolicy) -> None:
        """Register a containment policy."""
        if policy.policy_id in self._policies:
            raise ValueError(f"policy_id {policy.policy_id} already registered")
        self._policies[policy.policy_id] = policy
        self._by_agent.setdefault(policy.agent_id, []).append(policy)

    def get(self, policy_id: str) -> Optional[ContainmentPolicy]:
        """Get a policy by ID."""
        return self._policies.get(policy_id)

    def get_by_agent(self, agent_id: str) -> list[ContainmentPolicy]:
        """Get all policies for an agent."""
        return list(self._by_agent.get(agent_id, []))

    def active_for_agent(self, agent_id: str) -> list[ContainmentPolicy]:
        """Get all active (non-expired) policies for an agent."""
        return [p for p in self.get_by_agent(agent_id) if not is_expired(p)]

    def count(self) -> int:
        """Count all policies."""
        return len(self._policies)

    def clear(self) -> None:
        """Clear all policies."""
        self._policies.clear()
        self._by_agent.clear()
