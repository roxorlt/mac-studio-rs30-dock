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

    # Power brick bay (XGIMI RS30 180W-330W external DC adapter; M5 Mac Studio PSU is internal!)
    # Flagship 300W-330W brick measures up to 200 x 90 x 40 mm (~1.05-1.2 kg) with AC/DC cords at both ends
    brick_w: float = 208.0            # 208mm inner length (> 200mm brick; 220mm outer <= 256mm Bambu bed!)
    brick_t: float = 48.0             # 48mm inner width (fits 40-44mm brick + convection air gap; 60mm outer)
    brick_h: float = 94.0             # 94mm inner wall height above 8mm base (102mm total height wraps 90mm brick)

    # V3.2 Full Self-Audit Clearances, Dual-Tier Rails & 4x M4 Positive Anti-Lift Pillar Locks (mm)
    mac_side_clearance: float = 1.8   # 197.0 + 2*1.8 = 200.6 mm portal (leaves 1.6mm net play WITH 2x1.0mm velvet strips!)
    base_intake_half: float = 87.0    # 174.0 mm Z=0..6mm 360° bed frame -> forms physical Z=6mm shelf under 181mm dust filter!
    rail_inner_half: float = 91.5     # 183.0 mm Z=6..26mm channel (> 181mm filter & > Ø179.2mm Mac circular foot!)
    wall_thickness: float = 8.0       # 8.0 mm heavy-duty pillar wall -> 216.6 x 216.6 mm outer (fits 256mm bed!)
    base_ring_h: float = 6.0          # 6.0 mm continuous bed frame & physical slide ledge for M4 dust filter
    shelf_z: float = 26.0             # Upper slide-rail Z height for Mac Studio (foot sits at Z=18mm, 8.8mm above filter!)
    air_gap_above_mac: float = 18.0   # 18 mm cool air plenum above Mac Studio
    tenon_h: float = 8.5              # 8.5 mm deep alignment tenons
    tenon_inset: float = 1.35         # Leaves >= 5.3mm tenon width around 4x M4 corner locking screw bores
    tenon_tol: float = 0.25
    m4_lock_bore_r: float = 1.9       # ~3.8mm M4 self-threading / heat-set pilot bore in M1 pillars (24mm deep)
    m4_clear_r: float = 2.2           # ~4.4mm M4 clearance hole through M2 corner mortise roof
    m4_cb_r: float = 4.1              # ~8.2mm recessed M4 screw head counterbore in M2 outer Z=14mm terrace

    # V3.2 Raised Pedestal Upper Deck + Recessed Flat Counterbore (mm)
    deck_seat_z: float = 17.0         # 17.0 mm solid center bridge pedestal boss
    deck_outer_z: float = 14.0        # Stepped DOWN 3.0 mm outside Ø176mm so rotating U-arms have +3~4mm air gap!
    rs30_pedestal_d: float = 176.0    # Raised flat pedestal boss (< Ø196mm base -> zero cup-lip rub or diameter mismatch!)
    cb_depth_z: float = 8.5           # 8.5 mm recessed flat washer seat (hides D-ring head for Scheme C + 8.5mm clamp!)
    cb_flat_d: float = 26.0           # Ø26 mm flat bearing shoulder for 1/4"-20 D-ring screw head
    cb_mouth_d: float = 43.0          # Ø43 mm 45° two-finger bevel access

    side_by_side_dx: float = 296.0    # 108.3 + 166.5 + 21.2 mm safety gap in Scheme C
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


def v3_radii(theta: float, p: DockParams) -> tuple[float, float, float, float]:
    """Returns (r_base, r_rail, r_pock, r_out) at angle theta for the V3.1 Dual-Rail Cassette Portal."""
    pocket_half = p.mac_w / 2.0 + p.mac_side_clearance       # 100.3 mm (200.6 mm bare portal; 198.6 mm w/ velvet!)
    rear_pock_cr = p.mac_corner_r + p.mac_side_clearance     # 32.2 mm
    front_pock_cr = 1.0                                      # Straight portal sides |X| = 100.3 mm!

    outer_half = pocket_half + p.wall_thickness              # 108.3 mm (216.6 mm outer)
    rear_out_cr = rear_pock_cr + p.wall_thickness            # 40.2 mm
    front_out_cr = 12.0

    r_base = asym_rounded_square_radius(theta, p.base_intake_half, cr_front=14.0, cr_rear=22.0)
    r_rail = asym_rounded_square_radius(theta, p.rail_inner_half, cr_front=3.5, cr_rear=24.0)
    r_pock = asym_rounded_square_radius(theta, pocket_half, cr_front=front_pock_cr, cr_rear=rear_pock_cr)
    r_out = asym_rounded_square_radius(theta, outer_half, cr_front=front_out_cr, cr_rear=rear_out_cr)
    return r_base, r_rail, r_pock, r_out


