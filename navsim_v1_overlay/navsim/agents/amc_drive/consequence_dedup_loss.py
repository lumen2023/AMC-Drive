"""Differentiable consequence-axis de-redundancy loss.

This module implements the R22-R25 result: the de-redundancy object is NOT
"trajectory geometric diversity" (the existing `diversity_loss` in
amc_drive_agent.py, which acts on local x/y/yaw coordinates), but "behavior-axis
coverage" -- the lateral (cross-centerline) lane position of candidate endpoints.

The loss is fully differentiable end-to-end:
    proposal_endpoint(local) --SE(2)--> world --polyline projection--> (P, L)
    -> gated lateral-coverage loss.

Reference: docs/R25_可微链路闭环与训练方案_20260915.md
"""

from __future__ import annotations

import torch


def se2_transform_local_to_world(
    pts_local: torch.Tensor,   # (..., 2) local x,y
    ego_x: torch.Tensor,       # (...) scalar world x
    ego_y: torch.Tensor,       # (...) scalar world y
    ego_yaw: torch.Tensor,     # (...) scalar world yaw
) -> torch.Tensor:
    """SE(2) compose: world = ego + R(yaw) @ local. Differentiable.

    Assumes pts_local are expressed relative to ego rear-axle frame
    (x forward, y left), matching the AMC-Drive proposal coordinate convention.
    """
    c = torch.cos(ego_yaw)
    s = torch.sin(ego_yaw)
    # Broadcast ego scalars (B,) against pts_local (B, P, 2):
    # expand ego to (B, 1) so it broadcasts over the P dimension.
    while c.dim() < pts_local.dim() - 1:
        c = c.unsqueeze(-1)
        s = s.unsqueeze(-1)
        ego_x = ego_x.unsqueeze(-1)
        ego_y = ego_y.unsqueeze(-1)
    wx = ego_x + c * pts_local[..., 0] - s * pts_local[..., 1]
    wy = ego_y + s * pts_local[..., 0] + c * pts_local[..., 1]
    return torch.stack([wx, wy], dim=-1)


