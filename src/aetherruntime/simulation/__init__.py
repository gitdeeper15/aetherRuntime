"""AetherRuntime — Simulation layer (Layer 6, simulation only)."""

from .network import (
    Network,
    NetworkState,
    PartitionSchedule,
    Message,
)
from .node import (
    Node,
    create_cluster,
)
from .testbed import (
    Testbed,
    TestbedConfig,
    Scenario,
    SCENARIOS,
    experiment_1_detection_accuracy,
    experiment_2_halt_window,
    experiment_3_recovery_correctness,
)

__all__ = [
    "Network",
    "NetworkState",
    "PartitionSchedule",
    "Message",
    "Node",
    "create_cluster",
    "Testbed",
    "TestbedConfig",
    "Scenario",
    "SCENARIOS",
    "experiment_1_detection_accuracy",
    "experiment_2_halt_window",
    "experiment_3_recovery_correctness",
]
