"""Tests for detection (8 tests)."""

import pytest

from aetherruntime.models import (
    AnomalyAlert,
    Baseline,
    BaselineModel,
    TelemetryCategory,
    TelemetryRecord,
    _now_iso,
    _random_hex,
)
from aetherruntime.detection import (
    detect,
    detect_batch,
    AlertRegistry,
    BaselineNotFound,
    TelemetryNotFound,
)


def _make_baseline(agent_id):
    return Baseline(
        baseline_id=_random_hex(),
        agent_id=agent_id,
        category=TelemetryCategory.CPU,
        model_type=BaselineModel.MEAN_STD,
        parameters={"mean": 20.0, "std": 2.0},
        computed_at=_now_iso(),
        sample_count=20,
    )


def _make_record(agent_id, value):
    return TelemetryRecord(
        telemetry_id=_random_hex(),
        agent_id=agent_id,
        category=TelemetryCategory.CPU,
        value=value,
        timestamp=_now_iso(),
    )


def test_O3_detect_anomaly(mock_agent):
    """O3: detect returns AnomalyAlert for spikes."""
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 100.0)
    alert = detect(record, baseline, threshold=2.0)
    assert alert is not None
    assert 0.0 <= alert.confidence <= 1.0


def test_O3_detect_no_anomaly(mock_agent):
    """O3: detect returns None for normal values."""
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 20.0)
    alert = detect(record, baseline, threshold=2.0)
    assert alert is None


def test_O3_detect_deterministic(mock_agent):
    """O3: detect is deterministic (same input → same verdict)."""
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 100.0)
    alert1 = detect(record, baseline, threshold=2.0)
    alert2 = detect(record, baseline, threshold=2.0)
    assert (alert1 is None) == (alert2 is None)
    if alert1 and alert2:
        assert abs(alert1.confidence - alert2.confidence) < 1e-6


def test_E8_telemetry_not_found():
    """E8: detect raises TelemetryNotFound."""
    with pytest.raises(TelemetryNotFound):
        detect(None, _make_baseline(_random_hex()))


def test_E9_baseline_not_found(mock_agent):
    """E9: detect raises BaselineNotFound."""
    record = _make_record(mock_agent.agent_id, 20.0)
    with pytest.raises(BaselineNotFound):
        detect(record, None)


def test_I9_confidence_range(mock_agent):
    """I9: confidence is in [0.0, 1.0]."""
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 100.0)
    alert = detect(record, baseline, threshold=2.0)
    assert alert is not None
    assert 0.0 <= alert.confidence <= 1.0


def test_I10_alert_references_telemetry(mock_agent):
    """I10: alert.telemetry_id refers to the record."""
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 100.0)
    alert = detect(record, baseline, threshold=2.0)
    assert alert.telemetry_id == record.telemetry_id


def test_alert_registry(mock_agent):
    """AlertRegistry stores and retrieves alerts."""
    registry = AlertRegistry()
    baseline = _make_baseline(mock_agent.agent_id)
    record = _make_record(mock_agent.agent_id, 100.0)
    alert = detect(record, baseline, threshold=2.0)
    registry.put(alert)
    assert registry.get(alert.alert_id) is alert
    assert registry.count() == 1
