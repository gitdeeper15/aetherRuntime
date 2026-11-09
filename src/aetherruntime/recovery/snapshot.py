"""
AetherRuntime v2.0.0 — Recovery: Snapshot (Layer 5)

This module provides snapshot management for recovery.
A snapshot is a point-in-time capture of an agent's state.

Key properties:
    - Content-addressed (SHA-256 hash).
    - Stored in AetherGit (simulated).
    - Used by `recover` (see `replay.py`).

Invariants enforced:
    - I24: hash matches SHA-256 of state
    - I25: stored_at refers to an existing AetherGit record
    - I26: snapshot_id is unique
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Optional

from ..models import (
    Agent,
    Snapshot,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class SnapshotNotFound(Exception):
    """Snapshot does not exist."""
    pass


class HashMismatch(Exception):
    """I24: hash does not match SHA-256 of state."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Snapshot creation
# ═══════════════════════════════════════════════════════════════════════════


def create_snapshot(
    agent: Agent,
    state: bytes,
    stored_at: Optional[str] = None,
) -> Snapshot:
    """
    Create a snapshot of an agent's state.

    Args:
        agent: The agent to snapshot.
        state: Serialized agent state (bytes).
        stored_at: Storage location (AetherGit ref). Defaults to a generated ref.

    Returns:
        A new Snapshot with a valid SHA-256 hash.

    Raises:
        ValueError: If state is empty or agent is None.

    Invariants:
        I24: hash matches SHA-256 of state.
        I25: stored_at refers to a valid location.
        I26: snapshot_id is unique.

    Example:
        >>> snapshot = create_snapshot(agent, b"state data")
        >>> len(snapshot.hash)
        64
    """
    if agent is None:
        raise ValueError("agent must not be None")
    if not state:
        raise ValueError("state must not be empty")

    # ─── I24: Compute SHA-256 hash ───
    state_hash = hashlib.sha256(state).hexdigest()

    # ─── I25: Default storage location ───
    if stored_at is None:
        stored_at = f"aethergit://snapshots/{state_hash[:16]}"

    # ─── I26: Generate unique snapshot_id ───
    snapshot_id = _random_hex()

    return Snapshot(
        snapshot_id=snapshot_id,
        agent_id=agent.agent_id,
        state=state,
        hash=state_hash,
        timestamp=_now_iso(),
        stored_at=stored_at,
    )


def verify_snapshot(snapshot: Snapshot) -> bool:
    """
    Verify that a snapshot's hash matches its state (I24).

    Args:
        snapshot: The Snapshot to verify.

    Returns:
        True if hash matches, False otherwise.
    """
    expected = hashlib.sha256(snapshot.state).hexdigest()
    return expected == snapshot.hash


# ═══════════════════════════════════════════════════════════════════════════
# Snapshot registry
# ═══════════════════════════════════════════════════════════════════════════


class SnapshotRegistry:
    """
    An in-memory registry of snapshots.

    Indexes:
        - by_id: dict[snapshot_id → Snapshot]
        - by_agent: dict[agent_id → list[Snapshot]]
    """

    def __init__(self) -> None:
        self._by_id: dict[str, Snapshot] = {}
        self._by_agent: dict[str, list[Snapshot]] = {}

    def put(self, snapshot: Snapshot) -> None:
        """Register a snapshot (I26: snapshot_id unique)."""
        if snapshot.snapshot_id in self._by_id:
            raise ValueError(
                f"snapshot_id {snapshot.snapshot_id} already registered"
            )
        # I24: verify hash before storing
        if not verify_snapshot(snapshot):
            raise HashMismatch(
                f"snapshot {snapshot.snapshot_id} has invalid hash"
            )
        self._by_id[snapshot.snapshot_id] = snapshot
        self._by_agent.setdefault(snapshot.agent_id, []).append(snapshot)

    def get(self, snapshot_id: str) -> Optional[Snapshot]:
        """Get a snapshot by ID."""
        return self._by_id.get(snapshot_id)

    def get_by_agent(self, agent_id: str) -> list[Snapshot]:
        """Get all snapshots for an agent."""
        return list(self._by_agent.get(agent_id, []))

    def latest_for_agent(self, agent_id: str) -> Optional[Snapshot]:
        """Get the latest snapshot for an agent."""
        snapshots = self.get_by_agent(agent_id)
        if not snapshots:
            return None
        snapshots.sort(
            key=lambda s: datetime.fromisoformat(
                s.timestamp.replace("Z", "+00:00")
            ),
            reverse=True,
        )
        return snapshots[0]

    def count(self) -> int:
        """Count all snapshots."""
        return len(self._by_id)

    def count_by_agent(self, agent_id: str) -> int:
        """Count snapshots for an agent."""
        return len(self._by_agent.get(agent_id, []))

    def clear(self) -> None:
        """Clear all snapshots."""
        self._by_id.clear()
        self._by_agent.clear()


# ═══════════════════════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════════════════════


def get_snapshot_hash(state: bytes) -> str:
    """Compute the SHA-256 hash of a state."""
    return hashlib.sha256(state).hexdigest()


def compare_snapshots(a: Snapshot, b: Snapshot) -> bool:
    """Check if two snapshots have the same state."""
    return a.hash == b.hash