def project_to_polyline(
    pts: torch.Tensor,           # (..., 2) world points
    vertices: torch.Tensor,      # (N, 2) centerline vertices (deduplicated)
    seg_len: torch.Tensor,       # (N-1,) segment lengths
    cum_arc: torch.Tensor,       # (N,) cumulative arc length from start
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Project points onto a polyline.

    Returns (arc_len, signed_lateral, nearest_seg_idx).
    arc_len: (...,) arc length along polyline of projection.
    signed_lateral: (...,) signed perpendicular distance (positive = left).
    Differentiable except at measure-zero boundaries (segment switch / endpoints).
    """
    a = vertices[:-1]  # (N-1, 2)
    b = vertices[1:]   # (N-1, 2)
    ab = b - a         # (N-1, 2)
    ab2 = (ab * ab).sum(-1)  # (N-1,)

    # project onto each segment
    # pts: (..., 2) -> (..., N-1, 2)
    x = pts.unsqueeze(-2)
    t = ((x - a) * ab).sum(-1) / ab2  # (..., N-1)
    t = torch.clamp(t, 0.0, 1.0)
    proj = a + t.unsqueeze(-1) * ab  # (..., N-1, 2)
    d2 = ((x - proj) ** 2).sum(-1)   # (..., N-1)

    k = torch.argmin(d2, dim=-1)  # (...,) nearest segment index

    # gather the nearest-segment quantities
    t_k = torch.gather(t, -1, k.unsqueeze(-1)).squeeze(-1)       # (...,)
    seg_k = torch.gather(seg_len, 0, k.reshape(-1)).reshape(k.shape)  # (...,)
    arc_k = torch.gather(cum_arc[:-1], 0, k.reshape(-1)).reshape(k.shape)  # (...,)

    arc_len = arc_k + t_k * seg_k

    # signed lateral: cross product sign of (b-a) x (pt - a_k)
    a_k = a[k]  # (..., 2)
    ab_k = ab[k]  # (..., 2)
    v = pts - a_k  # (..., 2)
    cross = ab_k[..., 0] * v[..., 1] - ab_k[..., 1] * v[..., 0]  # (...,)
    # perpendicular distance (sqrt with eps smoothing: |L| has non-smooth
    # subgradient at L=0 exactly on the centerline; eps avoids NaN there)
    d2_k = torch.gather(d2, -1, k.unsqueeze(-1)).squeeze(-1)
    d_k = torch.sqrt(d2_k + 1e-12)
    signed_lateral = torch.sign(cross) * d_k

    return arc_len, signed_lateral, k


def consequence_dedup_loss(
    proposals: torch.Tensor,      # (B, P, T, 3) local (x,y,yaw) proposal trajectories
    ego_x: torch.Tensor,          # (B,) world ego x
    ego_y: torch.Tensor,          # (B,) world ego y
    ego_yaw: torch.Tensor,        # (B,) world ego yaw
    centerlines: list,            # list of B tensors (N_b, 2) world centerline vertices
    tau_p: float = 0.9,           # optimal-band progress threshold
    lateral_bins: int = 32,       # (unused placeholder for future binning)
    lateral_reg_weight: float = 0.0,  # lateral quadratic regularizer weight
    return_diagnostics: bool = False,
):
    """Gated lateral-coverage de-redundancy loss.

    For each batch element, among proposals in the optimal band
    (progress > tau_p * scene_max_progress), penalize lateral clustering:

        L = - mean_{i != j in B} |L_i - L_j|  +  lambda * mean_{i in B} L_i^2

    where L_i = signed lateral offset of proposal endpoint from centerline.

    The first term maximizes lateral coverage (de-redundancy); the second term
    is a quadratic regularizer pulling endpoints back toward the centerline,
    preventing unbounded lateral drift. At equilibrium the lateral spread is
    uniform with range = 2 / lambda (see docs/R30). lambda = 0.4 => range ~5m.

    The gate B is computed on DETACHED progress so gradients only act on the
    lateral positions of selected proposals (prevents 'lower progress to escape
    gate' degeneracy).

    Args:
        proposals: (B, P, T, 3) local proposal trajectories.
        ego_x, ego_y, ego_yaw: (B,) world ego pose at scene time.
        centerlines: list of B (N_b, 2) world centerline vertex arrays.
        tau_p: optimal-band threshold (fraction of scene max progress).
        lateral_reg_weight: lambda, quadratic lateral regularizer (0 disables).

    Returns:
        loss (scalar). If return_diagnostics, also returns dict of diagnostics.
    """
    B, P, T, _ = proposals.shape
    device = proposals.device
    dtype = proposals.dtype

    endpoint_local = proposals[:, :, -1, :2]  # (B, P, 2)

    # SE(2) to world (differentiable)
    endpoint_world = se2_transform_local_to_world(
        endpoint_local, ego_x, ego_y, ego_yaw
    )  # (B, P, 2)

    losses = []
    diag = {"n_selected": [], "lateral_spread": [], "gate_size": []}

    for b in range(B):
        verts = centerlines[b].to(device=device, dtype=dtype)
        # deduplicate zero-length segments
        d = torch.norm(verts[1:] - verts[:-1], dim=-1)
        keep = torch.cat([torch.tensor([True], device=device), d > 1e-9])
        verts = verts[keep]
        if verts.shape[0] < 2:
            losses.append(torch.zeros((), device=device, dtype=dtype))
            continue

        seg_len = torch.norm(verts[1:] - verts[:-1], dim=-1)
        cum_arc = torch.cat([torch.zeros(1, device=device, dtype=dtype),
                             torch.cumsum(seg_len, 0)])

        arc, signed_lat, _ = project_to_polyline(
            endpoint_world[b], verts, seg_len, cum_arc
        )  # (P,), (P,)

        # progress = longitudinal arc length along centerline (physical meaning:
        # how far along the route the ego has advanced). No shift needed: the
        # optimal band is the set of proposals whose arc reaches the scene's
        # maximal forward extent.
        prog = torch.clamp(arc, min=0.0)
        scene_max = prog.max()
        if scene_max <= 0:
            losses.append(torch.zeros((), device=device, dtype=dtype))
            continue

        # gate B: progress > tau_p * scene_max (DETACHED)
        gate = (prog.detach() > tau_p * scene_max.detach())

        n_sel = int(gate.sum())
        diag["gate_size"].append(n_sel)

        if n_sel < 2:
            losses.append(torch.zeros((), device=device, dtype=dtype))
            diag["lateral_spread"].append(0.0)
            diag["n_selected"].append(n_sel)
            continue

        L_sel = signed_lat[gate]  # (n_sel,)
        # pairwise |L_i - L_j| mean (over upper triangle)
        pair = torch.abs(L_sel[:, None] - L_sel[None, :])
        triu = torch.triu(pair, diagonal=1)
        n_pair = n_sel * (n_sel - 1) / 2
        mean_pair = triu.sum() / n_pair

        # de-redundancy loss = -mean pairwise lateral distance (maximize spread)
        # + quadratic lateral regularizer (pull back toward centerline)
        loss_b = -mean_pair
        if lateral_reg_weight > 0:
            loss_b = loss_b + lateral_reg_weight * (L_sel ** 2).mean()

        losses.append(loss_b)
        diag["n_selected"].append(n_sel)
        diag["lateral_spread"].append(float((L_sel.max() - L_sel.min()).detach()))

    loss = torch.stack(losses).mean()

    if return_diagnostics:
        return loss, diag
    return loss
