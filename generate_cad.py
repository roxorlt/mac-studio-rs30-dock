#!/usr/bin/env python3
"""
StudioBeam DuoDock V3 — Front-Slide Cassette Portal + Heavy-Duty 5.4kg Load & 360° Clearance CAD
Target Hardware:
  1. Apple Mac Studio (M5 Max / M5 Ultra, 2026):
     - Body: 197.0 x 197.0 x 95.0 mm (87.0 mm aluminum unibody + 8.0 mm bottom foot)
     - Corner Radius: R30.4 mm, Bottom Air Intake Ring: Ø179.2 mm (R = 89.6 mm)
  2. XGIMI RS30 Series (RS30 Pro / Pro Max / Ultra / Ultra Max, 2026):
     - Overall (with integrated U-gimbal): 298.0 (W) x 249.0 (H) x 190.0 (D) mm, 5.3 - 5.4 kg
     - 360° Horizontal Swept Radius: R_sweep = 166.5 mm (Ø333.0 mm swept cylinder)
     - Swivel Base Turntable: ~Ø196 mm, center 1/4"-20 UNC mount thread

V3 Key Upgrade — Front-Loading Slide-In Cassette Bay ("前推滑入式导轨机舱"):
  - Front-Left & Front-Right pillars sit strictly outside Mac Studio's width (|X| = 99.7..107.7 mm),
    creating a 199.4 mm wide unobstructed front portal (+Y) with full-height 105 mm clearance!
  - Left & Right horizontal slide rails (|X| = 91.2..99.7 mm at Z = 26.0 mm) clear Mac Studio's
    Ø179.2 mm (|X| <= 89.6 mm) circular bottom foot during horizontal insertion.
  - Rear-Left & Rear-Right pillars retain R31.6 curved backstops so sliding Mac Studio in from the
    front automatically stops at exact center, while leaving a 152 mm wide rear port & power-button window!
  - Mac Studio can now be slid straight in/out from the front WITHOUT lifting or touching the 5.4 kg RS30 on top!
"""

from __future__ import annotations

import json
import math
import struct
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class DockParams:
    # Authoritative M5 Mac Studio dimensions (mm)
    mac_w: float = 197.0
    mac_d: float = 197.0
    mac_body_h: float = 87.0
    mac_foot_h: float = 8.0
    mac_corner_r: float = 30.4
    mac_intake_d: float = 179.2

    # Authoritative XGIMI RS30 dimensions (mm)
    rs30_total_w: float = 298.0
    rs30_total_h: float = 249.0
    rs30_total_d: float = 190.0
    rs30_swept_r: float = 166.5
    rs30_base_d: float = 196.0
    rs30_bolt_hole_d: float = 7.0

    # Power brick bay (RS30 280W-300W adapter, mounted alongside Left/Right blank wall)
    brick_w: float = 188.0
    brick_t: float = 44.0
    brick_h: float = 92.0

    # V3 Front-Slide Cassette & Heavy-Duty Structural Clearances (mm)
    mac_side_clearance: float = 1.2   # 197.0 + 2*1.2 = 199.4 mm clear front slide-in width!
    rail_inner_half: float = 91.2     # 182.4 mm foot channel (> Ø179.2 mm circular foot -> 8.5 mm wide side rails!)
    wall_thickness: float = 8.0       # 8.0 mm heavy-duty pillar wall -> 215.4 x 215.4 mm outer (fits 256mm bed!)
    base_ring_h: float = 6.0          # 6.0 mm bed tie-frame (12 mm BELOW Mac Studio's Z=18mm foot bottom!)
    shelf_z: float = 26.0             # Slide-rail Z height (elevates Mac Studio corners 26mm; foot at Z=18mm)
    air_gap_above_mac: float = 18.0   # 18 mm cool air plenum & finger lift clearance above Mac Studio
    tenon_h: float = 8.0
    tenon_inset: float = 1.9
    tenon_tol: float = 0.25

    # V3 Heavy-Duty Support-Free Upper Deck parameters (mm)
    deck_seat_z: float = 16.0         # 16.0 mm solid structural bridge plate
    deck_outer_z: float = 15.0        # Outer corners stepped 1mm below turntable seat for 360° U-arm clearance
    deck_lip_top_z: float = 20.0      # 4.0 mm tall circular anti-slip retaining lip
    rs30_seat_d: float = 198.4
    rs30_lip_outer_d: float = 207.0

    side_by_side_dx: float = 295.0    # 107.7 + 166.5 + 20.8 mm safety gap in Scheme C
    n_angles: int = 360               # Exact 1° angular resolution!


