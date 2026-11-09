"""Pytest fixtures for AetherRuntime tests."""

import secrets
import pytest

from aetherruntime.models import (
    Agent,
    AgentStatus,
    Baseline,
    BaselineModel,
    ContainmentLevel,
    ContainmentPolicy,
    HaltOrder,
    Snapshot,
    TelemetryCategory,
    TelemetryRecord,
    _now_iso,
    _random_hex,
    create_agent,
)


@pytest.fixture
def mock_public_key():
    """Valid 32-byte Ed25519 public key."""
    return secrets.token_bytes(32)


@pytest.fixture
def mock_agent(mock_public_key):
    """A valid Agent in idle state."""
    return Agent(
        agent_id=_random_hex(),
        public_key=mock_public_key,
        created_at=_now_iso(),
        status=AgentStatus.IDLE,
    )


@pytest.fixture
def running_agent(mock_agent):
    """A valid Agent in running state."""
    mock_agent.status = AgentStatus.RUNNING
    return mock_agent


@pytest.fixture
def mock_telemetry(mock_agent):
    """A valid TelemetryRecord."""
    return TelemetryRecord(
        telemetry_id=_random_hex(),
        agent_id=mock_agent.agent_id,
        category=TelemetryCategory.CPU,
        value=20.0,
        timestamp=_now_iso(),
    )


@pytest.fixture
def mock_baseline(mock_agent):
    """A valid Baseline with 20 samples."""
    return Baseline(
        baseline_id=_random_hex(),
        agent_id=mock_agent.agent_id,
        category=TelemetryCategory.CPU,
        model_type=BaselineModel.MEAN_STD,
        parameters={"mean": 20.0, "std": 2.0},
        computed_at=_now_iso(),
        sample_count=20,
    )


@pytest.fixture
def mock_snapshot(mock_agent):
    """A valid Snapshot."""
    import hashlib
    state = b"test state"
    return Snapshot(
        snapshot_id=_random_hex(),
        agent_id=mock_agent.agent_id,
        state=state,
        hash=hashlib.sha256(state).hexdigest(),
        timestamp=_now_iso(),
        stored_at=f"aethergit://test/{_random_hex()[:8]}",
    )


@pytest.fixture
def mock_signature():
    """A valid 64-byte signature (stub)."""
    return b"\x01" + b"\x00" * 63


@pytest.fixture
def mock_halt_order(mock_agent, mock_signature):
    """A valid HaltOrder (not enforced)."""
    return HaltOrder(
        halt_id=_random_hex(),
        agent_id=mock_agent.agent_id,
        reason="test",
        proposer=mock_agent.agent_id,
        proposer_signature=mock_signature,
        quorum_threshold=0.67,
        created_at=_now_iso(),
    )
