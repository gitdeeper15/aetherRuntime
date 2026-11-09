"""AetherRuntime — Recovery layer (Layer 5)."""

from .snapshot import (
    create_snapshot,
    verify_snapshot,
    SnapshotRegistry,
    SnapshotNotFound as SnapshotSnapshotNotFound,
    HashMismatch,
    get_snapshot_hash,
    compare_snapshots,
)
from .replay import (
    recover,
    RecoveryRegistry,
    RecoveryStats,
    AgentNotHalted,
    SnapshotNotFound as ReplaySnapshotNotFound,
    UnauthorizedReauthorizer,
    VerificationFailed,
)

__all__ = [
    "create_snapshot",
    "verify_snapshot",
    "SnapshotRegistry",
    "SnapshotSnapshotNotFound",
    "HashMismatch",
    "get_snapshot_hash",
    "compare_snapshots",
    "recover",
    "RecoveryRegistry",
    "RecoveryStats",
    "AgentNotHalted",
    "ReplaySnapshotNotFound",
    "UnauthorizedReauthorizer",
    "VerificationFailed",
]
