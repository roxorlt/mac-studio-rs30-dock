// ============================================================================
// StudioBeam DuoDock V3.2 — Parametric OpenSCAD Source
// M5 Mac Studio (197x197x95 mm, R30.4, Base Intake Ø179.2 mm, Internal PSU)
// + XGIMI RS30 Series (298x249x190 mm, 5.4 kg, External 200x90x40 mm PSU)
//
// V3.2 Upgrades:
//   1. 200.6mm bare front portal (198.6mm net with 2x1.0mm velvet strips)
//   2. Dual-tier stepped shelves: Z=6mm dust-filter slide ledge + Z=26mm Mac slide rail
//   3. Ø176mm raised flat pedestal + recessed Ø26mm 1/4"-20 D-ring screw counterbore
//   4. 4x M4x25mm recessed corner locking bolts (outside Ø196mm RS30 base!) bolting M2 solidly to M1
//   5. Enlarged 208x48x94mm inner cavity (220x60x102mm outer) dual-end U-slotted RS30 PSU pod
// ============================================================================

$fn = 96;

mac_w          = 197.0;
mac_body_h     = 87.0;
mac_corner_r   = 30.4;
mac_clearance  = 1.8;
base_intake_w  = 174.0;
rail_inner_w   = 183.0;
wall_t         = 8.0;
base_ring_h    = 6.0;
shelf_z        = 26.0;
air_gap_h      = 18.0;
tenon_h        = 8.5;
tenon_inset    = 1.35;
tenon_tol      = 0.25;

deck_seat_z    = 17.0;
deck_outer_z   = 14.0;
rs30_ped_d     = 176.0;
rs30_bolt_d    = 7.0;

part_mode      = "assembly";

pocket_w  = mac_w + 2 * mac_clearance;        // 200.6 mm
pocket_cr = mac_corner_r + mac_clearance;     // 32.2 mm
outer_w   = pocket_w + 2 * wall_t;            // 216.6 mm
outer_cr  = pocket_cr + wall_t;               // 40.2 mm
col_top_z = shelf_z + mac_body_h + air_gap_h; // 131.0 mm

// 4 corner pillar lock centers (all R = 122..126 mm > RS30 Ø196mm base R=98mm!)
lock_pts = [
    [ 104.3,  65.0],
    [-104.3,  65.0],
    [-103.5, -72.5],
    [ 103.5, -72.5]
];

module asym_box2d(w, cr_front, cr_rear) {
    intersection() {
        offset(r = cr_front) square([w - 2 * cr_front, w - 2 * cr_front], center = true);
        translate([0, w / 2]) square([w + 4, w], center = true);
    }
    intersection() {
        offset(r = cr_rear) square([w - 2 * cr_rear, w - 2 * cr_rear], center = true);
        translate([0, -w / 2]) square([w + 4, w], center = true);
    }
}

module v3_window_cutters_2d(tol_extra = 0) {
    translate([0, 90]) square([pocket_w - tol_extra, 180], center = true);
    translate([0, -90]) square([154.8 - tol_extra, 180], center = true);
    square([300, 74.0 - tol_extra], center = true);
}

module m1_base_cradle() {
    difference() {
        union() {
            linear_extrude(base_ring_h)
                difference() {
                    asym_box2d(outer_w, 12.0, outer_cr);
                    asym_box2d(base_intake_w, 14.0, 22.0);
                }
            translate([0, 0, base_ring_h])
                linear_extrude(shelf_z - base_ring_h)
                    difference() {
                        asym_box2d(outer_w, 12.0, outer_cr);
                        asym_box2d(rail_inner_w, 3.5, 24.0);
                        translate([0, 90]) square([rail_inner_w, 180], center = true);
                        translate([0, -90]) square([154.8, 180], center = true);
                        square([300, 74.0], center = true);
                    }
            translate([0, 0, shelf_z])
                linear_extrude(col_top_z - shelf_z)
                    difference() {
                        asym_box2d(outer_w, 12.0, outer_cr);
                        asym_box2d(pocket_w, 1.0, pocket_cr);
                        v3_window_cutters_2d(0);
                    }
            translate([0, 0, col_top_z])
                linear_extrude(tenon_h)
                    difference() {
                        asym_box2d(outer_w - 2 * tenon_inset, 10.0, outer_cr - tenon_inset);
                        asym_box2d(pocket_w + 2 * tenon_inset, 2.0, pocket_cr + tenon_inset);
                        v3_window_cutters_2d(-2);
                    }
        }
        // 4x M4 blind pilot / heat-set nut bores (24mm deep)
        for (pt = lock_pts)
            translate([pt[0], pt[1], col_top_z + tenon_h - 24.0])
                cylinder(h = 25.0, d = 3.8);
    }
}

