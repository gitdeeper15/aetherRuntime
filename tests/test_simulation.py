"""Tests for simulation (10 tests)."""

import pytest

from aetherruntime.simulation import (
    Network,
    NetworkState,
    PartitionSchedule,
    Node,
    create_cluster,
    Testbed,
    TestbedConfig,
    SCENARIOS,
)


def test_network_creation():
    """Network can be created with N nodes."""
    net = Network(10, seed=42)
    assert net.n_nodes == 10
    assert len(net.node_ids) == 10


def test_node_creation():
    """Node can be created and started."""
    node = Node(seed=42)
    assert node.node_id is not None
    node.start()
    assert node.status.value == "running"


def test_testbed_run():
    """Testbed can run a scenario."""
    config = TestbedConfig(n_nodes=3, n_runs=2, seed=42)
    testbed = Testbed(config)
    result = testbed.run_experiment("S1")
    assert result["n_nodes"] == 3
    assert result["n_runs"] == 2
    assert result["mean_anomalies"] >= 0


def test_scenarios_registered():
    """All 6 scenarios are registered."""
    assert len(SCENARIOS) == 6
    for s in ["S1", "S2", "S3", "S4", "S5", "S6"]:
        assert s in SCENARIOS


def test_halt_propagation():
    """Halt order propagates through network."""
    net = Network(5, seed=42)
    net.broadcast("node-000", {"type": "halt"}, "halt")
    assert net.pending_count() == 4


def test_network_partition():
    """Network can be partitioned."""
    schedule = PartitionSchedule()
    schedule.add_step(step=1, partition=True)
    schedule.add_step(step=3, partition=False)
    net = Network(5, partition_schedule=schedule, seed=42)

    net.step_forward()  # step 1 → partitioned
    assert net.is_partitioned() is True

    net.step_forward()  # step 2 → partitioned
    net.step_forward()  # step 3 → connected
    assert net.is_partitioned() is False


def test_message_dropped_during_partition():
    """Messages are dropped during partition."""
    schedule = PartitionSchedule()
    schedule.add_step(step=1, partition=True)
    net = Network(5, partition_schedule=schedule, seed=42)
    net.step_forward()  # step 1 → partitioned
    success = net.send("node-000", "node-001", {"type": "test"})
    assert success is False


def test_message_delivered_when_connected():
    """Messages are delivered when connected."""
    net = Network(5, seed=42)
    success = net.send("node-000", "node-001", {"type": "test"})
    assert success is True
    net.deliver_all()
    assert net.delivered_count() == 1


def test_create_cluster():
    """create_cluster creates N nodes."""
    nodes = create_cluster(5, seed=42)
    assert len(nodes) == 5
    for node in nodes:
        assert node.status.value == "running"


def test_all_scenarios_run():
    """All 6 scenarios can run without errors."""
    config = TestbedConfig(n_nodes=2, n_runs=1, seed=42)
    testbed = Testbed(config)
    for s in ["S1", "S2", "S3", "S4", "S5", "S6"]:
        result = testbed.run_experiment(s)
        assert "mean_anomalies" in result
