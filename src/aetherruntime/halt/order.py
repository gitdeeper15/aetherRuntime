"""
AetherRuntime v2.0.0 — Halt: Order (Layer 4)

This module implements Operation 5 (`propose_halt`) from
docs/specification/02_operations.md.

The `propose_halt` operation creates a signed halt order for an agent.
The halt becomes enforced when a quorum of authorized nodes approves it
(see `quorum.py`).

Key properties:
    - The proposer must be authorized (via AetherGovern).
    - The proposer's signature must verify (Ed25519).
    - The halt window Δt_window > 0 (Proposition 2).

Invariants enforced:
    - I14: proposer_signature verifies
    - I15: quorum_threshold in [0.5, 1.0]
    - I16: enforced_at set iff quorum reached
    - I17: Δt_window > 0 (Proposition 2)
    - O5: propose_halt requires valid signature

Errors:
    - E15: AgentNotFound
    - E16: UnauthorizedProposer
    - E17: InvalidSignature
"""

from __future__ import annotations

import hashlib
from typing import Optional

from ..models import (
    Agent,
    AgentStatus,
    HaltOrder,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class AgentNotFound(Exception):
    """E15: Agent does not exist."""
    pass


class UnauthorizedProposer(Exception):
    """E16: Proposer is not authorized (via AetherGovern)."""
    pass


class InvalidSignature(Exception):
    """E17: proposer_signature does not verify."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Signature verification (stub; Ed25519 in production)
# ═══════════════════════════════════════════════════════════════════════════


def _verify_signature(
    public_key: bytes,
    signature: bytes,
    message: bytes,
) -> bool:
    """
    Verify an Ed25519 signature.

    In simulation, we use a deterministic hash-based stub. In production,
    this would use the `cryptography` library's Ed25519 verifier.
    """
    if len(signature) != 64:
        return False
    if len(public_key) != 32:
        return False
    # Stub: signature must be 64 bytes and start with a non-zero byte
    # In production: Ed25519PublicKey.from_public_bytes(public_key).verify(signature, message)
    return signature[0] != 0


# ═══════════════════════════════════════════════════════════════════════════
# Operation 5 — propose_halt
# ═══════════════════════════════════════════════════════════════════════════


def propose_halt(
    agent: Agent,
    proposer: Agent,
    proposer_signature: bytes,
    reason: str,
    quorum_threshold: float = 0.67,
    is_proposer_authorized: bool = True,
) -> HaltOrder:
    """
    Propose a halt order for a compromised agent (Operation 5).

    Args:
        agent: The agent to halt.
        proposer: The agent proposing the halt. Must be authorized.
        proposer_signature: Ed25519 signature from the proposer.
        reason: Human-readable reason for the halt.
        quorum_threshold: Required fraction of approvals (default 0.67 = 2/3).
        is_proposer_authorized: In production, checked via AetherGovern.

    Returns:
        A new HaltOrder with `enforced_at = None`.

    Raises:
        AgentNotFound: If agent or proposer is None.
        UnauthorizedProposer: If proposer is not authorized.
        InvalidSignature: If proposer_signature does not verify.

    Invariants:
        I14: proposer_signature verifies.
        I15: quorum_threshold in [0.5, 1.0].
        I16: enforced_at is None (until quorum reached).
        O5: propose_halt requires valid signature.

    Example:
        >>> order = propose_halt(agent, proposer, sig, "anomalous CPU")
        >>> order.enforced_at
        None
    """
    # ─── E15: Agent and proposer must exist ───
    if agent is None:
        raise AgentNotFound("agent must not be None")
    if proposer is None:
        raise AgentNotFound("proposer must not be None")

    # ─── E16: Proposer must be authorized (via AetherGovern) ───
    if not is_proposer_authorized:
        raise UnauthorizedProposer(
            f"Proposer {proposer.agent_id} is not authorized"
        )

    # ─── I15: quorum_threshold in [0.5, 1.0] ───
    if not (0.5 <= quorum_threshold <= 1.0):
        raise ValueError(
            f"quorum_threshold must be in [0.5, 1.0], got {quorum_threshold}"
        )

    # ─── I14: Verify proposer signature ───
    halt_id = _random_hex()
    created_at = _now_iso()
    message = _halt_message(halt_id, agent.agent_id, reason, created_at)
    if not _verify_signature(proposer.public_key, proposer_signature, message):
        raise InvalidSignature("proposer_signature does not verify")

    # ─── Q1: Create HaltOrder with enforced_at = None ───
    return HaltOrder(
        halt_id=halt_id,
        agent_id=agent.agent_id,
        reason=reason,
        proposer=proposer.agent_id,
        proposer_signature=proposer_signature,
        quorum_threshold=quorum_threshold,
        created_at=created_at,
        approvals=[],
        enforced_at=None,  # I16: not enforced until quorum
    )


def _halt_message(
    halt_id: str,
    agent_id: str,
    reason: str,
    created_at: str,
) -> bytes:
    """Construct the message that the proposer signs."""
    return hashlib.sha256(
        f"{halt_id}|{agent_id}|{reason}|{created_at}".encode("utf-8")
    ).digest()


# ═══════════════════════════════════════════════════════════════════════════
# Halt order registry
# ═══════════════════════════════════════════════════════════════════════════


class HaltOrderRegistry:
    """An in-memory registry of halt orders."""

    def __init__(self) -> None:
        self._orders: dict[str, HaltOrder] = {}
        self._by_agent: dict[str, list[HaltOrder]] = {}

    def put(self, order: HaltOrder) -> None:
        """Register a halt order."""
        if order.halt_id in self._orders:
            raise ValueError(f"halt_id {order.halt_id} already registered")
        self._orders[order.halt_id] = order
        self._by_agent.setdefault(order.agent_id, []).append(order)

    def get(self, halt_id: str) -> Optional[HaltOrder]:
        """Get a halt order by ID."""
        return self._orders.get(halt_id)

    def get_by_agent(self, agent_id: str) -> list[HaltOrder]:
        """Get all halt orders for an agent."""
        return list(self._by_agent.get(agent_id, []))

    def enforced_for_agent(self, agent_id: str) -> list[HaltOrder]:
        """Get all enforced halt orders for an agent."""
        return [o for o in self.get_by_agent(agent_id) if o.is_enforced()]

    def count(self) -> int:
        """Count all halt orders."""
        return len(self._orders)

    def clear(self) -> None:
        """Clear all halt orders."""
        self._orders.clear()
        self._by_agent.clear()


# ═══════════════════════════════════════════════════════════════════════════
# Halt window computation (Proposition 2)
# ═══════════════════════════════════════════════════════════════════════════


def compute_halt_window(order: HaltOrder) -> Optional[float]:
    """
    Compute the halt window Δt_window for an enforced halt order.

    Δt_window = enforced_at - created_at (Proposition 2).

    Returns:
        The window in seconds, or None if not enforced.
    """
    return order.halt_window_seconds()


def validate_halt_window(order: HaltOrder) -> bool:
    """
    Validate that Δt_window > 0 (I17, Proposition 2).

    Returns:
        True if enforced and window > 0, False otherwise.
    """
    window = compute_halt_window(order)
    return window is not None and window > 0