def asym_rounded_square_radius(theta: float, half_w: float, cr_front: float, cr_rear: float) -> float:
    """
    Exact ray radius from (0,0) to [-half_w, half_w]^2 where:
      - Front half (y >= 0, sin(theta) >= 0) uses corner radius cr_front
      - Rear half  (y <  0, sin(theta) <  0) uses corner radius cr_rear
    Since both halves share the exact flat side |x| = half_w near y = 0, this is C^infinity across y = 0!
    """
    cr = cr_front if math.sin(theta) >= 0.0 else cr_rear
    ct = abs(math.cos(theta))
    st = abs(math.sin(theta))
    c = half_w - cr
    if ct > 1e-9 and (half_w * (st / ct)) <= c:
        return half_w / ct
    if st > 1e-9 and (half_w * (ct / st)) <= c:
        return half_w / st
    b = c * (ct + st)
    disc = max(0.0, b * b - (2.0 * c * c - cr * cr))
    return b + math.sqrt(disc)


def is_v3_pillar_slice(k: int, n_angles: int = 360) -> bool:
    """
    Defines the 4 structural columns in polar angle degrees (0° = +X Right, 90° = +Y Front, 180° = -X Left, 270° = -Y Rear):
      - Front-Right Portal Column: [20°, 43°]   -> inner wall lies 100% on flat plane X = +99.7 mm (front window 43°..137° is 199.4mm wide!)
      - Front-Left  Portal Column: [137°, 160°] -> inner wall lies 100% on flat plane X = -99.7 mm
      - Rear-Left   Backstop Col : [198°, 232°] -> wraps R31.6 rear corner (22.8mm backstop) to auto-stop Mac Studio on slide-in
      - Rear-Right  Backstop Col : [308°, 342°] -> wraps R31.6 rear corner (leaves 232°..308° = 153.8mm wide rear port & power-btn window!)
    """
    deg = (k * 360.0) / n_angles
    return (
        (20.0 <= deg < 43.0)
        or (137.0 <= deg < 160.0)
        or (198.0 <= deg < 232.0)
        or (308.0 <= deg < 342.0)
    )


