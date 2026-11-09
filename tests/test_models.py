"""Tests for models.py (10 tests)."""

import pytest

from aetherruntime.models import (
    Agent,
    AgentStatus,
    Baseline,
    BaselineModel,
    ContainmentLevel,
    ContainmentPolicy,
    TelemetryCategory,
    TelemetryRecord,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# I1–I10: Structural invariants
# ═══════════════════════════════════════════════════════════════════════════


def test_I1_agent_id_unique(mock_public_key):
    """I1: agent_id is a 64-char hex string."""
    with pytest.raises(ValueError):
        Agent(
            agent_id="short",
            public_key=mock_public_key,
            created_at=_now_iso(),
        )


def test_I2_public_key_valid(mock_public_key):
    """I2: public_key is 32 bytes (Ed25519)."""
    with pytest.raises(ValueError):
        Agent(
            agent_id=_random_hex(),
            public_key=b"short",
            created_at=_now_iso(),
        )


def test_I3_status_enum(mock_public_key):
    """I3: status is a valid AgentStatus."""
    with pytest.raises(ValueError):
        Agent(
            agent_id=_random_hex(),
            public_key=mock_public_key,
            created_at=_now_iso(),
            status="unknown",
        )


def test_I4_telemetry_id_unique(mock_agent):
    """I4: telemetry_id is a 64-char hex string."""
    with pytest.raises(ValueError):
        TelemetryRecord(
            telemetry_id="short",
            agent_id=mock_agent.agent_id,
            category=TelemetryCategory.CPU,
            value=20.0,
            timestamp=_now_iso(),
        )


def test_I5_value_finite(mock_agent):
    """I5: value must be finite (not NaN, not Inf)."""
    with pytest.raises(ValueError):
        TelemetryRecord(
            telemetry_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            category=TelemetryCategory.CPU,
            value=float("nan"),
            timestamp=_now_iso(),
        )
    with pytest.raises(ValueError):
        TelemetryRecord(
            telemetry_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            category=TelemetryCategory.CPU,
            value=float("inf"),
            timestamp=_now_iso(),
        )


def test_I7_baseline_sample_count(mock_agent):
    """I7: sample_count must be >= 10."""
    with pytest.raises(ValueError):
        Baseline(
            baseline_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            category=TelemetryCategory.CPU,
            model_type=BaselineModel.MEAN_STD,
            parameters={"mean": 20.0, "std": 2.0},
            computed_at=_now_iso(),
            sample_count=5,
        )


def test_I8_baseline_parameters(mock_agent):
    """I8: parameters contains required keys for model_type."""
    with pytest.raises(ValueError):
        Baseline(
            baseline_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            category=TelemetryCategory.CPU,
            model_type=BaselineModel.MEAN_STD,
            parameters={"mean": 20.0},  # missing 'std'
            computed_at=_now_iso(),
            sample_count=20,
        )


def test_I11_containment_level(mock_agent):
    """I11: level must be a valid ContainmentLevel."""
    with pytest.raises(ValueError):
        ContainmentPolicy(
            policy_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            alert_id=_random_hex(),
            level="invalid",
            restrictions={
                "cpu_percent": 10.0,
                "memory_mb": 512,
                "network": "deny",
                "filesystem": "read-only",
            },
            expiry=_now_iso(),
            created_at=_now_iso(),
        )


def test_I12_expiry_after_created(mock_agent):
    """I12: expiry must be > created_at."""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    past = (now - timedelta(hours=1)).isoformat()
    with pytest.raises(ValueError):
        ContainmentPolicy(
            policy_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            alert_id=_random_hex(),
            level=ContainmentLevel.L1_THROTTLE,
            restrictions={
                "cpu_percent": 10.0,
                "memory_mb": 512,
                "network": "deny",
                "filesystem": "read-only",
            },
            expiry=past,
            created_at=now.isoformat(),
        )


def test_I13_restrictions_keys(mock_agent):
    """I13: restrictions contains all required keys."""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    future = (now + timedelta(hours=1)).isoformat()
    with pytest.raises(ValueError):
        ContainmentPolicy(
            policy_id=_random_hex(),
            agent_id=mock_agent.agent_id,
            alert_id=_random_hex(),
            level=ContainmentLevel.L1_THROTTLE,
            restrictions={"cpu_percent": 10.0},  # missing keys
            expiry=future,
            created_at=now.isoformat(),
        )
