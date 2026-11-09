"""
AetherRuntime v2.0.0 — Recovery: Replay (Layer 5)

This module implements Operation 7 (`recover`) from
docs/specification/02_operations.md.

The `recover` operation restores a halted agent to a known-good state:
    1. Snapshot reconciliation: load the last known-good snapshot.
    2. Safe replay: replay only actions before the anomaly.
    3. Verification: verify the recovered state against specifications.
    4. Reauthorization: the agent must be re-authorized by AetherGovern.
    5. Resume: the agent resumes at the state before the anomaly.

Invariants enforced:
    - I21: verification_result = True before running
    - I22: snapshot_id refers to existing Snapshot
    - I23: reauthorized_by is authorized (via AetherGovern)
    - I33: RecoveryRecord follows a HaltOrder
    - O7: recover requires verification_result = True
    - X1: every admitted action has traceable authority
    - X4: every recovery produces RecoveryRecord with verification_result = True

Errors:
    - E19: AgentNotHalted
    - E20: SnapshotNotFound
    - E21: UnauthorizedReauthorizer
    - E22: VerificationFailed
"""

from __future__ import annotations

from typing import Optional

from ..models import (
    Agent,
    AgentStatus,
    HaltOrder,
    RecoveryRecord,
    Snapshot,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class AgentNotHalted(Exception):
    """E19: Agent status != halted."""
    pass


class SnapshotNotFound(Exception):
    """E20: snapshot_id does not exist."""
    pass


class UnauthorizedReauthorizer(Exception):
    """E21: reauthorized_by is not authorized."""
    pass


class VerificationFailed(Exception):
    """E22: Recovered state does not match specification."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Verification (stub; AetherProof in production)
# ═══════════════════════════════════════════════════════════════════════════


def _verify_recovered_state(
    agent: Agent,
    snapshot: Snapshot,
    replay_log: list,
) -> bool:
    """
    Verify that the recovered state matches specifications.

    In simulation, we check:
        - Snapshot hash is valid.
        - Replay log contains only safe actions (no anomaly triggers).

    In production, this would call AetherProof.
    """
    import hashlib
    expected = hashlib.sha256(snapshot.state).hexdigest()
    if expected != snapshot.hash:
        return False
    for action in replay_log:
        if action.get("safe", True) is False:
            return False
    return True


# ═══════════════════════════════════════════════════════════════════════════
# Operation 7 — recover
# ═══════════════════════════════════════════════════════════════════════════


def recover(
    agent: Agent,
    halt_order: HaltOrder,
    snapshot: Snapshot,
    replay_log: list,
    reauthorizer: Agent,
    is_reauthorizer_authorized: bool = True,
) -> RecoveryRecord:
    """
    Recover a halted agent to a known-good state (Operation 7).

    Args:
        agent: The agent to recover. Must be in `halted` state.
        halt_order: The HaltOrder that was enforced.
        snapshot: The Snapshot to restore.
        replay_log: List of safe actions to replay.
        reauthorizer: The agent re-authorizing recovery (via AetherGovern).
        is_reauthorizer_authorized: In production, checked via AetherGovern.

    Returns:
        A new RecoveryRecord with verification_result = True.

    Raises:
        AgentNotHalted: If agent.status != halted.
        SnapshotNotFound: If snapshot is None.
        UnauthorizedReauthorizer: If reauthorizer is not authorized.
        VerificationFailed: If recovered state does not match spec.

    Invariants:
        I21: verification_result = True before running.
        I22: snapshot_id refers to existing Snapshot.
        I23: reauthorized_by is authorized.
        I33: RecoveryRecord follows a HaltOrder.
        O7: recover requires verification_result = True.
        X4: every recovery produces RecoveryRecord with verification_result = True.

    Example:
        >>> record = recover(agent, halt, snapshot, [], reauth)
        >>> record.verification_result
        True
        >>> agent.status
        <AgentStatus.RUNNING: 'running'>
    """
    # ─── E19: Agent must be halted ───
    if agent.status != AgentStatus.HALTED:
        raise AgentNotHalted(
            f"Agent {agent.agent_id} is not halted (status: {agent.status.value})"
        )

    # ─── E20: Snapshot must exist ───
    if snapshot is None:
        raise SnapshotNotFound("snapshot must not be None")
    if snapshot.agent_id != agent.agent_id:
        raise SnapshotNotFound(
            f"snapshot {snapshot.snapshot_id} does not belong to "
            f"agent {agent.agent_id}"
        )

    # ─── I33: RecoveryRecord must follow a HaltOrder ───
    if halt_order is None or halt_order.agent_id != agent.agent_id:
        raise ValueError(
            f"halt_order does not match agent {agent.agent_id}"
        )

    # ─── E21: Reauthorizer must be authorized ───
    if not is_reauthorizer_authorized:
        raise UnauthorizedReauthorizer(
            f"Reauthorizer {reauthorizer.agent_id} is not authorized"
        )

    # ─── E22: Verify recovered state ───
    verification_result = _verify_recovered_state(agent, snapshot, replay_log)
    if not verification_result:
        raise VerificationFailed(
            f"Verification failed for agent {agent.agent_id}"
        )

    # ─── Q4: Update agent status to `recovering` ───
    agent.status = AgentStatus.RECOVERING

    # ─── Q1: Create RecoveryRecord ───
    record = RecoveryRecord(
        recovery_id=_random_hex(),
        agent_id=agent.agent_id,
        halt_id=halt_order.halt_id,
        snapshot_id=snapshot.snapshot_id,
        replay_log=replay_log,
        verification_result=verification_result,
        timestamp=_now_iso(),
        reauthorized_by=reauthorizer.agent_id,
    )

    # ─── Q4: Update agent status to `running` ───
    agent.status = AgentStatus.RUNNING

    return record


# ═══════════════════════════════════════════════════════════════════════════
# Recovery registry
# ═══════════════════════════════════════════════════════════════════════════


class RecoveryRegistry:
    """An in-memory registry of recovery records."""

    def __init__(self) -> None:
        self._records: dict[str, RecoveryRecord] = {}
        self._by_agent: dict[str, list[RecoveryRecord]] = {}

    def put(self, record: RecoveryRecord) -> None:
        """Register a recovery record."""
        if record.recovery_id in self._records:
            raise ValueError(
                f"recovery_id {record.recovery_id} already registered"
            )
        self._records[record.recovery_id] = record
        self._by_agent.setdefault(record.agent_id, []).append(record)

    def get(self, recovery_id: str) -> Optional[RecoveryRecord]:
        """Get a recovery record by ID."""
        return self._records.get(recovery_id)

    def get_by_agent(self, agent_id: str) -> list[RecoveryRecord]:
        """Get all recovery records for an agent."""
        return list(self._by_agent.get(agent_id, []))

    def count(self) -> int:
        """Count all recovery records."""
        return len(self._records)

    def clear(self) -> None:
        """Clear all records."""
        self._records.clear()
        self._by_agent.clear()


# ═══════════════════════════════════════════════════════════════════════════
# Recovery statistics
# ═══════════════════════════════════════════════════════════════════════════


class RecoveryStats:
    """Aggregated statistics for recovery records."""

    def __init__(self, records: list[RecoveryRecord]) -> None:
        self.records = records

    @property
    def total(self) -> int:
        return len(self.records)

    @property
    def n_verified(self) -> int:
        return sum(1 for r in self.records if r.verification_result)

    @property
    def verification_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.n_verified / self.total

    def __repr__(self) -> str:
        return (
            f"RecoveryStats(total={self.total}, "
            f"verified={self.n_verified}, "
            f"rate={self.verification_rate:.3f})"
        )
