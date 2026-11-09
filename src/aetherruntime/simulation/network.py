"""
AetherRuntime v2.0.0 — Simulation: Network (Layer 6, simulation only)

This module provides a simple peer-to-peer network simulator for
testing AetherRuntime. It supports:
    - N nodes (agents)
    - Message passing between nodes
    - Network partitions
    - Gossip propagation (for halt orders)

This is a simulation, not a production network.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════════════════


class NetworkState(str, Enum):
    """Network operational state."""
    CONNECTED = "connected"
    PARTITIONED = "partitioned"
    DEGRADED = "degraded"


# ═══════════════════════════════════════════════════════════════════════════
# Partition schedule
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class PartitionSchedule:
    """
    A schedule for network partitions.

    Example:
        >>> schedule = PartitionSchedule()
        >>> schedule.add_step(step=10, partition=True)
        >>> schedule.add_step(step=20, partition=False)
    """
    events: list[tuple[int, bool]] = field(default_factory=list)

    def add_step(self, step: int, partition: bool) -> None:
        """Add a partition event at a given step."""
        self.events.append((step, partition))
        self.events.sort(key=lambda e: e[0])

    def state_at(self, step: int) -> bool:
        """Return True if partitioned at `step`, False otherwise."""
        current = False
        for event_step, is_partition in self.events:
            if event_step <= step:
                current = is_partition
            else:
                break
        return current


# ═══════════════════════════════════════════════════════════════════════════
# Message
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Message:
    """A message between two nodes."""
    sender: str
    receiver: str
    payload: dict
    timestamp: str
    message_type: str = "generic"

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "type": self.message_type,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Network
# ═══════════════════════════════════════════════════════════════════════════


class Network:
    """
    A simple peer-to-peer network simulator.

    Attributes:
        n_nodes: Number of nodes.
        state: Current network state.
        partition_schedule: Schedule of partitions.
        message_queue: Pending messages.
        delivered_messages: Delivered messages (for analysis).
    """

    def __init__(
        self,
        n_nodes: int,
        partition_schedule: Optional[PartitionSchedule] = None,
        seed: Optional[int] = None,
    ) -> None:
        if n_nodes <= 0:
            raise ValueError("n_nodes must be > 0")
        self.n_nodes = n_nodes
        self.node_ids = [f"node-{i:03d}" for i in range(n_nodes)]
        self.state = NetworkState.CONNECTED
        self.partition_schedule = partition_schedule or PartitionSchedule()
        self.message_queue: list[Message] = []
        self.delivered_messages: list[Message] = []
        self.step = 0
        self._rng = random.Random(seed)

    def step_forward(self) -> None:
        """Advance the simulation by one step."""
        self.step += 1
        if self.partition_schedule.state_at(self.step):
            self.state = NetworkState.PARTITIONED
        else:
            self.state = NetworkState.CONNECTED

    def is_partitioned(self) -> bool:
        """Check if the network is currently partitioned."""
        return self.state == NetworkState.PARTITIONED

    def broadcast(self, sender: str, payload: dict, message_type: str = "generic") -> int:
        """
        Broadcast a message from `sender` to all other nodes.

        Args:
            sender: The sender node ID.
            payload: The message payload.
            message_type: Type of message (for classification).

        Returns:
            Number of messages queued.
        """
        if sender not in self.node_ids:
            raise ValueError(f"Unknown sender: {sender}")
        count = 0
        for receiver in self.node_ids:
            if receiver == sender:
                continue
            self.send(sender, receiver, payload, message_type)
            count += 1
        return count

    def send(
        self,
        sender: str,
        receiver: str,
        payload: dict,
        message_type: str = "generic",
    ) -> bool:
        """
        Send a message from `sender` to `receiver`.

        Returns:
            True if queued successfully, False if dropped (partition).
        """
        if sender not in self.node_ids or receiver not in self.node_ids:
            raise ValueError("Unknown sender or receiver")
        if self.is_partitioned():
            # Drop message during partition
            return False
        from datetime import datetime, timezone
        msg = Message(
            sender=sender,
            receiver=receiver,
            payload=payload,
            timestamp=datetime.now(timezone.utc).isoformat(),
            message_type=message_type,
        )
        self.message_queue.append(msg)
        return True

    def deliver_all(self) -> int:
        """
        Deliver all queued messages.

        Returns:
            Number of messages delivered.
        """
        n = len(self.message_queue)
        self.delivered_messages.extend(self.message_queue)
        self.message_queue.clear()
        return n

    def pending_count(self) -> int:
        """Count pending messages."""
        return len(self.message_queue)

    def delivered_count(self) -> int:
        """Count delivered messages."""
        return len(self.delivered_messages)

    def statistics(self) -> dict:
        """Return network statistics."""
        return {
            "n_nodes": self.n_nodes,
            "step": self.step,
            "state": self.state.value,
            "pending": self.pending_count(),
            "delivered": self.delivered_count(),
        }
