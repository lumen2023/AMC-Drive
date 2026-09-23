"""Framework-neutral AMC-Drive transfer contracts.

The contracts preserve the distinction between a decoder that samples
candidates, a consequence representation that compares candidates, and a
selector that converts candidate opportunity into one deployed action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol


TensorLike = Any


class DecoderFamily(str, Enum):
    """Decoder family used for migration bookkeeping."""

    PROPOSAL = "proposal"
    DIFFUSION = "diffusion"
    FLOW_MATCHING = "flow_matching"
    ROBOT_POLICY = "robot_policy"
    OTHER = "other"


class SampleSemantics(str, Enum):
    """Meaning of the fixed K axis."""

    PERSISTENT_SLOT = "persistent_slot"
    STOCHASTIC_SAMPLE = "stochastic_sample"
    ACTION_CHUNK = "action_chunk"


@dataclass(frozen=True)
class DecoderSemantics:
    family: DecoderFamily
    sample_semantics: SampleSemantics
    candidate_count: int
    persistent_identity: bool
    notes: str = ""


@dataclass(frozen=True)
class CandidateBatch:
    """Decoded fixed-budget candidates.

    Expected semantic shape for candidates is [B, K, T, D].
    """

    condition: Mapping[str, Any]
    candidates: TensorLike
    semantics: DecoderSemantics
    actions: TensorLike | None = None
    valid_mask: TensorLike | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RepresentationBatch:
    """Candidate-conditioned consequence representation."""

    latents: TensorLike
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RelationBatch:
    """Pairwise within-condition candidate relation."""

    similarities: TensorLike
    distances: TensorLike | None = None
    tau: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CapacityCalibrationOutput:
    loss: TensorLike
    metrics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SelectionOutput:
    selected: TensorLike
    scores: TensorLike
    metadata: Mapping[str, Any] = field(default_factory=dict)


class CandidateDecoder(Protocol):
    def sample(self, condition: Mapping[str, Any], budget: int) -> CandidateBatch:
        """Return candidates with explicit [B,K,T,D] semantics."""


class ConsequenceEncoder(Protocol):
    def encode(self, condition: Mapping[str, Any], candidates: CandidateBatch) -> RepresentationBatch:
        """Return candidate-conditioned consequence representations."""


class RedundancyRelation(Protocol):
    def pairwise(self, representation: RepresentationBatch) -> RelationBatch:
        """Return a within-condition [B,K,K] relation object."""


class CapacityCalibrator(Protocol):
    def loss(
        self,
        candidates: CandidateBatch,
        relation: RelationBatch,
        endpoint_context: Mapping[str, Any],
    ) -> CapacityCalibrationOutput:
        """Return a decoder-aware auxiliary calibration loss."""


class CandidateSelector(Protocol):
    def select(self, candidates: CandidateBatch, scores: TensorLike) -> SelectionOutput:
        """Select one candidate from the fixed-budget set."""


def require_fixed_budget(semantics: DecoderSemantics, expected_k: int) -> None:
    """Raise if a candidate batch violates the fixed-budget contract."""

    if semantics.candidate_count != expected_k:
        raise ValueError(
            f"Expected K={expected_k}, got K={semantics.candidate_count}."
        )
