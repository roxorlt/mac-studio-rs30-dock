// ============================================================================
// StudioBeam DuoDock V3 — Front-Slide Cassette Portal Parametric OpenSCAD Source
// M5 Mac Studio (197x197x95 mm, R30.4, Base Intake Ø179.2 mm)
// + XGIMI RS30 Pro / Pro Max / Ultra / Ultra Max (298x249x190 mm, 5.4 kg)
//
// V3 Upgrade: Front-Loading Slide-In Cassette Bay (+Y full 199.4mm clear portal)
// Mac Studio slides straight in/out from the front on side rails WITHOUT moving RS30!
// ============================================================================

$fn = 96;

mac_w          = 197.0;
mac_body_h     = 87.0;
mac_corner_r   = 30.4;
mac_clearance  = 1.2;    // Pocket width = 199.4 mm (> 197.0 mm Mac Studio)
rail_inner_w   = 182.4;  // > Ø179.2 mm circular bottom foot -> 8.5 mm wide side rails
wall_t         = 8.0;    // Outer width = 215.4 mm (<= 256 mm Bambu bed)
base_ring_h    = 6.0;    // 12 mm below Mac Studio Z=18 mm foot bottom
shelf_z        = 26.0;
air_gap_h      = 18.0;
tenon_h        = 8.0;
tenon_inset    = 1.9;
tenon_tol      = 0.25;

deck_seat_z    = 16.0;
deck_outer_z   = 15.0;
deck_lip_top_z = 20.0;
rs30_seat_d    = 198.4;
rs30_lip_out_d = 207.0;
rs30_bolt_d    = 7.0;

part_mode      = "assembly"; // "assembly", "m1_base", "m2_deck", "m3_power_pod", "m4_dust_frame"

pocket_w  = mac_w + 2 * mac_clearance;        // 199.4 mm
pocket_cr = mac_corner_r + mac_clearance;     // 31.6 mm
outer_w   = pocket_w + 2 * wall_t;            // 215.4 mm
outer_cr  = pocket_cr + wall_t;               // 39.6 mm
col_top_z = shelf_z + mac_body_h + air_gap_h; // 131.0 mm

// Asymmetric 2D profile: curved R_rear in -Y half, straight slide-in portal in +Y half
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
    // 1. Full-width 199.4mm front slide-in portal (+Y)
    translate([0, 90]) square([pocket_w - tol_extra, 180], center = true);
    // 2. Rear 152mm wide port & power-button window (-Y)
    translate([0, -90]) square([153.8 - tol_extra, 180], center = true);
    // 3. Left & Right 72mm side ventilation windows (±X)
    square([300, 72.0 - tol_extra], center = true);
}

// Module 1 (V3): Front-Slide Cassette Cradle & Exoskeleton Portal
module m1_base_cradle() {
    union() {
        // 1. 6mm bed tie-frame (sits 12mm below Mac Studio's bottom foot)
        linear_extrude(base_ring_h)
            difference() {
                asym_box2d(outer_w, 12.0, outer_cr);
                asym_box2d(rail_inner_w, 3.5, 24.0);
            }
        // 2. Left/Right slide rails & rear pedestals (Z = 0..26mm)
        linear_extrude(shelf_z)
            difference() {
                asym_box2d(outer_w, 12.0, outer_cr);
                asym_box2d(rail_inner_w, 3.5, 24.0);
                // Keep full 182.4mm front foot entry channel open!
                translate([0, 90]) square([rail_inner_w, 180], center = true);
                translate([0, -90]) square([153.8, 180], center = true);
                square([300, 72.0], center = true);
            }
        // 3. Rear R31.6 backstop columns + Front straight portal columns (Z = 26..131mm)
        translate([0, 0, shelf_z])
            linear_extrude(col_top_z - shelf_z)
                difference() {
                    asym_box2d(outer_w, 12.0, outer_cr);
                    asym_box2d(pocket_w, 1.0, pocket_cr);
                    v3_window_cutters_2d(0);
                }
        // 4. Top alignment tenons
        translate([0, 0, col_top_z])
            linear_extrude(tenon_h)
                difference() {
                    asym_box2d(outer_w - 2 * tenon_inset, 10.0, outer_cr - tenon_inset);
                    asym_box2d(pocket_w + 2 * tenon_inset, 2.0, pocket_cr + tenon_inset);
                    v3_window_cutters_2d(-2);
                }
    }
}

// Module 2 (V3): 16mm Heavy-Duty Bridge Deck matching V3 Portal Tenons
module m2_upper_deck() {
    difference() {
        union() {
            linear_extrude(deck_outer_z)
                asym_box2d(outer_w, 12.0, outer_cr);
            cylinder(h = deck_lip_top_z, d = rs30_lip_out_d);
        }
        translate([0, 0, deck_seat_z])
            cylinder(h = deck_lip_top_z, d = rs30_seat_d);
        translate([0, 0, -0.5])
            cylinder(h = deck_lip_top_z + 1, d = rs30_bolt_d);
        translate([0, 0, -0.01])
            cylinder(h = 10.01, d1 = 27.0, d2 = rs30_bolt_d);
        translate([0, 0, -0.1])
            linear_extrude(tenon_h + 0.6)
                difference() {
                    asym_box2d(outer_w - 2 * (tenon_inset - tenon_tol), 10.0, outer_cr - (tenon_inset - tenon_tol));
                    asym_box2d(pocket_w + 2 * (tenon_inset - tenon_tol), 2.0, pocket_cr + (tenon_inset - tenon_tol));
                    v3_window_cutters_2d(2);
                }
    }
}

module m3_power_pod() {
    pod_w = 60.0; pod_d = 204.0; pod_h = 102.0;
    difference() {
        linear_extrude(pod_h) offset(r = 14) square([pod_w - 28, pod_d - 28], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) offset(r = 8) square([pod_w - 28, pod_d - 28], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) {
            square([pod_w + 4, 120], center = true);
            square([28, pod_d + 4], center = true);
        }
    }
}

module m4_dust_frame() {
    difference() {
        linear_extrude(3.2) offset(r = 18) square([180 - 36, 180 - 36], center = true);
        translate([0, 0, -0.5]) cylinder(h = 4.2, d = 164.0);
        translate([0, 0, 1.6]) cylinder(h = 2.0, d = 172.0);
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
    translate([0, 0, 10]) m4_dust_frame();
}
