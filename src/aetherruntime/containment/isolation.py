"""
AetherRuntime v2.0.0 — Containment: Isolation (Layer 3)

This module implements the isolation mechanisms for containment.
While `policy.py` defines the containment policy (what to restrict),
this module enforces it (how to restrict).

Key properties:
    - Isolation is reversible (X5).
    - Isolation preserves forensic evidence (no data destruction).
    - Isolation applies resource limits per level.

Invariants enforced:
    - X5: containment is reversible
    - I13: restrictions are applied correctly
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from ..models import (
    Agent,
    AgentStatus,
    ContainmentLevel,
    ContainmentPolicy,
)


# ═══════════════════════════════════════════════════════════════════════════
# Isolation state
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class IsolationState:
    """
    The current isolation state of an agent.

    Fields:
        - agent_id: The isolated agent.
        - level: The current containment level.
        - restrictions: The active restrictions.
        - applied_at: When isolation was applied.
        - released_at: When isolation was released (None if active).
    """
    agent_id: str
    level: ContainmentLevel
    restrictions: dict
    applied_at: str
    released_at: Optional[str] = None

    @property
    def is_active(self) -> bool:
        """Check if isolation is currently active."""
        return self.released_at is None

    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {
            "agent_id": self.agent_id,
            "level": self.level.value,
            "restrictions": self.restrictions,
            "applied_at": self.applied_at,
            "released_at": self.released_at,
            "is_active": self.is_active,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Isolation manager
# ═══════════════════════════════════════════════════════════════════════════


class IsolationManager:
    """
    Manages the isolation state of agents.

    Applies containment policies by:
        1. Recording the isolation state.
        2. Enforcing resource restrictions (in simulation: tracked only).
        3. Providing query methods for the current state.
    """

    def __init__(self) -> None:
        self._states: dict[str, IsolationState] = {}
        self._history: list[IsolationState] = []

    def apply(self, policy: ContainmentPolicy) -> IsolationState:
        """
        Apply a containment policy (enforce isolation).

        Args:
            policy: The ContainmentPolicy to apply.

        Returns:
            The IsolationState after application.
        """
        if policy.agent_id in self._states and self._states[policy.agent_id].is_active:
            raise ValueError(
                f"Agent {policy.agent_id} already isolated at "
                f"{self._states[policy.agent_id].level.value}"
            )

        state = IsolationState(
            agent_id=policy.agent_id,
            level=policy.level,
            restrictions=dict(policy.restrictions),
            applied_at=datetime.now(timezone.utc).isoformat(),
        )
        self._states[policy.agent_id] = state
        self._history.append(state)
        return state

    def release(self, agent_id: str) -> Optional[IsolationState]:
        """
        Release an agent from isolation.

        Args:
            agent_id: The agent to release.

        Returns:
            The IsolationState after release, or None if not isolated.
        """
        state = self._states.get(agent_id)
        if state is None or not state.is_active:
            return None
        state.released_at = datetime.now(timezone.utc).isoformat()
        self._history.append(state)
        return state

    def get(self, agent_id: str) -> Optional[IsolationState]:
        """Get the current isolation state for an agent."""
        return self._states.get(agent_id)

    def is_isolated(self, agent_id: str) -> bool:
        """Check if an agent is currently isolated."""
        state = self._states.get(agent_id)
        return state is not None and state.is_active

    def active_agents(self) -> list[str]:
        """Get all currently isolated agent IDs."""
        return [aid for aid, st in self._states.items() if st.is_active]

    def history(self) -> list[IsolationState]:
        """Get the full history of isolation states."""
        return list(self._history)

    def count_active(self) -> int:
        """Count currently isolated agents."""
        return len(self.active_agents())

    def clear(self) -> None:
        """Clear all isolation states."""
        self._states.clear()
        self._history.clear()


# ═══════════════════════════════════════════════════════════════════════════
# Resource enforcement (simulated)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ResourceSnapshot:
    """A snapshot of an agent's resource usage (for enforcement)."""
    cpu_percent: float
    memory_mb: float
    network_requests: int = 0
    filesystem_writes: int = 0


def enforce_restrictions(
    usage: ResourceSnapshot,
    restrictions: dict,
) -> tuple[ResourceSnapshot, list[str]]:
    """
    Enforce resource restrictions on a snapshot.

    Args:
        usage: The agent's current resource usage.
        restrictions: The containment restrictions.

    Returns:
        (adjusted_usage, violations):
            - adjusted_usage: The usage after applying restrictions.
            - violations: List of violations (empty if none).
    """
    adjusted = ResourceSnapshot(
        cpu_percent=usage.cpu_percent,
        memory_mb=usage.memory_mb,
        network_requests=usage.network_requests,
        filesystem_writes=usage.filesystem_writes,
    )
    violations: list[str] = []

    # CPU limit
    cpu_limit = restrictions.get("cpu_percent")
    if cpu_limit is not None and adjusted.cpu_percent > cpu_limit:
        violations.append(
            f"CPU {adjusted.cpu_percent:.1f}% > {cpu_limit}%"
        )
        adjusted.cpu_percent = cpu_limit

    # Memory limit
    mem_limit = restrictions.get("memory_mb")
    if mem_limit is not None and adjusted.memory_mb > mem_limit:
        violations.append(
            f"Memory {adjusted.memory_mb:.0f}MB > {mem_limit}MB"
        )
        adjusted.memory_mb = mem_limit

    # Network restriction
    net_policy = restrictions.get("network")
    if net_policy == "deny" and adjusted.network_requests > 0:
        violations.append(
            f"Network denied, {adjusted.network_requests} requests blocked"
        )
        adjusted.network_requests = 0

    # Filesystem restriction
    fs_policy = restrictions.get("filesystem")
    if fs_policy in ("read-only", "sandboxed", "frozen"):
        if adjusted.filesystem_writes > 0:
            violations.append(
                f"Filesystem {fs_policy}, {adjusted.filesystem_writes} writes blocked"
            )
            adjusted.filesystem_writes = 0

    return adjusted, violations


# ═══════════════════════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════════════════════


def apply_isolation(
    manager: IsolationManager,
    policy: ContainmentPolicy,
) -> IsolationState:
    """Convenience wrapper: apply isolation via manager."""
    return manager.apply(policy)


def release_isolation(
    manager: IsolationManager,
    agent_id: str,
) -> Optional[IsolationState]:
    """Convenience wrapper: release isolation via manager."""
    return manager.release(agent_id)
