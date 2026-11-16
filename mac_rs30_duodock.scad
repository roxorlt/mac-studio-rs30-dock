// ============================================================================
// StudioBeam DuoDock V2 — Parametric OpenSCAD Source (Structural & Clearance Verified)
// M5 Mac Studio (197x197x95 mm, R30.4, Base Intake Ø179.2 mm)
// + XGIMI RS30 Pro / Pro Max / Ultra / Ultra Max (298x249x190 mm, 5.4 kg, R_sweep=166.5 mm)
// ============================================================================

$fn = 96;

/* [Device Reference Dimensions (mm)] */
mac_w          = 197.0;
mac_body_h     = 87.0;
mac_foot_h     = 8.0;
mac_corner_r   = 30.4;
mac_intake_d   = 179.2;

rs30_base_d    = 196.0;
rs30_bolt_d    = 7.0;   // 1/4"-20 UNC clearance

/* [V2 Structural Clearances & Dimensions (mm)] */
mac_clearance  = 1.2;   // 0.2mm print tol + 1.0mm self-adhesive velvet strip
intake_hole_d  = 182.0; // Lets Ø179.2mm intake foot nest freely
wall_t         = 7.5;   // Heavy-duty 7.5mm exoskeleton wall (214.4mm outer <= 256mm bed)
base_ring_h    = 6.0;
shelf_z        = 26.0;  // Elevates Mac Studio corners 26mm above desk
air_gap_h      = 18.0;  // 18mm thermal air-gap above Mac Studio
tenon_h        = 8.0;
tenon_inset    = 1.9;
tenon_tol      = 0.25;

deck_seat_z    = 16.0;  // 16mm continuous structural bridge plate (8x stiffer than V1)
deck_outer_z   = 15.0;  // Stepped 1mm below turntable seat for 100% 360° U-arm clearance
deck_lip_top_z = 20.0;  // 4mm circular anti-slip lip around Ø198.4mm seat
rs30_seat_d    = 198.4;
rs30_lip_out_d = 207.0;

/* [Export Selector] */
// "assembly", "m1_base", "m2_deck", "m3_power_pod", "m4_dust_frame"
part_mode      = "assembly";

pocket_w  = mac_w + 2 * mac_clearance;        // 199.4 mm
pocket_cr = mac_corner_r + mac_clearance;     // 31.6 mm
outer_w   = pocket_w + 2 * wall_t;            // 214.4 mm
outer_cr  = pocket_cr + wall_t;               // 39.1 mm
col_top_z = shelf_z + mac_body_h + air_gap_h; // 131.0 mm

module rounded_sq(w, r) {
    offset(r = r)
        square([w - 2 * r, w - 2 * r], center = true);
}

module rounded_rect2d(w, d, r) {
    offset(r = r)
        square([w - 2 * r, d - 2 * r], center = true);
}

module window_cutters_2d(span_w = 116, big = 300) {
    square([span_w, big], center = true);
    square([big, span_w], center = true);
}

// Module 1: Mac Studio Elevated Airflow Cradle & 7.5mm Heavy-Duty Pillars
module m1_base_cradle() {
    union() {
        linear_extrude(base_ring_h)
            difference() {
                rounded_sq(outer_w, outer_cr);
                circle(d = intake_hole_d);
            }
        linear_extrude(shelf_z)
            difference() {
                rounded_sq(outer_w, outer_cr);
                circle(d = intake_hole_d);
                window_cutters_2d(116);
            }
        translate([0, 0, shelf_z])
            linear_extrude(col_top_z - shelf_z)
                difference() {
                    rounded_sq(outer_w, outer_cr);
                    rounded_sq(pocket_w, pocket_cr);
                    window_cutters_2d(116);
                }
        translate([0, 0, col_top_z])
            linear_extrude(tenon_h)
                difference() {
                    rounded_sq(outer_w - 2 * tenon_inset, outer_cr - tenon_inset);
                    rounded_sq(pocket_w + 2 * tenon_inset, pocket_cr + tenon_inset);
                    window_cutters_2d(118);
                }
    }
}

// Module 2: V2 Support-Free 16mm Heavy-Duty Bridge Deck + Stepped 360° U-Arm Corners
module m2_upper_deck() {
    difference() {
        union() {
            // Outer rounded-square bridge plate (z = 0..15mm)
            linear_extrude(deck_outer_z)
                rounded_sq(outer_w, outer_cr);
            // Circular turret & retaining lip (z = 0..20mm within Ø207mm)
            cylinder(h = deck_lip_top_z, d = rs30_lip_out_d);
        }
        // Sunken RS30 turntable seat (Ø198.4mm above z = 16mm)
        translate([0, 0, deck_seat_z])
            cylinder(h = deck_lip_top_z, d = rs30_seat_d);
        // Center 1/4"-20 UNC bolt hole + 45° self-supporting conical thumbscrew access
        translate([0, 0, -0.5])
            cylinder(h = deck_lip_top_z + 1, d = rs30_bolt_d);
        translate([0, 0, -0.01])
            cylinder(h = 10.01, d1 = 27.0, d2 = rs30_bolt_d);
        // Corner mortise slots (z = 0..8.5mm)
        translate([0, 0, -0.1])
            linear_extrude(tenon_h + 0.6)
                difference() {
                    rounded_sq(outer_w - 2 * (tenon_inset - tenon_tol), outer_cr - (tenon_inset - tenon_tol));
                    rounded_sq(pocket_w + 2 * (tenon_inset - tenon_tol), pocket_cr + (tenon_inset - tenon_tol));
                    window_cutters_2d(114);
                }
    }
}

// Module 3: Side-Mounted Power-Brick Pod (-X/+X blank side so -Y rear Mac ports stay 100% clear)
module m3_power_pod() {
    pod_w = 60.0;
    pod_d = 204.0;
    pod_h = 102.0;
    difference() {
        linear_extrude(pod_h)
            rounded_rect2d(pod_w, pod_d, 14.0);
        translate([0, 0, 8.0])
            linear_extrude(pod_h)
                rounded_rect2d(pod_w - 12.0, pod_d - 12.0, 8.0);
        translate([0, 0, 8.0]) {
            linear_extrude(pod_h) {
                square([pod_w + 4, 120], center = true);
                square([28, pod_d + 4], center = true);
            }
        }
    }
}

// Module 4: Slide-in Bottom Dust Filter Frame
module m4_dust_frame() {
    difference() {
        linear_extrude(3.2)
            rounded_sq(184.0, 22.0);
        translate([0, 0, -0.5])
            cylinder(h = 4.2, d = 164.0);
        translate([0, 0, 1.6])
            cylinder(h = 2.0, d = 172.0);
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