module m2_upper_deck() {
    difference() {
        union() {
            linear_extrude(deck_outer_z)
                asym_box2d(outer_w, 12.0, outer_cr);
            cylinder(h = deck_seat_z, d1 = rs30_ped_d + 2 * (deck_seat_z - deck_outer_z), d2 = rs30_ped_d);
        }
        translate([0, 0, -0.5])
            cylinder(h = deck_seat_z + 1, d = rs30_bolt_d);
        translate([0, 0, -0.01])
            cylinder(h = 8.51, d1 = 43.0, d2 = 26.0);
        translate([0, 0, -0.1])
            linear_extrude(tenon_h + 0.6)
                difference() {
                    asym_box2d(outer_w - 2 * (tenon_inset - tenon_tol), 10.0, outer_cr - (tenon_inset - tenon_tol));
                    asym_box2d(pocket_w + 2 * (tenon_inset - tenon_tol), 2.0, pocket_cr + (tenon_inset - tenon_tol));
                    v3_window_cutters_2d(2);
                }
        // 4x M4 through-holes + recessed counterbores in Z=14mm outer corners
        for (pt = lock_pts) {
            translate([pt[0], pt[1], -0.5]) cylinder(h = deck_outer_z + 1.0, d = 4.4);
            translate([pt[0], pt[1], deck_outer_z - 2.6]) cylinder(h = 3.0, d = 8.2);
        }
    }
}

module m3_power_pod() {
    // Fits XGIMI RS30 180W-330W external power brick (up to 200 x 90 x 40 mm, ~1.1 kg)
    // Inner cavity: 208 x 48 x 94 mm; Dual-end 31mm top-open U-slots for AC & DC cord strain-relief boots
    pod_w = 60.0; pod_d = 220.0; pod_h = 102.0;
    difference() {
        linear_extrude(pod_h) offset(r = 12) square([pod_w - 24, pod_d - 24], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) offset(r = 6) square([pod_w - 12 - 12, pod_d - 12 - 12], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) {
            square([31.0, pod_d + 8], center = true);            // Dual-end open U-slots for AC C13 & DC boots
            translate([0,  47]) square([pod_w + 8, 54], center = true); // Front-half side cooling vents
            translate([0, -47]) square([pod_w + 8, 54], center = true); // Rear-half side cooling vents
        }
    }
}

module m4_dust_frame() {
    difference() {
        linear_extrude(3.2) asym_box2d(181.0, 4.0, 24.5);
        translate([0, 0, -0.5]) cylinder(h = 4.2, d = 162.0);
        translate([0, 0, 1.6]) cylinder(h = 2.0, d = 171.0);
    }
}

if (part_mode == "m1_base") m1_base_cradle();
else if (part_mode == "m2_deck") m2_upper_deck();
else if (part_mode == "m3_power_pod") m3_power_pod();
else if (part_mode == "m4_dust_frame") m4_dust_frame();
else {
    m1_base_cradle();
    translate([0, 0, col_top_z + 18]) m2_upper_deck();
    translate([-(outer_w / 2 + 34), 0, 0]) m3_power_pod();
    translate([0, 0, base_ring_h]) m4_dust_frame();
}
