"""
AetherRuntime v2.0.0 — Core Entities

This module implements the 10 core entities defined in
docs/specification/01_entities.md:

1. Agent
2. TelemetryRecord
3. Baseline
4. AnomalyAlert
5. ContainmentPolicy
6. HaltOrder
7. HaltApproval
8. RecoveryRecord
9. Snapshot
10. RuntimeConfig

Each entity is a dataclass with validation in __post_init__.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════════════════


class AgentStatus(str, Enum):
    """Agent status (I3)."""
    IDLE = "idle"
    RUNNING = "running"
    ANOMALOUS = "anomalous"
    CONTAINED = "contained"
    HALTED = "halted"
    RECOVERING = "recovering"


class TelemetryCategory(str, Enum):
    """Telemetry categories."""
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    SYSCALL = "syscall"
    ACTION = "action"


class BaselineModel(str, Enum):
    """Baseline model types (I8)."""
    MEAN_STD = "mean_std"
    ZSCORE = "zscore"
    MOVING_AVERAGE = "moving_average"
    SEASONAL = "seasonal"


class ContainmentLevel(str, Enum):
    """Containment levels (I11)."""
    L1_THROTTLE = "L1_throttle"
    L2_ISOLATE = "L2_isolate"
    L3_QUARANTINE = "L3_quarantine"
    L4_FREEZE = "L4_freeze"


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _validate_hex(value: str, length: int, name: str) -> None:
    """Validate that value is a hex string of exact length."""
    if not isinstance(value, str) or len(value) != length:
        raise ValueError(f"{name} must be a hex string of length {length}")
    try:
        int(value, 16)
    except ValueError:
        raise ValueError(f"{name} must be a valid hex string")


def _validate_iso8601(value: str, name: str) -> None:
    """Validate that value is a valid ISO 8601 string."""
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValueError(f"{name} must be a valid ISO 8601 string")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 1 — Agent
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Agent:
    """
    An autonomous software actor (Entity 1).

    Fields: 5 (agent_id, public_key, created_at, metadata, status)
    Invariants: I1, I2, I3
    """
    agent_id: str
    public_key: bytes
    created_at: str
    status: AgentStatus = AgentStatus.IDLE
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        # I1: agent_id is a 64-char hex string
        _validate_hex(self.agent_id, 64, "agent_id")
        # I2: public_key is 32 bytes (Ed25519)
        if len(self.public_key) != 32:
            raise ValueError("public_key must be 32 bytes (Ed25519)")
        # I3: status is a valid AgentStatus
        if not isinstance(self.status, AgentStatus):
            raise ValueError(f"status must be AgentStatus, got {type(self.status)}")
        _validate_iso8601(self.created_at, "created_at")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 2 — TelemetryRecord
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class TelemetryRecord:
    """
    A time-stamped observation from a running agent (Entity 2).

    Fields: 6 (telemetry_id, agent_id, category, value, timestamp, metadata)
    Invariants: I4, I5, I6
    """
    telemetry_id: str
    agent_id: str
    category: TelemetryCategory
    value: float
    timestamp: str
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_hex(self.telemetry_id, 64, "telemetry_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        # I5: value is finite
        if not isinstance(self.value, (int, float)):
            raise ValueError("value must be int or float")
        if self.value != self.value or self.value in (float("inf"), float("-inf")):
            raise ValueError("value must be finite (not NaN or Inf)")
        _validate_iso8601(self.timestamp, "timestamp")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 3 — Baseline
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Baseline:
    """
    A statistical model of expected behaviour (Entity 3).

    Fields: 7 (baseline_id, agent_id, category, model_type,
                parameters, computed_at, sample_count)
    Invariants: I7, I8
    """
    baseline_id: str
    agent_id: str
    category: TelemetryCategory
    model_type: BaselineModel
    parameters: dict
    computed_at: str
    sample_count: int

    def __post_init__(self) -> None:
        _validate_hex(self.baseline_id, 64, "baseline_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        # I7: sample_count >= 10
        if self.sample_count < 10:
            raise ValueError("sample_count must be >= 10")
        # I8: parameters contains required keys
        required_keys = {
            BaselineModel.MEAN_STD: {"mean", "std"},
            BaselineModel.ZSCORE: {"mean", "std"},
            BaselineModel.MOVING_AVERAGE: {"window", "values"},
            BaselineModel.SEASONAL: {"period", "coefficients"},
        }
        required = required_keys.get(self.model_type, set())
        missing = required - set(self.parameters.keys())
        if missing:
            raise ValueError(f"parameters missing keys: {missing}")
        _validate_iso8601(self.computed_at, "computed_at")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 4 — AnomalyAlert
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class AnomalyAlert:
    """
    A record produced by detection (Entity 4).

    Fields: 7 (alert_id, agent_id, telemetry_id, baseline_id,
                confidence, reason, timestamp)
    Invariants: I9, I10, I30
    """
    alert_id: str
    agent_id: str
    telemetry_id: str
    baseline_id: str
    confidence: float
    reason: str
    timestamp: str

    def __post_init__(self) -> None:
        _validate_hex(self.alert_id, 64, "alert_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        _validate_hex(self.telemetry_id, 64, "telemetry_id")
        _validate_hex(self.baseline_id, 64, "baseline_id")
        # I9: confidence in [0.0, 1.0]
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")
        _validate_iso8601(self.timestamp, "timestamp")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 5 — ContainmentPolicy
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ContainmentPolicy:
    """
    A record specifying containment (Entity 5).

    Fields: 7 (policy_id, agent_id, alert_id, level,
                restrictions, expiry, created_at)
    Invariants: I11, I12, I13
    """
    policy_id: str
    agent_id: str
    alert_id: str
    level: ContainmentLevel
    restrictions: dict
    expiry: str
    created_at: str

    def __post_init__(self) -> None:
        _validate_hex(self.policy_id, 64, "policy_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        _validate_hex(self.alert_id, 64, "alert_id")
        # I11: level is a valid ContainmentLevel
        if not isinstance(self.level, ContainmentLevel):
            raise ValueError(f"level must be ContainmentLevel, got {type(self.level)}")
        # I12: expiry > created_at
        _validate_iso8601(self.expiry, "expiry")
        _validate_iso8601(self.created_at, "created_at")
        expiry_dt = datetime.fromisoformat(self.expiry.replace("Z", "+00:00"))
        created_dt = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
        if expiry_dt <= created_dt:
            raise ValueError("expiry must be > created_at")
        # I13: restrictions contains required keys
        required = {"cpu_percent", "memory_mb", "network", "filesystem"}
        missing = required - set(self.restrictions.keys())
        if missing:
            raise ValueError(f"restrictions missing keys: {missing}")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 6 — HaltOrder
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class HaltOrder:
    """
    A signed halt order (Entity 6).

    Fields: 9 (halt_id, agent_id, reason, proposer, proposer_signature,
                approvals, quorum_threshold, created_at, enforced_at)
    Invariants: I14, I15, I16, I17
    """
    halt_id: str
    agent_id: str
    reason: str
    proposer: str
    proposer_signature: bytes
    quorum_threshold: float
    created_at: str
    approvals: list = field(default_factory=list)
    enforced_at: Optional[str] = None

    def __post_init__(self) -> None:
        _validate_hex(self.halt_id, 64, "halt_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        _validate_hex(self.proposer, 64, "proposer")
        if len(self.proposer_signature) != 64:
            raise ValueError("proposer_signature must be 64 bytes")
        # I15: quorum_threshold in [0.5, 1.0]
        if not (0.5 <= self.quorum_threshold <= 1.0):
            raise ValueError("quorum_threshold must be in [0.5, 1.0]")
        _validate_iso8601(self.created_at, "created_at")
        if self.enforced_at is not None:
            _validate_iso8601(self.enforced_at, "enforced_at")

    def is_enforced(self) -> bool:
        """Check if quorum is reached and halt is enforced (I16)."""
        return self.enforced_at is not None

    def halt_window_seconds(self) -> Optional[float]:
        """Compute Δt_window (I17, Proposition 2)."""
        if self.enforced_at is None:
            return None
        created_dt = datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
        enforced_dt = datetime.fromisoformat(self.enforced_at.replace("Z", "+00:00"))
        return (enforced_dt - created_dt).total_seconds()


# ═══════════════════════════════════════════════════════════════════════════
# Entity 7 — HaltApproval
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class HaltApproval:
    """
    A signed approval for a halt order (Entity 7).

    Fields: 5 (approval_id, halt_id, approver, signature, timestamp)
    Invariants: I18, I19, I20
    """
    approval_id: str
    halt_id: str
    approver: str
    signature: bytes
    timestamp: str

    def __post_init__(self) -> None:
        _validate_hex(self.approval_id, 64, "approval_id")
        _validate_hex(self.halt_id, 64, "halt_id")
        _validate_hex(self.approver, 64, "approver")
        if len(self.signature) != 64:
            raise ValueError("signature must be 64 bytes")
        _validate_iso8601(self.timestamp, "timestamp")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 8 — Snapshot
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Snapshot:
    """
    A point-in-time capture of an agent's state (Entity 9).

    Fields: 6 (snapshot_id, agent_id, state, hash, timestamp, stored_at)
    Invariants: I24, I25, I26
    """
    snapshot_id: str
    agent_id: str
    state: bytes
    hash: str
    timestamp: str
    stored_at: str

    def __post_init__(self) -> None:
        _validate_hex(self.snapshot_id, 64, "snapshot_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        # I24: hash matches SHA-256 of state
        import hashlib
        actual = hashlib.sha256(self.state).hexdigest()
        if self.hash != actual:
            raise ValueError(f"hash mismatch: expected {actual}, got {self.hash}")
        _validate_iso8601(self.timestamp, "timestamp")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 9 — RecoveryRecord
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class RecoveryRecord:
    """
    A record of a recovery operation (Entity 8).

    Fields: 8 (recovery_id, agent_id, halt_id, snapshot_id,
                replay_log, verification_result, timestamp, reauthorized_by)
    Invariants: I21, I22, I23, I33
    """
    recovery_id: str
    agent_id: str
    halt_id: str
    snapshot_id: str
    replay_log: list
    verification_result: bool
    timestamp: str
    reauthorized_by: str

    def __post_init__(self) -> None:
        _validate_hex(self.recovery_id, 64, "recovery_id")
        _validate_hex(self.agent_id, 64, "agent_id")
        _validate_hex(self.halt_id, 64, "halt_id")
        _validate_hex(self.snapshot_id, 64, "snapshot_id")
        _validate_hex(self.reauthorized_by, 64, "reauthorized_by")
        _validate_iso8601(self.timestamp, "timestamp")


# ═══════════════════════════════════════════════════════════════════════════
# Entity 10 — RuntimeConfig
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class RuntimeConfig:
    """
    A configuration record (Entity 10).

    Fields: 6 (config_id, anomaly_threshold, halt_quorum,
                telemetry_rate_hz, containment_expiry_seconds, created_at)
    Invariants: I27, I28, I29
    """
    config_id: str
    anomaly_threshold: float
    halt_quorum: float
    telemetry_rate_hz: float
    containment_expiry_seconds: int
    created_at: str

    def __post_init__(self) -> None:
        _validate_hex(self.config_id, 64, "config_id")
        # I27: anomaly_threshold > 0
        if self.anomaly_threshold <= 0:
            raise ValueError("anomaly_threshold must be > 0")
        # I28: halt_quorum in [0.5, 1.0]
        if not (0.5 <= self.halt_quorum <= 1.0):
            raise ValueError("halt_quorum must be in [0.5, 1.0]")
        # I29: telemetry_rate_hz > 0
        if self.telemetry_rate_hz <= 0:
            raise ValueError("telemetry_rate_hz must be > 0")
        _validate_iso8601(self.created_at, "created_at")


# ═══════════════════════════════════════════════════════════════════════════
# Factory functions
# ═══════════════════════════════════════════════════════════════════════════


def _random_hex() -> str:
    """Generate a random 64-char hex string."""
    import secrets
    return secrets.token_hex(32)


def create_agent(public_key: bytes, metadata: Optional[dict] = None) -> Agent:
    """Factory: create a new Agent."""
    return Agent(
        agent_id=_random_hex(),
        public_key=public_key,
        created_at=_now_iso(),
        status=AgentStatus.IDLE,
        metadata=metadata or {},
    )


def create_runtime_config(
    anomaly_threshold: float = 1.0,
    halt_quorum: float = 0.67,
    telemetry_rate_hz: float = 1.0,
    containment_expiry_seconds: int = 300,
) -> RuntimeConfig:
    """Factory: create a RuntimeConfig with defaults."""
    return RuntimeConfig(
        config_id=_random_hex(),
        anomaly_threshold=anomaly_threshold,
        halt_quorum=halt_quorum,
        telemetry_rate_hz=telemetry_rate_hz,
        containment_expiry_seconds=containment_expiry_seconds,
        created_at=_now_iso(),
    )