def v3_sector_type(k: int, n_angles: int = 360) -> int:
    """
    Returns sector type for each 1° polar slice:
      0 = open window (front portal, side windows, rear I/O window)
      1 = solid structural pillar + alignment tenon/mortise
      2 = enclosed center M4 anti-lift locking bolt bore inside each of the 4 pillars:
          - Front-Right center: [31°, 33°)   (R ~ 122.3 mm, outside Ø196mm RS30 base!)
          - Front-Left  center: [147°, 149°) (R ~ 122.3 mm, outside Ø196mm RS30 base!)
          - Rear-Left   center: [214°, 216°) (R ~ 126.4 mm, outside Ø196mm RS30 base!)
          - Rear-Right  center: [324°, 326°) (R ~ 126.4 mm, outside Ø196mm RS30 base!)
    """
    deg = (k * 360.0) / n_angles
    if (
        (31.0 <= deg < 33.0)
        or (147.0 <= deg < 149.0)
        or (214.0 <= deg < 216.0)
        or (324.0 <= deg < 326.0)
    ):
        return 2
    if is_v3_pillar_slice(k, n_angles):
        return 1
    return 0


def build_module1_base_cradle(p: DockParams) -> MeshBuilder:
    """
    Module 1 (V3.2): Dual-Tier Front-Slide Cassette Cradle + 4x M4 Anti-Lift Pillar Lock Bores
      - Tier 1 (Z = 6.0 mm): Physical slide ledge (174mm hole, 183mm channel) supporting M4 dust filter front pull-out!
      - Tier 2 (Z = 26.0 mm): Velvet-ready horizontal slide rails (200.6mm front portal) for Mac Studio!
      - 4x Blind M4 pilot/insert bores (Z = 115.5..139.5 mm) centered in the 4 corner tenons to bolt M2 solidly to M1!
    """
    mb = MeshBuilder()
    z_ring = p.base_ring_h                                         # 6.0 mm
    z_shelf = p.shelf_z                                            # 26.0 mm
    z_col_top = p.shelf_z + p.mac_body_h + p.air_gap_above_mac     # 131.0 mm
    z_tenon_top = z_col_top + p.tenon_h                            # 139.5 mm
    z_bore_bot = z_tenon_top - 24.0                                # 115.5 mm (24mm deep blind M4 bore!)

    thetas = [2.0 * math.pi * k / p.n_angles for k in range(p.n_angles)]
    sector_types = [v3_sector_type(k, p.n_angles) for k in range(p.n_angles)]

    def bore_radii(theta: float) -> tuple[float, float, float, float, float, float, float, float]:
        r_base, r_rail, r_pock, r_out = v3_radii(theta, p)
        r_t_in = r_pock + p.tenon_inset
        r_t_out = r_out - p.tenon_inset
        r_mid = 0.5 * (r_t_in + r_t_out)
        r_b_in = r_mid - p.m4_lock_bore_r
        r_b_out = r_mid + p.m4_lock_bore_r
        return r_base, r_rail, r_pock, r_out, r_t_in, r_t_out, r_b_in, r_b_out

    def profile_fn(theta: float, st: int) -> list[tuple[float, float]]:
        r_base, r_rail, r_pock, r_out, r_t_in, r_t_out, r_b_in, r_b_out = bore_radii(theta)
        if st == 0:
            return [
                (r_base, 0.0),
                (r_out, 0.0),
                (r_out, z_ring),
                (r_rail, z_ring),
                (r_base, z_ring),
            ]
        top_tenon_chain = (
            [(r_b_out, z_tenon_top), (r_b_in, z_tenon_top)]
            if st == 1
            else [(r_b_out, z_tenon_top), (r_b_out, z_bore_bot), (r_b_in, z_bore_bot), (r_b_in, z_tenon_top)]
        )
        return [
            (r_base, 0.0),
            (r_out, 0.0),
            (r_out, z_ring),
            (r_out, z_shelf),
            (r_out, z_col_top),
            (r_t_out, z_col_top),
            (r_t_out, z_tenon_top),
            *top_tenon_chain,
            (r_t_in, z_tenon_top),
            (r_t_in, z_col_top),
            (r_pock, z_col_top),
            (r_pock, z_shelf),
            (r_rail, z_shelf),
            (r_rail, z_ring),
            (r_base, z_ring),
        ]

    def cheek_triangulator(builder: MeshBuilder, theta: float, st_prev: int, st_curr: int) -> None:
        _, r_rail, r_pock, r_out, r_t_in, r_t_out, r_b_in, r_b_out = bore_radii(theta)
        ct, st_sin = math.cos(theta), math.sin(theta)

        def v(r: float, z: float) -> int:
            return builder.add_vert(r * ct, r * st_sin, z)

        if {st_prev, st_curr} == {1, 2}:
            flip_bore = (st_prev == 1 and st_curr == 2)
            q00, q10, q11, q01 = v(r_b_in, z_bore_bot), v(r_b_out, z_bore_bot), v(r_b_out, z_tenon_top), v(r_b_in, z_tenon_top)
            builder.add_quad(q00, q10, q11, q01) if not flip_bore else builder.add_quad(q00, q01, q11, q10)
            return

        flip = (st_prev == 1 and st_curr == 0)
        a0, a1 = v(r_rail, z_ring), v(r_out, z_ring)
        b0, b1, b2 = v(r_rail, z_shelf), v(r_pock, z_shelf), v(r_out, z_shelf)
        c0, c1, c2, c3 = v(r_pock, z_col_top), v(r_t_in, z_col_top), v(r_t_out, z_col_top), v(r_out, z_col_top)
        d0, db_in, db_out, d1 = v(r_t_in, z_tenon_top), v(r_b_in, z_tenon_top), v(r_b_out, z_tenon_top), v(r_t_out, z_tenon_top)

        tris_ccw = [
            (a0, a1, b2), (a0, b2, b1), (a0, b1, b0),
            (b1, b2, c3), (b1, c3, c2), (b1, c2, c1), (b1, c1, c0),
            (c1, c2, d1), (c1, d1, db_out), (c1, db_out, db_in), (c1, db_in, d0),
        ]
        for t in tris_ccw:
            builder.add_tri(t[0], t[1], t[2]) if not flip else builder.add_tri(t[0], t[2], t[1])

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, cheek_triangulator)
    return mb


