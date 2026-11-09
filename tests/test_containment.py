"""Tests for containment (8 tests)."""

import pytest
from datetime import datetime, timedelta, timezone

from aetherruntime.models import (
    AnomalyAlert,
    AgentStatus,
    ContainmentLevel,
    _now_iso,
    _random_hex,
)
from aetherruntime.containment import (
    contain,
    release,
    is_expired,
    ContainmentRegistry,
    AlertNotFound,
    ExpiryInPast,
    AlreadyContained,
)


def _make_alert(agent_id):
    return AnomalyAlert(
        alert_id=_random_hex(),
        agent_id=agent_id,
        telemetry_id=_random_hex(),
        baseline_id=_random_hex(),
        confidence=0.9,
        reason="test",
        timestamp=_now_iso(),
    )


def test_contain_l1(mock_agent):
    """contain with L1_throttle creates a policy."""
    alert = _make_alert(mock_agent.agent_id)
    policy = contain(mock_agent, alert, ContainmentLevel.L1_THROTTLE, 300)
    assert policy.level == ContainmentLevel.L1_THROTTLE
    assert mock_agent.status == AgentStatus.CONTAINED


def test_contain_l4(mock_agent):
    """contain with L4_freeze creates a policy."""
    alert = _make_alert(mock_agent.agent_id)
    policy = contain(mock_agent, alert, ContainmentLevel.L4_FREEZE, 300)
    assert policy.level == ContainmentLevel.L4_FREEZE


def test_E11_alert_not_found(mock_agent):
    """E11: contain raises AlertNotFound if alert is None."""
    with pytest.raises(AlertNotFound):
        contain(mock_agent, None, ContainmentLevel.L1_THROTTLE, 300)


def test_E13_expiry_in_past(mock_agent):
    """E13: contain raises ExpiryInPast if expiry_seconds <= 0."""
    alert = _make_alert(mock_agent.agent_id)
    with pytest.raises(ExpiryInPast):
        contain(mock_agent, alert, ContainmentLevel.L1_THROTTLE, -1)


def test_release(mock_agent):
    """X5: containment is reversible."""
    alert = _make_alert(mock_agent.agent_id)
    policy = contain(mock_agent, alert, ContainmentLevel.L1_THROTTLE, 300)
    assert mock_agent.status == AgentStatus.CONTAINED
    release(mock_agent, policy)
    assert mock_agent.status == AgentStatus.RUNNING


def test_is_expired(mock_agent):
    """is_expired returns True for expired policies."""
    alert = _make_alert(mock_agent.agent_id)
    policy = contain(mock_agent, alert, ContainmentLevel.L1_THROTTLE, 1)
    # Not yet expired
    assert not is_expired(policy)


def test_containment_registry(mock_agent):
    """ContainmentRegistry stores and retrieves policies."""
    registry = ContainmentRegistry()
    alert = _make_alert(mock_agent.agent_id)
    policy = contain(mock_agent, alert, ContainmentLevel.L2_ISOLATE, 300)
    registry.put(policy)
    assert registry.get(policy.policy_id) is policy
    assert registry.count() == 1


def test_already_contained(mock_agent):
    """E14: cannot contain at same or lower level twice."""
    alert = _make_alert(mock_agent.agent_id)
    policy1 = contain(mock_agent, alert, ContainmentLevel.L3_QUARANTINE, 300)
    with pytest.raises(AlreadyContained):
        contain(mock_agent, alert, ContainmentLevel.L2_ISOLATE, 300,
                existing_policy=policy1)
