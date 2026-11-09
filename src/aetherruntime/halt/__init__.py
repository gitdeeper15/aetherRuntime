"""AetherRuntime — Halt layer (Layer 4)."""

from .order import (
    propose_halt,
    HaltOrderRegistry,
    compute_halt_window,
    validate_halt_window,
    AgentNotFound,
    UnauthorizedProposer,
    InvalidSignature as OrderInvalidSignature,
)
from .quorum import (
    approve_halt,
    approve_batch,
    QuorumTracker,
    HaltNotFound,
    InvalidSignature as QuorumInvalidSignature,
    AlreadyApproved,
    QuorumAlreadyReached,
)

__all__ = [
    "propose_halt",
    "HaltOrderRegistry",
    "compute_halt_window",
    "validate_halt_window",
    "AgentNotFound",
    "UnauthorizedProposer",
    "OrderInvalidSignature",
    "approve_halt",
    "approve_batch",
    "QuorumTracker",
    "HaltNotFound",
    "QuorumInvalidSignature",
    "AlreadyApproved",
    "QuorumAlreadyReached",
]