def build_module2_upper_deck(p: DockParams) -> MeshBuilder:
    """
    Module 2 (V3.2): Raised Ø176mm Pedestal Deck + Recessed D-Ring Counterbore + 4x M4 Corner Lock Holes
      - Center 1/4"-20 bolt hole + flat Ø26mm recessed washer seat clamps RS30's turntable base rigidly onto M2.
      - 4x Recessed M4 countersunk/cap-screw through-holes at R=122-126mm (outside RS30's Ø196mm base!) bolt M2
        positively down onto M1's 4 corner pillars so tilting the stiff gimbal never lifts M2!
    """
    mb = MeshBuilder()
    r_bolt = p.rs30_bolt_hole_d / 2.0
    r_cb_flat = p.cb_flat_d / 2.0
    r_cb_mouth = p.cb_mouth_d / 2.0
    z_cb = p.cb_depth_z

    r_ped = p.rs30_pedestal_d / 2.0
    z_seat = p.deck_seat_z
    z_outer = p.deck_outer_z
    r_ped_chamf = r_ped + (z_seat - z_outer)
    z_m_wall = p.tenon_h + 0.5
    z_m4_cb = z_outer - 2.6   # 11.4 mm recessed M4 head shoulder (hides screw head flush below Z=14mm!)

    thetas = [2.0 * math.pi * k / p.n_angles for k in range(p.n_angles)]
    sector_types = [v3_sector_type(k, p.n_angles) for k in range(p.n_angles)]

    def mortise_radii(theta: float):
        _, _, r_pock, r_out = v3_radii(theta, p)
        r_m_in = r_pock + (p.tenon_inset - p.tenon_tol)
        r_m_out = r_out - (p.tenon_inset - p.tenon_tol)
        r_m_mid = 0.5 * (r_m_in + r_m_out)
        r_h_in = r_m_mid - p.m4_clear_r
        r_h_out = r_m_mid + p.m4_clear_r
        r_c_in = max(r_ped_chamf + 1.5, r_m_mid - p.m4_cb_r)
        r_c_out = min(r_out - 1.2, r_m_mid + p.m4_cb_r)
        # Roof slope height at r_h_in / r_h_out (symmetric around r_m_mid)
        slope = min(1.8, z_m4_cb - 1.4 - z_m_wall)
        z_m_peak = z_m_wall + max(0.4, slope)
        frac = (r_h_in - r_m_in) / max(1e-6, (r_m_mid - r_m_in))
        z_h_roof = z_m_wall + frac * (z_m_peak - z_m_wall)
        return r_out, r_m_in, r_m_mid, r_m_out, z_m_peak, r_h_in, r_h_out, r_c_in, r_c_out, z_h_roof

    def loops_for_slice(theta: float, st: int) -> list[list[tuple[float, float]]]:
        r_out, r_m_in, r_m_mid, r_m_out, z_m_peak, r_h_in, r_h_out, r_c_in, r_c_out, z_h_roof = mortise_radii(theta)
        bot_center = [(r_bolt, z_cb), (r_cb_flat, z_cb), (r_cb_mouth, 0.0)]
        top_inner = [(r_ped_chamf, z_outer), (r_ped, z_seat), (r_bolt, z_seat)]
        if st == 0:
            return [[
                *bot_center,
                (r_m_in, 0.0), (r_m_mid, 0.0), (r_m_out, 0.0), (r_out, 0.0),
                (r_out, z_outer), (r_c_out, z_outer), (r_c_in, z_outer),
                *top_inner,
            ]]
        if st == 1:
            return [[
                *bot_center,
                (r_m_in, 0.0), (r_m_in, z_m_wall), (r_h_in, z_h_roof), (r_m_mid, z_m_peak),
                (r_h_out, z_h_roof), (r_m_out, z_m_wall), (r_m_out, 0.0), (r_out, 0.0),
                (r_out, z_outer), (r_c_out, z_outer), (r_c_in, z_outer),
                *top_inner,
            ]]
        # st == 2: Two closed loops separated by the M4 through-hole + recessed counterbore!
        loop_inner = [
            *bot_center,
            (r_m_in, 0.0), (r_m_in, z_m_wall), (r_h_in, z_h_roof),
            (r_h_in, z_m4_cb), (r_c_in, z_m4_cb), (r_c_in, z_outer),
            *top_inner,
        ]
        loop_outer = [
            (r_m_out, 0.0), (r_out, 0.0), (r_out, z_outer),
            (r_c_out, z_outer), (r_c_out, z_m4_cb), (r_h_out, z_m4_cb),
            (r_h_out, z_h_roof), (r_m_out, z_m_wall),
        ]
        return [loop_inner, loop_outer]

    n = len(thetas)
    for k in range(n):
        k_next = (k + 1) % n
        t0, t1 = thetas[k], thetas[k_next]
        st = sector_types[k]
        l0 = loops_for_slice(t0, st)
        l1 = loops_for_slice(t1, st)
        for loop0, loop1 in zip(l0, l1):
            m = len(loop0)
            v0 = [mb.add_vert(r * math.cos(t0), r * math.sin(t0), z) for (r, z) in loop0]
            v1 = [mb.add_vert(r * math.cos(t1), r * math.sin(t1), z) for (r, z) in loop1]
            for i in range(m):
                i_next = (i + 1) % m
                mb.add_quad(v0[i], v1[i], v1[i_next], v0[i_next])

        k_prev = (k - 1) % n
        st_prev = sector_types[k_prev]
        if st_prev != st:
            _, r_m_in, r_m_mid, r_m_out, z_m_peak, r_h_in, r_h_out, r_c_in, r_c_out, z_h_roof = mortise_radii(t0)
            ct, st_sin = math.cos(t0), math.sin(t0)

            def v(r: float, z: float) -> int:
                return mb.add_vert(r * ct, r * st_sin, z)

            if {st_prev, st} == {0, 1}:
                flip = (st_prev == 0 and st == 1)
                b0, b1, b2 = v(r_m_in, 0.0), v(r_m_mid, 0.0), v(r_m_out, 0.0)
                w0, wh_in, wp, wh_out, w2 = (
                    v(r_m_in, z_m_wall), v(r_h_in, z_h_roof), v(r_m_mid, z_m_peak),
                    v(r_h_out, z_h_roof), v(r_m_out, z_m_wall),
                )
                tris = (
                    (b0, b1, wp), (b0, wp, wh_in), (b0, wh_in, w0),
                    (b1, b2, w2), (b1, w2, wh_out), (b1, wh_out, wp),
                )
                for tri in tris:
                    mb.add_tri(tri[0], tri[1], tri[2]) if not flip else mb.add_tri(tri[0], tri[2], tri[1])
            elif {st_prev, st} == {1, 2}:
                # Solid bridge cheek closing the M4 shaft + counterbore between st==1 and st==2
                flip_h = (st_prev == 2 and st == 1)
                rh0, rhm, rh1 = v(r_h_in, z_h_roof), v(r_m_mid, z_m_peak), v(r_h_out, z_h_roof)
                sh0, sh1 = v(r_h_in, z_m4_cb), v(r_h_out, z_m4_cb)
                cb0, cb1, ct0, ct1 = v(r_c_in, z_m4_cb), v(r_c_out, z_m4_cb), v(r_c_in, z_outer), v(r_c_out, z_outer)
                tris_h = (
                    (rh0, sh0, sh1), (rh0, sh1, rh1), (rh0, rh1, rhm),
                    (cb0, ct0, ct1), (cb0, ct1, cb1),
                )
                # Note: wait — sh0/sh1 lie on segment cb0..cb1! Avoid T-junction on z_m4_cb by splitting along sh0/sh1:
                tris_h_exact = (
                    (rh0, sh0, sh1), (rh0, sh1, rh1), (rh0, rh1, rhm),
                    (cb0, ct0, ct1), (cb0, ct1, sh1), (cb0, sh1, sh0), (sh1, ct1, cb1),
                )
                for tri in tris_h_exact:
                    mb.add_tri(tri[0], tri[1], tri[2]) if not flip_h else mb.add_tri(tri[0], tri[2], tri[1])

    return mb


