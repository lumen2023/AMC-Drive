"""Bounded full-trajectory diversity losses for the R31-D2 pilot.

The learned consequence relation is deliberately a stopped-gradient weight.
Only proposal geometry receives gradients in this pilot.
"""
from __future__ import annotations

import torch


def pairwise_trajectory_rbf(
    proposals: torch.Tensor, bandwidth: float
) -> torch.Tensor:
    """Return ``exp(-d/(2b))`` for mean squared xy trajectory distance.

    Args:
        proposals: [B, P, T, >=2] local trajectories.
        bandwidth: positive, fixed before training.
    """
    if proposals.ndim != 4 or proposals.shape[-1] < 2:
        raise ValueError(f"invalid proposal shape {tuple(proposals.shape)}")
    if not bandwidth > 0:
        raise ValueError("bandwidth must be positive")
    xy = proposals[..., :2]
    d2 = (xy[:, :, None] - xy[:, None, :]).square().sum(-1).mean(-1)
    return torch.exp(-d2 / (2.0 * bandwidth))


def weighted_upper_mean(matrix: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
    """Weighted upper-triangle mean; empty scenes contribute zero."""
    if matrix.shape != weights.shape or matrix.ndim != 3:
        raise ValueError("matrix and weights must both have shape [B,P,P]")
    p = matrix.shape[-1]
    upper = torch.triu(torch.ones(p, p, dtype=torch.bool, device=matrix.device), 1)
    w = weights[:, upper]
    x = matrix[:, upper]
    denom = w.sum(-1)
    per_scene = torch.where(denom > 0, (w * x).sum(-1) / denom.clamp_min(1e-12), 0.0)
    return per_scene.mean()


def dual_channel_loss(
    proposals: torch.Tensor,
    quality: torch.Tensor,
    duplicate_mask: torch.Tensor,
    bandwidth: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return geometry coverage and precision-filtered redundancy terms.

    Both terms lie in [0,1]. Minimization reduces RBF similarity. ``quality``
    and ``duplicate_mask`` must be frozen inputs; this function detaches them
    defensively so the proposal is the only gradient path.
    """
    sim = pairwise_trajectory_rbf(proposals, bandwidth)
    q = quality.detach().clamp(0, 1)
    if q.shape != proposals.shape[:2]:
        raise ValueError("quality must have shape [B,P]")
    if duplicate_mask.shape != sim.shape:
        raise ValueError("duplicate_mask must have shape [B,P,P]")
    quality_pairs = q[:, :, None] * q[:, None, :]
    geometry = weighted_upper_mean(sim, quality_pairs)
    relation = weighted_upper_mean(sim, quality_pairs * duplicate_mask.detach().to(sim.dtype))
    return geometry, relation