class MeshBuilder:
    """Builds indexed triangle meshes and verifies strict 2-manifold watertightness."""

    def __init__(self) -> None:
        self.verts: list[tuple[float, float, float]] = []
        self.vert_map: dict[tuple[int, int, int], int] = {}
        self.tris: list[tuple[int, int, int]] = []

    def add_vert(self, x: float, y: float, z: float) -> int:
        key = (round(x * 10000), round(y * 10000), round(z * 10000))
        idx = self.vert_map.get(key)
        if idx is None:
            idx = len(self.verts)
            self.verts.append((key[0] / 10000.0, key[1] / 10000.0, key[2] / 10000.0))
            self.vert_map[key] = idx
        return idx

    def add_tri(self, i0: int, i1: int, i2: int) -> None:
        if i0 != i1 and i1 != i2 and i2 != i0:
            self.tris.append((i0, i1, i2))

    def add_quad(self, p00: int, p10: int, p11: int, p01: int) -> None:
        self.add_tri(p00, p10, p11)
        self.add_tri(p00, p11, p01)

    def revolve_sector_profiles(self, thetas, sector_types, profile_fn, cheek_triangulator) -> None:
        n = len(thetas)
        for k in range(n):
            k_next = (k + 1) % n
            t0, t1 = thetas[k], thetas[k_next]
            st = sector_types[k]
            prof0 = profile_fn(t0, st)
            prof1 = profile_fn(t1, st)
            m = len(prof0)
            v0 = [self.add_vert(r * math.cos(t0), r * math.sin(t0), z) for (r, z) in prof0]
            v1 = [self.add_vert(r * math.cos(t1), r * math.sin(t1), z) for (r, z) in prof1]
            for i in range(m):
                i_next = (i + 1) % m
                self.add_quad(v0[i], v1[i], v1[i_next], v0[i_next])
            k_prev = (k - 1) % n
            if sector_types[k_prev] != sector_types[k]:
                cheek_triangulator(self, t0, sector_types[k_prev], sector_types[k])

    def verify_and_stats(self) -> dict:
        directed_edges: dict[tuple[int, int], int] = {}
        for (a, b, c) in self.tris:
            for u, v in ((a, b), (b, c), (c, a)):
                directed_edges[(u, v)] = directed_edges.get((u, v), 0) + 1

        duplicate_half_edges = sum(1 for cnt in directed_edges.values() if cnt != 1)
        unmatched_half_edges = sum(1 for (u, v) in directed_edges if (v, u) not in directed_edges)

        verts_np = np.array(self.verts, dtype=np.float64)
        tris_np = np.array(self.tris, dtype=np.int32)
        v0 = verts_np[tris_np[:, 0]]
        v1 = verts_np[tris_np[:, 1]]
        v2 = verts_np[tris_np[:, 2]]
        cross = np.cross(v1 - v0, v2 - v0)
        vol_mm3 = float(np.sum(np.einsum("ij,ij->i", v0, cross)) / 6.0)
        area_mm2 = float(0.5 * np.sum(np.linalg.norm(cross, axis=1)))
        mins = verts_np.min(axis=0)
        maxs = verts_np.max(axis=0)
        dims = maxs - mins

        shell_vol_mm3 = min(vol_mm3, area_mm2 * 1.45 * 0.64)
        infill_vol_mm3 = max(0.0, vol_mm3 - shell_vol_mm3) * 0.30
        effective_fdm_cm3 = (shell_vol_mm3 + infill_vol_mm3) / 1000.0
        solid_cm3 = vol_mm3 / 1000.0

        return {
            "vertices": len(self.verts),
            "triangles": len(self.tris),
            "is_watertight_2manifold": (duplicate_half_edges == 0 and unmatched_half_edges == 0 and vol_mm3 > 0),
            "duplicate_half_edges": duplicate_half_edges,
            "unmatched_half_edges": unmatched_half_edges,
            "bbox_mm": [round(float(d), 2) for d in dims],
            "solid_volume_cm3": round(solid_cm3, 2),
            "surface_area_cm2": round(area_mm2 / 100.0, 2),
            "fdm_effective_cm3_30pct": round(effective_fdm_cm3, 2),
            "mass_petg_fdm_g": round(effective_fdm_cm3 * 1.27, 1),
            "mass_jlc_solid_petg_g": round(solid_cm3 * 1.27, 1),
            "mass_sls_pa12_g": round(solid_cm3 * 1.01, 1),
        }

    def write_binary_stl(self, path: Path, header_text: str) -> None:
        verts_np = np.array(self.verts, dtype=np.float32)
        tris_np = np.array(self.tris, dtype=np.int32)
        v0 = verts_np[tris_np[:, 0]]
        v1 = verts_np[tris_np[:, 1]]
        v2 = verts_np[tris_np[:, 2]]
        normals = np.cross(v1 - v0, v2 - v0)
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = np.divide(normals, np.maximum(norms, 1e-12))

        header = header_text.encode("ascii", errors="ignore")[:80].ljust(80, b" ")
        with path.open("wb") as f:
            f.write(header)
            f.write(struct.pack("<I", len(self.tris)))
            for i in range(len(self.tris)):
                nx, ny, nz = normals[i]
                ax, ay, az = v0[i]
                bx, by, bz = v1[i]
                cx, cy, cz = v2[i]
                f.write(
                    struct.pack(
                        "<12fH",
                        float(nx), float(ny), float(nz),
                        float(ax), float(ay), float(az),
                        float(bx), float(by), float(bz),
                        float(cx), float(cy), float(cz),
                        0,
                    )
                )


