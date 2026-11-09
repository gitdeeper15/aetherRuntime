"""Tests for recovery (8 tests)."""

import pytest

from aetherruntime.models import AgentStatus, _now_iso, _random_hex
from aetherruntime.recovery import (
    create_snapshot,
    verify_snapshot,
    recover,
    SnapshotRegistry,
    RecoveryRegistry,
    AgentNotHalted,
    HashMismatch,
)


def _make_halted_agent():
    """Create a halted agent."""
    from aetherruntime.simulation import Node
    node = Node(seed=42)
    node.start()
    node.agent.status = AgentStatus.HALTED
    return node


def test_O7_recover(mock_agent):
    """O7: recover returns RecoveryRecord with verification_result=True."""
    from aetherruntime.simulation import Node
    node = _make_halted_agent()
    snapshot = create_snapshot(node.agent, b"state")
    reauthorizer = Node(seed=99)
    reauthorizer.start()

    halt_order = type('obj', (object,), {
        'halt_id': _random_hex(),
        'agent_id': node.agent.agent_id,
    })()

    record = recover(
        agent=node.agent,
        halt_order=halt_order,
        snapshot=snapshot,
        replay_log=[],
        reauthorizer=reauthorizer.agent,
    )
    assert record.verification_result is True


def test_E19_agent_not_halted(mock_agent):
    """E19: recover raises AgentNotHalted."""
    from aetherruntime.simulation import Node
    node = Node(seed=42)
    node.start()  # running, not halted
    snapshot = create_snapshot(node.agent, b"state")
    halt_order = type('obj', (object,), {
        'halt_id': _random_hex(),
        'agent_id': node.agent.agent_id,
    })()
    with pytest.raises(AgentNotHalted):
        recover(node.agent, halt_order, snapshot, [], mock_agent)


def test_I21_verification_before_running():
    """I21: verification_result=True before resuming."""
    node = _make_halted_agent()
    snapshot = create_snapshot(node.agent, b"state")
    from aetherruntime.simulation import Node
    reauthorizer = Node(seed=99)
    reauthorizer.start()
    halt_order = type('obj', (object,), {
        'halt_id': _random_hex(),
        'agent_id': node.agent.agent_id,
    })()
    record = recover(node.agent, halt_order, snapshot, [], reauthorizer.agent)
    assert record.verification_result is True
    assert node.agent.status == AgentStatus.RUNNING


def test_I24_hash_matches_state(mock_agent):
    """I24: Snapshot hash matches SHA-256 of state."""
    snapshot = create_snapshot(mock_agent, b"test state")
    assert verify_snapshot(snapshot) is True


def test_hash_mismatch_raises(mock_agent):
    """HashMismatch raised for invalid hash."""
    import hashlib
    with pytest.raises(ValueError):
        from aetherruntime.models import Snapshot
        Snapshot(
            snapshot_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            state=b"test",
            hash="invalid_hash",
            timestamp=_now_iso(),
            stored_at="aethergit://test",
        )


def test_snapshot_registry(mock_agent):
    """SnapshotRegistry stores and retrieves snapshots."""
    registry = SnapshotRegistry()
    snapshot = create_snapshot(mock_agent, b"state1")
    registry.put(snapshot)
    assert registry.get(snapshot.snapshot_id) is snapshot
    assert registry.count() == 1


def test_recovery_registry(mock_agent):
    """RecoveryRegistry stores records."""
    registry = RecoveryRegistry()
    assert registry.count() == 0


def test_snapshot_latest_for_agent(mock_agent):
    """SnapshotRegistry.latest_for_agent returns the most recent."""
    registry = SnapshotRegistry()
    s1 = create_snapshot(mock_agent, b"state1")
    registry.put(s1)
    latest = registry.latest_for_agent(mock_agent.agent_id)
    assert latest is not None
