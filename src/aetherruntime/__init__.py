"""
AetherRuntime v2.0.0 — Runtime assurance for the Aether family.

AetherRuntime is the **sixth functional dimension** (provisional) of the
Aether family. It investigates whether a runtime-assurance gap genuinely
exists, and specifies a five-layer architecture:

    1. Monitoring
    2. Detection
    3. Containment
    4. Halt
    5. Recovery

Quick start:
    >>> from aetherruntime import (
    ...     Agent, AgentStatus, TelemetryCategory,
    ...     create_agent, create_runtime_config,
    ... )
    >>> agent = create_agent(public_key=secrets.token_bytes(32))
    >>> agent.status = AgentStatus.RUNNING

Reference:
    Paper (v0.1.0): https://doi.org/10.5281/zenodo.24078477
    Figshare:       https://doi.org/10.6084/m9.figshare.34955746
    OSF:            https://doi.org/10.17605/OSF.IO/KZU7P
    Website:        https://aetherruntime.netlify.app

Status:
    Reference Implementation (v2.0.0). No real-world deployment.
    Propositions P1–P2 are proof sketches.
"""

# ─── Version ───
from .__version__ import (
    __version__,
    __paper_version__,
    __author__,
    __email__,
    __orcid__,
    __affiliation__,
    __license__,
    __doi__,
    __figshare_doi__,
    __osf_doi__,
    __record_id__,
    __website__,
    __github__,
    __gitlab__,
    __codeberg__,
    __bitbucket__,
    __pypi__,
    __aethergit_doi__,
    __aetherflow_doi__,
    __aetherproof_doi__,
    __aethermesh_doi__,
    __aethergovern_doi__,
    __status__,
    __real_world_deployment__,
    __peer_reviewed__,
)

# ─── Models (10 entities + 4 enums) ───
from .models import (
    Agent,
    AgentStatus,
    AnomalyAlert,
    Baseline,
    BaselineModel,
    ContainmentLevel,
    ContainmentPolicy,
    HaltApproval,
    HaltOrder,
    RecoveryRecord,
    RuntimeConfig,
    Snapshot,
    TelemetryCategory,
    TelemetryRecord,
    create_agent,
    create_runtime_config,
)

# ─── Monitoring (Layer 1) ───
from .monitoring import (
    collect,
    collect_batch,
    TelemetryLog,
    update_baseline,
    update_all_baselines,
    BaselineRegistry,
    AgentNotRunning,
    InvalidValue,
    NonMonotonicTimestamp,
    AgentNotFound as MonitoringAgentNotFound,
    InsufficientTelemetry,
    InvalidWindowSize,
)

# ─── Detection (Layer 2) ───
from .detection import (
    detect,
    detect_batch,
    summarize_detection,
    DetectionSummary,
    AlertRegistry,
    AlertStats,
    validate_alert_against_telemetry,
    filter_alerts_by_confidence,
    group_alerts_by_agent,
    latest_alert_for_agent,
    TelemetryNotFound,
    BaselineNotFound,
    NonDeterministic,
)

# ─── Containment (Layer 3) ───
from .containment import (
    contain,
    release,
    is_expired,
    ContainmentRegistry,
    DEFAULT_RESTRICTIONS,
    IsolationManager,
    IsolationState,
    ResourceSnapshot,
    enforce_restrictions,
    apply_isolation,
    release_isolation,
    AlertNotFound,
    InvalidLevel,
    ExpiryInPast,
    AlreadyContained,
)

# ─── Halt (Layer 4) ───
from .halt import (
    propose_halt,
    HaltOrderRegistry,
    compute_halt_window,
    validate_halt_window,
    approve_halt,
    approve_batch,
    QuorumTracker,
    AgentNotFound as HaltAgentNotFound,
    UnauthorizedProposer,
    HaltNotFound,
    AlreadyApproved,
    QuorumAlreadyReached,
)

