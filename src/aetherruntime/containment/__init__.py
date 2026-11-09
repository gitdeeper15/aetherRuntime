"""AetherRuntime — Containment layer (Layer 3)."""

from .policy import (
    contain,
    release,
    is_expired,
    ContainmentRegistry,
    DEFAULT_RESTRICTIONS,
    AlertNotFound,
    InvalidLevel,
    ExpiryInPast,
    AlreadyContained,
)
from .isolation import (
    IsolationManager,
    IsolationState,
    ResourceSnapshot,
    enforce_restrictions,
    apply_isolation,
    release_isolation,
)

__all__ = [
    "contain",
    "release",
    "is_expired",
    "ContainmentRegistry",
    "DEFAULT_RESTRICTIONS",
    "AlertNotFound",
    "InvalidLevel",
    "ExpiryInPast",
    "AlreadyContained",
    "IsolationManager",
    "IsolationState",
    "ResourceSnapshot",
    "enforce_restrictions",
    "apply_isolation",
    "release_isolation",
]
