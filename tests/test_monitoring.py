"""Tests for monitoring (8 tests)."""

import pytest

from aetherruntime.models import AgentStatus, BaselineModel, TelemetryCategory
from aetherruntime.monitoring import (
    collect,
    update_baseline,
    AgentNotRunning,
    InvalidValue,
    InsufficientTelemetry,
    InvalidWindowSize,
)


def test_O1_collect_creates_record(running_agent):
    """O1: collect creates a TelemetryRecord."""
    record = collect(running_agent, TelemetryCategory.CPU, 20.0)
    assert record.value == 20.0
    assert record.agent_id == running_agent.agent_id


def test_E2_agent_not_running(mock_agent):
    """E2: collect raises AgentNotRunning if status != running."""
    with pytest.raises(AgentNotRunning):
        collect(mock_agent, TelemetryCategory.CPU, 20.0)


def test_E3_invalid_value(running_agent):
    """E3: collect raises InvalidValue for NaN."""
    with pytest.raises(InvalidValue):
        collect(running_agent, TelemetryCategory.CPU, float("nan"))


def test_O2_update_baseline_window(running_agent):
    """O2: update_baseline requires window_size >= 10."""
    records = [collect(running_agent, TelemetryCategory.CPU, 20.0) for _ in range(20)]
    with pytest.raises(InvalidWindowSize):
        update_baseline(
            agent=running_agent,
            category=TelemetryCategory.CPU,
            model_type=BaselineModel.MEAN_STD,
            window_size=5,
            telemetry_records=records,
        )


def test_E6_insufficient_telemetry(running_agent):
    """E6: update_baseline raises InsufficientTelemetry."""
    records = [collect(running_agent, TelemetryCategory.CPU, 20.0) for _ in range(5)]
    with pytest.raises(InsufficientTelemetry):
        update_baseline(
            agent=running_agent,
            category=TelemetryCategory.CPU,
            model_type=BaselineModel.MEAN_STD,
            window_size=10,
            telemetry_records=records,
        )


def test_baseline_mean_std(running_agent):
    """Baseline with mean_std model computes mean and std."""
    records = [
        collect(running_agent, TelemetryCategory.CPU, 20.0 + i * 0.1)
        for i in range(20)
    ]
    baseline = update_baseline(
        agent=running_agent,
        category=TelemetryCategory.CPU,
        model_type=BaselineModel.MEAN_STD,
        window_size=10,
        telemetry_records=records,
    )
    assert "mean" in baseline.parameters
    assert "std" in baseline.parameters
    assert baseline.sample_count >= 10


def test_baseline_zscore(running_agent):
    """Baseline with zscore model computes z_scores."""
    records = [
        collect(running_agent, TelemetryCategory.CPU, 20.0 + i * 0.1)
        for i in range(20)
    ]
    baseline = update_baseline(
        agent=running_agent,
        category=TelemetryCategory.CPU,
        model_type=BaselineModel.ZSCORE,
        window_size=10,
        telemetry_records=records,
    )
    assert "z_scores" in baseline.parameters


def test_telemetry_categories(running_agent):
    """All 5 categories are accepted."""
    for cat in TelemetryCategory:
        record = collect(running_agent, cat, 10.0)
        assert record.category == cat
