from extensions.transfer_contracts.redundancy_api import (
    DecoderFamily,
    DecoderSemantics,
    SampleSemantics,
    require_fixed_budget,
)


def test_fixed_budget_accepts_expected_k():
    semantics = DecoderSemantics(
        family=DecoderFamily.PROPOSAL,
        sample_semantics=SampleSemantics.PERSISTENT_SLOT,
        candidate_count=32,
        persistent_identity=True,
    )
    require_fixed_budget(semantics, expected_k=32)


def test_fixed_budget_rejects_wrong_k():
    semantics = DecoderSemantics(
        family=DecoderFamily.DIFFUSION,
        sample_semantics=SampleSemantics.STOCHASTIC_SAMPLE,
        candidate_count=16,
        persistent_identity=False,
    )
    try:
        require_fixed_budget(semantics, expected_k=32)
    except ValueError as exc:
        assert "Expected K=32" in str(exc)
    else:
        raise AssertionError("Expected ValueError for wrong K")
