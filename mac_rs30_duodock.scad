// ============================================================================
// StudioBeam DuoDock V3.1 — Full Engineering Self-Audit OpenSCAD Source
// M5 Mac Studio (197x197x95 mm, R30.4, Base Intake Ø179.2 mm)
// + XGIMI RS30 Pro / Pro Max / Ultra / Ultra Max (298x249x190 mm, 5.4 kg)
//
// V3.1 Upgrades:
//   1. 200.6mm bare front portal (198.6mm net with 2x1.0mm velvet strips)
//   2. Dual-tier stepped shelves: Z=6mm physical dust-filter slide ledge + Z=26mm Mac slide rail
//   3. Ø176mm raised flat pedestal boss (steps down 3mm outside Ø176mm -> zero U-arm lip rub!)
//   4. Recessed flat Ø26mm thumbscrew counterbore at Z=8.5mm (fits standard 14mm D-ring screw!)
// ============================================================================

$fn = 96;

mac_w          = 197.0;
mac_body_h     = 87.0;
mac_corner_r   = 30.4;
mac_clearance  = 1.8;    // Pocket width = 200.6 mm (198.6 mm net after 2x1mm velvet!)
base_intake_w  = 174.0;  // Z=0..6mm 360° frame -> physical Z=6mm shelf under 181mm filter!
rail_inner_w   = 183.0;  // > 181mm filter & > Ø179.2mm Mac circular foot
wall_t         = 8.0;    // Outer width = 216.6 mm (<= 256 mm Bambu bed)
base_ring_h    = 6.0;
shelf_z        = 26.0;
air_gap_h      = 18.0;
tenon_h        = 8.5;
tenon_inset    = 1.9;
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
    union() {
        // Tier 0: 6mm continuous bed frame & physical Z=6mm slide shelf for M4 dust filter
        linear_extrude(base_ring_h)
            difference() {
                asym_box2d(outer_w, 12.0, outer_cr);
                asym_box2d(base_intake_w, 14.0, 22.0);
            }
        // Tier 1: Z=6..26mm slide rails (183mm channel clears 181mm filter & Ø179.2mm Mac foot)
        translate([0, 0, base_ring_h])
            linear_extrude(shelf_z - base_ring_h)
                difference() {
                    asym_box2d(outer_w, 12.0, outer_cr);
                    asym_box2d(rail_inner_w, 3.5, 24.0);
                    translate([0, 90]) square([rail_inner_w, 180], center = true);
                    translate([0, -90]) square([154.8, 180], center = true);
                    square([300, 74.0], center = true);
                }
        // Tier 2: Z=26..131mm front portal + rear R32.2 curved backstop columns
        translate([0, 0, shelf_z])
            linear_extrude(col_top_z - shelf_z)
                difference() {
                    asym_box2d(outer_w, 12.0, outer_cr);
                    asym_box2d(pocket_w, 1.0, pocket_cr);
                    v3_window_cutters_2d(0);
                }
        // Top tenons (8.5mm tall)
        translate([0, 0, col_top_z])
            linear_extrude(tenon_h)
                difference() {
                    asym_box2d(outer_w - 2 * tenon_inset, 10.0, outer_cr - tenon_inset);
                    asym_box2d(pocket_w + 2 * tenon_inset, 2.0, pocket_cr + tenon_inset);
                    v3_window_cutters_2d(-2);
                }
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
    }
}

module m3_power_pod() {
    pod_w = 62.0; pod_d = 204.0; pod_h = 102.0;
    difference() {
        linear_extrude(pod_h) offset(r = 14) square([pod_w - 28, pod_d - 28], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) offset(r = 8) square([pod_w - 24, pod_d - 24], center = true);
        translate([0, 0, 8]) linear_extrude(pod_h) {
            square([pod_w + 4, 120], center = true);
            square([30, pod_d + 4], center = true);
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
    translate([-(outer_w / 2 + 35), 0, 0]) m3_power_pod();
    translate([0, 0, base_ring_h]) m4_dust_frame();
}
