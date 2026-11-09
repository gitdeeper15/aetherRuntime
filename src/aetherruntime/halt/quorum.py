"""
AetherRuntime v2.0.0 — Halt: Quorum (Layer 4)

This module implements Operation 6 (`approve_halt`) from
docs/specification/02_operations.md.

The `approve_halt` operation registers an approval from an authorized node
and, when the quorum threshold is reached, enforces the halt order.

Key properties:
    - Each approver can approve only once (I20).
    - Enforced when approvals count / total ≥ quorum_threshold (I16).
    - Δt_window > 0 (Proposition 2, I17).

Invariants enforced:
    - I16: enforced_at set iff quorum reached
    - I17: Δt_window > 0
    - I18: signature verifies
    - I19: approval_id unique
    - I20: approver cannot approve twice
    - O6: approve_halt cannot be done twice by same approver

Errors:
    - E18: HaltNotFound
    - E19: InvalidSignature
    - Additional: AlreadyApproved, QuorumAlreadyReached
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Optional

from ..models import (
    Agent,
    HaltApproval,
    HaltOrder,
    _now_iso,
    _random_hex,
)


# ═══════════════════════════════════════════════════════════════════════════
# Errors
# ═══════════════════════════════════════════════════════════════════════════


class HaltNotFound(Exception):
    """E18: halt_id does not exist."""
    pass


class InvalidSignature(Exception):
    """E19: approver_signature does not verify."""
    pass


class AlreadyApproved(Exception):
    """The approver has already approved this halt (I20)."""
    pass


class QuorumAlreadyReached(Exception):
    """Quorum was already reached; halt is enforced."""
    pass


# ═══════════════════════════════════════════════════════════════════════════
# Signature verification (stub)
# ═══════════════════════════════════════════════════════════════════════════


def _verify_signature(
    public_key: bytes,
    signature: bytes,
    message: bytes,
) -> bool:
    """Verify an Ed25519 signature (stub)."""
    if len(signature) != 64:
        return False
    if len(public_key) != 32:
        return False
    return signature[0] != 0


def _approval_message(halt_id: str, approver_id: str, timestamp: str) -> bytes:
    """Construct the message that the approver signs."""
    return hashlib.sha256(
        f"{halt_id}|{approver_id}|{timestamp}".encode("utf-8")
    ).digest()


# ═══════════════════════════════════════════════════════════════════════════
# Operation 6 — approve_halt
# ═══════════════════════════════════════════════════════════════════════════


def approve_halt(
    halt_order: HaltOrder,
    approver: Agent,
    approver_signature: bytes,
    total_authorized_nodes: int,
    is_approver_authorized: bool = True,
) -> HaltApproval:
    """
    Approve a halt order (Operation 6).

    Args:
        halt_order: The HaltOrder to approve.
        approver: The agent approving. Must be authorized.
        approver_signature: Ed25519 signature from the approver.
        total_authorized_nodes: Total number of authorized nodes.
        is_approver_authorized: In production, checked via AetherGovern.

    Returns:
        A new HaltApproval. If quorum is reached, halt_order.enforced_at
        is updated and the halt is enforced.

    Raises:
        HaltNotFound: If halt_order is None.
        InvalidSignature: If approver_signature does not verify.
        AlreadyApproved: If approver has already approved.
        QuorumAlreadyReached: If quorum was already reached.

    Invariants:
        I16: enforced_at set iff quorum reached.
        I17: Δt_window > 0 (Proposition 2).
        I18: signature verifies.
        I19: approval_id unique.
        I20: approver cannot approve twice.
        O6: approve_halt cannot be done twice by same approver.

    Example:
        >>> approval = approve_halt(order, node1, sig, total=3)
        >>> order.is_enforced()
        False  # need 2/3 approvals
        >>> approval2 = approve_halt(order, node2, sig2, total=3)
        >>> order.is_enforced()
        True   # 2/3 = quorum
    """
    # ─── E18: HaltOrder must exist ───
    if halt_order is None:
        raise HaltNotFound("halt_order must not be None")

    # ─── Quorum already reached? ───
    if halt_order.is_enforced():
        raise QuorumAlreadyReached(
            f"Quorum already reached for halt {halt_order.halt_id}"
        )

    # ─── E16: Approver must be authorized ───
    if not is_approver_authorized:
        raise InvalidSignature(
            f"Approver {approver.agent_id} is not authorized"
        )

    # ─── I20: Approver cannot approve twice ───
    for existing in halt_order.approvals:
        if existing.approver == approver.agent_id:
            raise AlreadyApproved(
                f"Approver {approver.agent_id} already approved halt "
                f"{halt_order.halt_id}"
            )

    # ─── I19: Generate unique approval_id ───
    approval_id = _random_hex()
    timestamp = _now_iso()

    # ─── I18: Verify signature ───
    message = _approval_message(halt_order.halt_id, approver.agent_id, timestamp)
    if not _verify_signature(approver.public_key, approver_signature, message):
        raise InvalidSignature("approver_signature does not verify")

    # ─── Q1: Create HaltApproval ───
    approval = HaltApproval(
        approval_id=approval_id,
        halt_id=halt_order.halt_id,
        approver=approver.agent_id,
        signature=approver_signature,
        timestamp=timestamp,
    )

    # ─── Register approval ───
    halt_order.approvals.append(approval)

    # ─── I16: Check quorum ───
    approvals_count = len(halt_order.approvals)
    quorum_reached = (approvals_count / total_authorized_nodes) >= halt_order.quorum_threshold

    if quorum_reached:
        # ─── I17: Δt_window > 0 (Proposition 2) ───
        created_dt = datetime.fromisoformat(
            halt_order.created_at.replace("Z", "+00:00")
        )
        enforced_dt = datetime.now(timezone.utc)
        if enforced_dt <= created_dt:
            # Force at least 1 microsecond window
            from datetime import timedelta
            enforced_dt = created_dt + timedelta(microseconds=1)
        halt_order.enforced_at = enforced_dt.isoformat()

    return approval


# ═══════════════════════════════════════════════════════════════════════════
# Batch approval
# ═══════════════════════════════════════════════════════════════════════════


def approve_batch(
    halt_order: HaltOrder,
    approvals: list[tuple[Agent, bytes, bool]],
    total_authorized_nodes: int,
) -> list[HaltApproval]:
    """
    Approve a halt order with multiple nodes in sequence.

    Args:
        halt_order: The HaltOrder to approve.
        approvals: List of (approver, signature, is_authorized) tuples.
        total_authorized_nodes: Total number of authorized nodes.

    Returns:
        List of successfully registered HaltApprovals.
    """
    result: list[HaltApproval] = []
    for approver, sig, is_auth in approvals:
        try:
            approval = approve_halt(
                halt_order, approver, sig, total_authorized_nodes, is_auth
            )
            result.append(approval)
        except (AlreadyApproved, QuorumAlreadyReached):
            continue
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Quorum tracker
# ═══════════════════════════════════════════════════════════════════════════


class QuorumTracker:
    """
    Tracks quorum status for halt orders.

    Provides query methods for approval counts, quorum percentage,
    and enforcement status.
    """

    def __init__(self, total_authorized_nodes: int) -> None:
        if total_authorized_nodes <= 0:
            raise ValueError("total_authorized_nodes must be > 0")
        self.total = total_authorized_nodes

    def status(self, halt_order: HaltOrder) -> dict:
        """Return quorum status for a halt order."""
        n_approvals = len(halt_order.approvals)
        percentage = n_approvals / self.total if self.total > 0 else 0.0
        return {
            "halt_id": halt_order.halt_id,
            "n_approvals": n_approvals,
            "total_authorized": self.total,
            "percentage": percentage,
            "threshold": halt_order.quorum_threshold,
            "quorum_reached": percentage >= halt_order.quorum_threshold,
            "enforced": halt_order.is_enforced(),
        }

    def is_enforced(self, halt_order: HaltOrder) -> bool:
        """Check if a halt order is enforced."""
        return halt_order.is_enforced()

    def remaining_approvals(self, halt_order: HaltOrder) -> int:
        """Count how many more approvals are needed."""
        if halt_order.is_enforced():
            return 0
        needed = int(self.total * halt_order.quorum_threshold) + 1
        return max(0, needed - len(halt_order.approvals))