def build_power_brick_pod(p: DockParams) -> MeshBuilder:
    """
    Module 3 (V3.2): Dual-End U-Slotted Power Brick Cradle for XGIMI RS30 180W-330W Adapter
      - Inner cavity: 208.0 (L) x 48.0 (W) x 94.0 (H) mm -> fits flagship 200 x 90 x 40 mm (~1.1 kg) brick!
      - Outer bbox: 220.0 (L) x 60.0 (W) x 102.0 (H) mm (<= 256 mm Bambu bed!)
      - 4 wrap-around corner L-columns retain the brick longitudinally, while 32mm wide top-open U-slots on BOTH
        +Y and -Y ends let thick AC-in (IEC C13) and DC-out cords + strain-relief boots drop straight in from above!
      - Dual side ventilation windows separated by a solid center rib keep the 300W brick cool with zero wall flex.
    """
    mb = MeshBuilder()
    wall = 6.0
    floor_h = 8.0
    height = p.brick_h + floor_h         # 102.0 mm
    oh_x = p.brick_t / 2.0 + wall        # 30.0 mm (60.0 mm outer width)
    oh_y = p.brick_w / 2.0 + wall        # 110.0 mm (220.0 mm outer length)
    ih_x = p.brick_t / 2.0               # 24.0 mm (48.0 mm inner width)
    ih_y = p.brick_w / 2.0               # 104.0 mm (208.0 mm inner length)
    outer_cr = 12.0
    icr = 6.0

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

    # Exact transition angles so end U-slots are |x| < 15.5 mm on +/-Y ends (retaining 8.5mm corner hooks on each side!)
    # and side vent windows are |y| in (20.0, 74.0) mm on +/-X sides (leaving a 40mm center rib + 36mm corner L-walls!)
    end_slot_half_x = 15.5
    vent_y_lo, vent_y_hi = 20.0, 74.0

    raw_angles: set[float] = set()
    for k in range(360):
        raw_angles.add(round(2.0 * math.pi * k / 360.0, 8))
    # Add exact boundary rays for crisp orthogonal window/slot cheeks
    a_end = math.atan2(oh_y, end_slot_half_x)     # ~81.98° from +X
    a_vlo = math.atan2(vent_y_lo, oh_x)           # ~33.69° from +X
    a_vhi = math.atan2(vent_y_hi, oh_x)           # ~67.93° from +X
    for base in (0.0, math.pi):
        for ang in (a_vlo, a_vhi, a_end, math.pi - a_end, math.pi - a_vhi, math.pi - a_vlo):
            raw_angles.add(round((base + ang) % (2.0 * math.pi), 8))

    thetas = sorted(raw_angles)
    sector_types: list[int] = []
    for k in range(len(thetas)):
        t_mid = 0.5 * (thetas[k] + (thetas[k + 1] if k + 1 < len(thetas) else 2.0 * math.pi))
        ro_m = rect_ray(t_mid, oh_x, oh_y, outer_cr)
        xm, ym = abs(ro_m * math.cos(t_mid)), abs(ro_m * math.sin(t_mid))
        is_end_uslot = (ym > oh_y - 2.0) and (xm < end_slot_half_x - 1e-4)
        is_side_vent = (xm > oh_x - 2.0) and (vent_y_lo + 1e-4 < ym < vent_y_hi - 1e-4)
        sector_types.append(0 if (is_end_uslot or is_side_vent) else 1)

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
    """181 x 181 x 3.2 mm dust filter frame resting on M1's Z=6mm physical ledge (174mm inner, 183mm outer)."""
    mb = MeshBuilder()
    half_w, cr_f, cr_r, r_hole, r_lip, h_total, h_lip, n = 90.5, 4.0, 24.5, 81.0, 85.5, 3.2, 1.6, 128
    thetas = [2.0 * math.pi * k / n for k in range(n)]
    sector_types = [0] * n

    def profile_fn(theta: float, _st: int) -> list[tuple[float, float]]:
        ro = asym_rounded_square_radius(theta, half_w, cr_f, cr_r)
        return [(r_hole, 0.0), (ro, 0.0), (ro, h_total), (r_lip, h_total), (r_lip, h_lip), (r_hole, h_lip)]

    mb.revolve_sector_profiles(thetas, sector_types, profile_fn, lambda *_: None)
    return mb


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "stl"
    out_dir.mkdir(parents=True, exist_ok=True)
    params = DockParams()

    modules = [
        ("01_mac_studio_base_cradle.stl", "StudioBeam V3.2 Locked Cradle", build_module1_base_cradle(params)),
        ("02_rs30_gimbal_upper_deck.stl", "StudioBeam V3.2 Locked Pedestal", build_module2_upper_deck(params)),
        ("03_power_brick_cable_pod.stl", "StudioBeam V3.2 208mm PSU Pod", build_power_brick_pod(params)),
        ("04_bottom_dust_filter_frame.stl", "StudioBeam V3.2 Dust Filter", build_module4_dust_filter_frame(params)),
    ]

    t_front_edge = math.radians(43.0)
    _, r_rail_43, r_pock_43, _ = v3_radii(t_front_edge, params)
    front_portal_clear_w = round(2.0 * r_pock_43 * math.cos(t_front_edge), 2)
    front_foot_channel_w = round(2.0 * r_rail_43 * math.cos(t_front_edge), 2)
    t_rear_edge = math.radians(232.0)
    _, _, r_pock_232, _ = v3_radii(t_rear_edge, params)
    rear_port_window_w = round(2.0 * abs(r_pock_232 * math.cos(t_rear_edge)), 2)

    report = {
        "version": "3.2-psu208-m4lock-cablesim",
        "parameters_mm": asdict(params),
        "engineering_verification": {
            "front_slide_in_portal_bare_mm": front_portal_clear_w,
            "front_slide_in_portal_with_velvet_mm": round(front_portal_clear_w - 2.0, 2),
            "mac_studio_body_width_mm": params.mac_w,
            "front_foot_and_filter_channel_mm": front_foot_channel_w,
            "mac_studio_foot_diameter_mm": params.mac_intake_d,
            "dust_filter_width_mm": 181.0,
            "dust_filter_ledge_hole_mm": params.base_intake_half * 2.0,
            "rear_port_and_power_btn_window_mm": rear_port_window_w,
            "rs30_pedestal_boss_d_mm": params.rs30_pedestal_d,
            "rs30_u_arm_step_down_clearance_mm": round(params.deck_seat_z - params.deck_outer_z, 1),
            "thumbscrew_clamp_thickness_mm": round(params.deck_seat_z - params.cb_depth_z, 1),
            "m4_pillar_lock_bolts": "4x M4x25mm recessed corner bolts at R=122.3mm (front) & R=126.4mm (rear)",
            "psu_pod_inner_cavity_mm": [params.brick_w, params.brick_t, params.brick_h],
            "psu_pod_dual_end_uslot_width_mm": 31.0,
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