def v3_radii(theta: float, p: DockParams) -> tuple[float, float, float]:
    """Returns (r_rail, r_pock, r_out) at angle theta for the V3 Front-Slide Cassette Portal."""
    pocket_half = p.mac_w / 2.0 + p.mac_side_clearance       # 99.7 mm
    rear_pock_cr = p.mac_corner_r + p.mac_side_clearance     # 31.6 mm
    front_pock_cr = 1.0                                      # Straight portal sides |X| = 99.7 mm up to Y = 98.7 mm!

    outer_half = pocket_half + p.wall_thickness              # 107.7 mm (215.4 mm outer)
    rear_out_cr = rear_pock_cr + p.wall_thickness            # 39.6 mm
    front_out_cr = 12.0                                      # Smooth rounded outer front corners

    # Inner foot/rail boundary: straight |X| = 91.2 mm in front (clears Ø179.2mm foot sliding in!), rounded R24 in rear
    r_rail = asym_rounded_square_radius(theta, p.rail_inner_half, cr_front=3.5, cr_rear=24.0)
    r_pock = asym_rounded_square_radius(theta, pocket_half, cr_front=front_pock_cr, cr_rear=rear_pock_cr)
    r_out = asym_rounded_square_radius(theta, outer_half, cr_front=front_out_cr, cr_rear=rear_out_cr)
    return r_rail, r_pock, r_out


def build_module1_base_cradle(p: DockParams) -> MeshBuilder:
    """
    Module 1 (V3): Front-Loading Slide-In Cassette Cradle & Heavy-Duty Exoskeleton Portal
    - Mac Studio slides straight in/out through the +Y front portal (199.4 mm clear width x 105.0 mm height)
      on two 8.5 mm wide horizontal rails (|X| = 91.2..99.7 mm at Z = 26.0 mm) WITHOUT touching the RS30 on top!
    """
    mb = MeshBuilder()
    z_ring = p.base_ring_h                                         # 6.0 mm
    z_shelf = p.shelf_z                                            # 26.0 mm
    z_col_top = p.shelf_z + p.mac_body_h + p.air_gap_above_mac     # 131.0 mm
    z_tenon_top = z_col_top + p.tenon_h                            # 139.0 mm

    thetas = [2.0 * math.pi * k / p.n_angles for k in range(p.n_angles)]
    sector_types = [1 if is_v3_pillar_slice(k, p.n_angles) else 0 for k in range(p.n_angles)]

    def profile_fn(theta: float, st: int) -> list[tuple[float, float]]:
        r_rail, r_pock, r_out = v3_radii(theta, p)
        if st == 0:
            return [(r_rail, 0.0), (r_out, 0.0), (r_out, z_ring), (r_rail, z_ring)]
        r_t_in = r_pock + p.tenon_inset
        r_t_out = r_out - p.tenon_inset
        return [
            (r_rail, 0.0),
            (r_out, 0.0),
            (r_out, z_ring),
            (r_out, z_shelf),
            (r_out, z_col_top),
            (r_t_out, z_col_top),
            (r_t_out, z_tenon_top),
            (r_t_in, z_tenon_top),
            (r_t_in, z_col_top),
            (r_pock, z_col_top),
            (r_pock, z_shelf),
            (r_rail, z_shelf),
            (r_rail, z_ring),
        ]

    def cheek_triangulator(builder: MeshBuilder, theta: float, st_prev: int, st_curr: int) -> None:
        r_rail, r_pock, r_out = v3_radii(theta, p)
        r_t_in = r_pock + p.tenon_inset
        r_t_out = r_out - p.tenon_inset
        ct, st_sin = math.cos(theta), math.sin(theta)

        def v(r: float, z: float) -> int:
            return builder.add_vert(r * ct, r * st_sin, z)

        flip = (st_prev == 1 and st_curr == 0)
        a0, a1 = v(r_rail, z_ring), v(r_out, z_ring)
        b0, b1, b2 = v(r_rail, z_shelf), v(r_pock, z_shelf), v(r_out, z_shelf)
        c0, c1, c2, c3 = v(r_pock, z_col_top), v(r_t_in, z_col_top), v(r_t_out, z_col_top), v(r_out, z_col_top)
        d0, d1 = v(r_t_in, z_tenon_top), v(r_t_out, z_tenon_top)

        tris_ccw = [
            (a0, a1, b2), (a0, b2, b1), (a0, b1, b0),
            (b1, b2, c3), (b1, c3, c2), (b1, c2, c1), (b1, c1, c0),
            (c1, c2, d1), (c1, d1, d0),
        ]
        for t in tris_ccw:
            builder.add_tri(t[0], t[1], t[2]) if not flip else builder.add_tri(t[0], t[2], t[1])

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, cheek_triangulator)
    return mb