# ─── Recovery (Layer 5) ───
from .recovery import (
    create_snapshot,
    verify_snapshot,
    SnapshotRegistry,
    HashMismatch,
    get_snapshot_hash,
    compare_snapshots,
    recover,
    RecoveryRegistry,
    RecoveryStats,
    AgentNotHalted,
    UnauthorizedReauthorizer,
    VerificationFailed,
)

# ─── Simulation (Layer 6, simulation only) ───
from .simulation import (
    Network,
    NetworkState,
    PartitionSchedule,
    Message,
    Node,
    create_cluster,
    Testbed,
    TestbedConfig,
    SCENARIOS,
    experiment_1_detection_accuracy,
    experiment_2_halt_window,
    experiment_3_recovery_correctness,
)


# ═══════════════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════════════


__all__ = [
    # Version
    "__version__",
    "__paper_version__",
    "__author__",
    "__email__",
    "__orcid__",
    "__affiliation__",
    "__license__",
    "__doi__",
    "__figshare_doi__",
    "__osf_doi__",
    "__record_id__",
    "__website__",
    "__github__",
    "__gitlab__",
    "__codeberg__",
    "__bitbucket__",
    "__pypi__",
    "__aethergit_doi__",
    "__aetherflow_doi__",
    "__aetherproof_doi__",
    "__aethermesh_doi__",
    "__aethergovern_doi__",
    "__status__",
    "__real_world_deployment__",
    "__peer_reviewed__",
    # Models
    "Agent",
    "AgentStatus",
    "AnomalyAlert",
    "Baseline",
    "BaselineModel",
    "ContainmentLevel",
    "ContainmentPolicy",
    "HaltApproval",
    "HaltOrder",
    "RecoveryRecord",
    "RuntimeConfig",
    "Snapshot",
    "TelemetryCategory",
    "TelemetryRecord",
    "create_agent",
    "create_runtime_config",
    # Monitoring
    "collect",
    "collect_batch",
    "TelemetryLog",
    "update_baseline",
    "update_all_baselines",
    "BaselineRegistry",
    "AgentNotRunning",
    "InvalidValue",
    "NonMonotonicTimestamp",
    "MonitoringAgentNotFound",
    "InsufficientTelemetry",
    "InvalidWindowSize",
    # Detection
    "detect",
    "detect_batch",
    "summarize_detection",
    "DetectionSummary",
    "AlertRegistry",
    "AlertStats",
    "validate_alert_against_telemetry",
    "filter_alerts_by_confidence",
    "group_alerts_by_agent",
    "latest_alert_for_agent",
    "TelemetryNotFound",
    "BaselineNotFound",
    "NonDeterministic",
    # Containment
    "contain",
    "release",
    "is_expired",
    "ContainmentRegistry",
    "DEFAULT_RESTRICTIONS",
    "IsolationManager",
    "IsolationState",
    "ResourceSnapshot",
    "enforce_restrictions",
    "apply_isolation",
    "release_isolation",
    "AlertNotFound",
    "InvalidLevel",
    "ExpiryInPast",
    "AlreadyContained",
    # Halt
    "propose_halt",
    "HaltOrderRegistry",
    "compute_halt_window",
    "validate_halt_window",
    "approve_halt",
    "approve_batch",
    "QuorumTracker",
    "HaltAgentNotFound",
    "UnauthorizedProposer",
    "HaltNotFound",
    "AlreadyApproved",
    "QuorumAlreadyReached",
    # Recovery
    "create_snapshot",
    "verify_snapshot",
    "SnapshotRegistry",
    "HashMismatch",
    "get_snapshot_hash",
    "compare_snapshots",
    "recover",
    "RecoveryRegistry",
    "RecoveryStats",
    "AgentNotHalted",
    "UnauthorizedReauthorizer",
    "VerificationFailed",
    # Simulation
    "Network",
    "NetworkState",
    "PartitionSchedule",
    "Message",
    "Node",
    "create_cluster",
    "Testbed",
    "TestbedConfig",
    "SCENARIOS",
    "experiment_1_detection_accuracy",
    "experiment_2_halt_window",
    "experiment_3_recovery_correctness",
]
