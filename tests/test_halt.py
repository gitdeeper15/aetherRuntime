"""Tests for halt (8 tests)."""

import pytest

from aetherruntime.models import AgentStatus, _now_iso, _random_hex
from aetherruntime.halt import (
    propose_halt,
    approve_halt,
    HaltOrderRegistry,
    QuorumTracker,
    UnauthorizedProposer,
    AlreadyApproved,
    QuorumAlreadyReached,
)


def _make_node_pair():
    """Create two nodes: proposer and target."""
    from aetherruntime.simulation import Node
    proposer = Node(seed=1)
    proposer.start()
    target = Node(seed=2)
    target.start()
    return proposer, target


def test_O5_propose_halt():
    """O5: propose_halt creates a HaltOrder with enforced_at=None."""
    proposer, target = _make_node_pair()
    order = propose_halt(
        agent=target.agent,
        proposer=proposer.agent,
        proposer_signature=b"\x01" + b"\x00" * 63,
        reason="test",
        quorum_threshold=0.67,
    )
    assert order.enforced_at is None
    assert order.is_enforced() is False


def test_E16_unauthorized_proposer():
    """E16: propose_halt raises UnauthorizedProposer."""
    proposer, target = _make_node_pair()
    with pytest.raises(UnauthorizedProposer):
        propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=b"\x01" + b"\x00" * 63,
            reason="test",
            quorum_threshold=0.67,
            is_proposer_authorized=False,
        )


def test_E17_invalid_signature():
    """E17: propose_halt raises InvalidSignature for bad signature."""
    proposer, target = _make_node_pair()
    with pytest.raises(Exception):  # InvalidSignature
        propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=b"\x00" * 64,  # invalid
            reason="test",
            quorum_threshold=0.67,
        )


def test_O6_approve_halt():
    """O6: approve_halt creates HaltApproval and enforces quorum."""
    proposer, target = _make_node_pair()
    order = propose_halt(
        agent=target.agent,
        proposer=proposer.agent,
        proposer_signature=b"\x01" + b"\x00" * 63,
        reason="test",
        quorum_threshold=0.67,
    )
    approval = approve_halt(
        halt_order=order,
        approver=proposer.agent,
        approver_signature=b"\x01" + b"\x00" * 63,
        total_authorized_nodes=1,  # 100% > 67% → quorum
    )
    assert order.is_enforced() is True


def test_I20_no_double_approval():
    """I20: approver cannot approve the same halt twice."""
    proposer, target = _make_node_pair()
    order = propose_halt(
        agent=target.agent,
        proposer=proposer.agent,
        proposer_signature=b"\x01" + b"\x00" * 63,
        reason="test",
        quorum_threshold=0.67,
    )
    approve_halt(order, proposer.agent, b"\x01" + b"\x00" * 63, 3)
    with pytest.raises(AlreadyApproved):
        approve_halt(order, proposer.agent, b"\x01" + b"\x00" * 63, 3)


def test_I15_quorum_threshold():
    """I15: quorum_threshold in [0.5, 1.0]."""
    proposer, target = _make_node_pair()
    with pytest.raises(ValueError):
        propose_halt(
            agent=target.agent,
            proposer=proposer.agent,
            proposer_signature=b"\x01" + b"\x00" * 63,
            reason="test",
            quorum_threshold=0.3,
        )


def test_I16_enforced_at_set():
    """I16: enforced_at is set iff quorum reached."""
    proposer, target = _make_node_pair()
    order = propose_halt(
        agent=target.agent,
        proposer=proposer.agent,
        proposer_signature=b"\x01" + b"\x00" * 63,
        reason="test",
        quorum_threshold=0.5,
    )
    approve_halt(order, proposer.agent, b"\x01" + b"\x00" * 63, 2)
    assert order.enforced_at is not None


def test_I17_halt_window_positive():
    """I17: Δt_window > 0 (Proposition 2)."""
    proposer, target = _make_node_pair()
    order = propose_halt(
        agent=target.agent,
        proposer=proposer.agent,
        proposer_signature=b"\x01" + b"\x00" * 63,
        reason="test",
        quorum_threshold=0.5,
    )
    approve_halt(order, proposer.agent, b"\x01" + b"\x00" * 63, 2)
    window = order.halt_window_seconds()
    assert window is not None
    assert window > 0