def build_module2_upper_deck(p: DockParams) -> MeshBuilder:
    """
    Module 2 (V3): 16mm Heavy-Duty Support-Free Bridge Deck matching V3 Front-Slide Portal Tenons
    """
    mb = MeshBuilder()
    r_bolt = p.rs30_bolt_hole_d / 2.0
    r_cone_bot = 13.5
    z_cone_top = 10.0
    r_seat = p.rs30_seat_d / 2.0
    r_lip_out = p.rs30_lip_outer_d / 2.0

    z_seat = p.deck_seat_z
    z_lip_top = p.deck_lip_top_z
    z_outer = p.deck_outer_z
    z_m_wall = p.tenon_h + 0.5

    thetas = [2.0 * math.pi * k / p.n_angles for k in range(p.n_angles)]
    sector_types = [1 if is_v3_pillar_slice(k, p.n_angles) else 0 for k in range(p.n_angles)]

    def mortise_radii(theta: float) -> tuple[float, float, float, float, float]:
        _, r_pock, r_out = v3_radii(theta, p)
        r_m_in = r_pock + (p.tenon_inset - p.tenon_tol)
        r_m_out = r_out - (p.tenon_inset - p.tenon_tol)
        r_m_mid = 0.5 * (r_m_in + r_m_out)
        z_m_peak = min(z_outer - 1.2, z_m_wall + 0.5 * (r_m_out - r_m_in))
        return r_out, r_m_in, r_m_mid, r_m_out, z_m_peak

    def profile_fn(theta: float, st: int) -> list[tuple[float, float]]:
        r_out, r_m_in, r_m_mid, r_m_out, z_m_peak = mortise_radii(theta)
        top_chain = [
            (r_out, z_outer),
            (r_lip_out, z_outer),
            (r_lip_out, z_lip_top),
            (r_seat, z_lip_top),
            (r_seat, z_seat),
            (r_bolt, z_seat),
        ]
        if st == 0:
            return [
                (r_bolt, z_cone_top), (r_cone_bot, 0.0),
                (r_m_in, 0.0), (r_m_mid, 0.0), (r_m_out, 0.0), (r_out, 0.0),
                *top_chain,
            ]
        return [
            (r_bolt, z_cone_top), (r_cone_bot, 0.0),
            (r_m_in, 0.0), (r_m_in, z_m_wall), (r_m_mid, z_m_peak), (r_m_out, z_m_wall), (r_m_out, 0.0), (r_out, 0.0),
            *top_chain,
        ]

    def cheek_triangulator(builder: MeshBuilder, theta: float, st_prev: int, st_curr: int) -> None:
        _, r_m_in, r_m_mid, r_m_out, z_m_peak = mortise_radii(theta)
        ct, st_sin = math.cos(theta), math.sin(theta)

        def v(r: float, z: float) -> int:
            return builder.add_vert(r * ct, r * st_sin, z)

        flip = (st_prev == 0 and st_curr == 1)
        b0, b1, b2 = v(r_m_in, 0.0), v(r_m_mid, 0.0), v(r_m_out, 0.0)
        w0, wp, w2 = v(r_m_in, z_m_wall), v(r_m_mid, z_m_peak), v(r_m_out, z_m_wall)
        for t in ((b0, b1, wp), (b0, wp, w0), (b1, b2, w2), (b1, w2, wp)):
            builder.add_tri(t[0], t[1], t[2]) if not flip else builder.add_tri(t[0], t[2], t[1])

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, cheek_triangulator)
    return mb


def build_annular_box_cage(
    outer_w: float,
    outer_d: float,
    outer_cr: float,
    wall: float,
    height: float,
    floor_h: float,
    window_half_steps: int = 8,
    n_angles: int = 128,
) -> MeshBuilder:
    mb = MeshBuilder()
    oh_x, oh_y = outer_w / 2.0, outer_d / 2.0
    ih_x, ih_y = oh_x - wall, oh_y - wall
    icr = max(2.0, outer_cr - wall)

    def rect_ray(theta: float, hx: float, hy: float, cr: float) -> float:
        ct, st = abs(math.cos(theta)), abs(math.sin(theta))
        cx, cy = hx - cr, hy - cr
        if ct > 1e-9 and (hx * st / ct) <= cy:
            return hx / ct
        if st > 1e-9 and (hy * ct / st) <= cx:
            return hy / st
        b = cx * ct + cy * st
        disc = max(0.0, b * b - (cx * cx + cy * cy - cr * cr))
        return b + math.sqrt(disc)

    thetas = [2.0 * math.pi * k / n_angles for k in range(n_angles)]
    q = n_angles // 4
    sector_types = [0 if ((k % q) < window_half_steps or (k % q) >= q - window_half_steps) else 1 for k in range(n_angles)]

    def profile_fn(theta: float, st: int) -> list[tuple[float, float]]:
        ro = rect_ray(theta, oh_x, oh_y, outer_cr)
        ri = rect_ray(theta, ih_x, ih_y, icr)
        if st == 1:
            return [(ri, 0.0), (ro, 0.0), (ro, floor_h), (ro, height), (ri, height), (ri, floor_h)]
        return [(ri, 0.0), (ro, 0.0), (ro, floor_h), (ri, floor_h)]

    def cheek_triangulator(builder: MeshBuilder, theta: float, st_prev: int, st_curr: int) -> None:
        ro = rect_ray(theta, oh_x, oh_y, outer_cr)
        ri = rect_ray(theta, ih_x, ih_y, icr)
        ct, st_sin = math.cos(theta), math.sin(theta)

        def v(r: float, z: float) -> int:
            return builder.add_vert(r * ct, r * st_sin, z)

        flip = (st_prev == 1 and st_curr == 0)
        p00, p10, p11, p01 = v(ri, floor_h), v(ro, floor_h), v(ro, height), v(ri, height)
        builder.add_quad(p00, p10, p11, p01) if not flip else builder.add_quad(p00, p01, p11, p10)

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, cheek_triangulator)
    return mb


def build_module4_dust_filter_frame(p: DockParams) -> MeshBuilder:
    mb = MeshBuilder()
    half_w, cr, r_hole, r_lip, h_total, h_lip, n = 90.0, 18.0, 82.0, 86.0, 3.2, 1.6, 128
    thetas = [2.0 * math.pi * k / n for k in range(n)]
    sector_types = [0] * n

    def profile_fn(theta: float, _st: int) -> list[tuple[float, float]]:
        ro = asym_rounded_square_radius(theta, half_w, cr, cr)
        return [(r_hole, 0.0), (ro, 0.0), (ro, h_total), (r_lip, h_total), (r_lip, h_lip), (r_hole, h_lip)]

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, lambda *_: None)
    return mb


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "stl"
    out_dir.mkdir(parents=True, exist_ok=True)
    params = DockParams()

    modules = [
        ("01_mac_studio_base_cradle.stl", "StudioBeam V3 Front-Slide Cradle", build_module1_base_cradle(params)),
        ("02_rs30_gimbal_upper_deck.stl", "StudioBeam V3 16mm Bridge Deck", build_module2_upper_deck(params)),
        (
            "03_power_brick_cable_pod.stl",
            "StudioBeam V3 Side Power Pod",
            build_annular_box_cage(
                outer_w=params.brick_t + 16.0,
                outer_d=params.brick_w + 16.0,
                outer_cr=14.0,
                wall=6.0,
                height=params.brick_h + 10.0,
                floor_h=8.0,
            ),
        ),
        ("04_bottom_dust_filter_frame.stl", "StudioBeam V3 Dust Filter Frame", build_module4_dust_filter_frame(params)),
    ]

    # Verify exact slide-in clearance at front portal (theta = 43° and 137°)
    t_front_edge = math.radians(43.0)
    r_rail_43, r_pock_43, _ = v3_radii(t_front_edge, params)
    front_portal_clear_w = round(2.0 * r_pock_43 * math.cos(t_front_edge), 2)
    front_foot_channel_w = round(2.0 * r_rail_43 * math.cos(t_front_edge), 2)
    t_rear_edge = math.radians(232.0)
    _, r_pock_232, _ = v3_radii(t_rear_edge, params)
    rear_port_window_w = round(2.0 * abs(r_pock_232 * math.cos(t_rear_edge)), 2)

    report = {
        "version": "3.0-front-slide-cassette-portal",
        "parameters_mm": asdict(params),
        "engineering_verification": {
            "front_slide_in_portal_width_mm": front_portal_clear_w,
            "mac_studio_body_width_mm": params.mac_w,
            "front_foot_channel_width_mm": front_foot_channel_w,
            "mac_studio_foot_diameter_mm": params.mac_intake_d,
            "rear_port_and_power_btn_window_mm": rear_port_window_w,
            "rs30_mass_kg": 5.4,
            "deck_solid_bridge_thickness_mm": params.deck_seat_z,
            "scheme_c_min_360_gap_mm": round(params.side_by_side_dx - (params.mac_w / 2 + params.mac_side_clearance + params.wall_thickness) - params.rs30_swept_r, 1),
        },
        "modules": {},
    }
    total_fdm_g = 0.0
    total_solid_g = 0.0
    total_sls_g = 0.0

    for fname, title, builder in modules:
        stl_path = out_dir / fname
        builder.write_binary_stl(stl_path, title)
        stats = builder.verify_and_stats()
        stats["file"] = str(stl_path)
        stats["file_size_kb"] = round(stl_path.stat().st_size / 1024.0, 1)
        assert stats["is_watertight_2manifold"], f"Mesh {fname} failed 2-manifold check: {stats}"
        assert max(stats["bbox_mm"]) <= 250.0, f"Mesh {fname} exceeds 256mm Bambu bed: {stats['bbox_mm']}"
        report["modules"][fname] = stats
        total_fdm_g += stats["mass_petg_fdm_g"]
        total_solid_g += stats["mass_jlc_solid_petg_g"]
        total_sls_g += stats["mass_sls_pa12_g"]

    assert front_portal_clear_w >= params.mac_w + 2.0, f"Front portal too narrow: {front_portal_clear_w}"
    assert front_foot_channel_w >= params.mac_intake_d + 2.0, f"Foot channel too narrow: {front_foot_channel_w}"

    report["totals"] = {
        "total_fdm_petg_30pct_infill_g": round(total_fdm_g, 1),
        "core_2_modules_fdm_petg_g": round(
            report["modules"]["01_mac_studio_base_cradle.stl"]["mass_petg_fdm_g"]
            + report["modules"]["02_rs30_gimbal_upper_deck.stl"]["mass_petg_fdm_g"],
            1,
        ),
        "total_solid_petg_equiv_g": round(total_solid_g, 1),
        "total_sls_pa12_nylon_g": round(total_sls_g, 1),
    }

    manifest_path = Path(__file__).resolve().parent / "cad_manifest.json"
    manifest_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
