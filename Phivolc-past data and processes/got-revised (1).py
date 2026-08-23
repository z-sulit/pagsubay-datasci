# --- Epicenter-by-Triplets (uniform PDF; recalculated excludes outlier points; N/E formatting) ---
import itertools
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# PDF deps
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Map deps (optional)
try:
    import folium
    from folium import Circle, Marker
    from folium.plugins import MarkerCluster
    FOLIUM_AVAILABLE = True
except Exception:
    FOLIUM_AVAILABLE = False

# ---------- OUTPUT LOCATION ----------
# Save results into: C:\Users\<you>\Documents\EpicenterReports
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "EpicenterReports")

# ---------------------------------------------------------------------------

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two (lat, lon) points in kilometers."""
    R = 6371.0088  # mean Earth radius (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(a))

def ensure_output_dir(path_like: str) -> str:
    """Return a writable directory path; create it if needed; fallback to CWD on failure."""
    if not path_like:
        return os.getcwd()
    try:
        os.makedirs(path_like, exist_ok=True)
        return path_like
    except Exception as e:
        print(f"[WARN] Could not create output dir ({e}). Falling back to CWD.")
        return os.getcwd()

# --------- Formatting helpers (N/S, E/W) ----------
def format_lat(lat):
    if lat is None:
        return "—"
    hemi = "N" if lat >= 0 else "S"
    return f"{abs(lat):.6f}° {hemi}"

def format_lon(lon):
    if lon is None:
        return "—"
    hemi = "E" if lon >= 0 else "W"
    return f"{abs(lon):.6f}° {hemi}"

def kmfmt(v):
    return f"{v:,.3f} km" if v is not None else "—"

def build_radii_stats(center_H, center_K, coords_seq):
    """
    coords_seq: iterable of (lat, lon) pairs in the order you want reported.
    Returns: (radii_deg, radii_km, R_min_deg, R_min_km, R_max_deg, R_max_km, R_mean_deg, R_std_deg)
    """
    coords_list = list(coords_seq)
    if len(coords_list) == 0:
        return [], [], None, None, None, None, None, None

    radii_deg = [np.sqrt((center_H - x)**2 + (center_K - y)**2) for (x, y) in coords_list]

    # min/max (in km) use the actual sites that produce min/max
    R_min_deg, R_max_deg = float(np.min(radii_deg)), float(np.max(radii_deg))
    min_idx = int(np.argmin(radii_deg))
    max_idx = int(np.argmax(radii_deg))
    (x_min, y_min) = coords_list[min_idx]
    (x_max, y_max) = coords_list[max_idx]
    R_min_km = haversine_km(center_H, center_K, x_min, y_min)
    R_max_km = haversine_km(center_H, center_K, x_max, y_max)

    R_mean_deg = float(np.mean(radii_deg))
    R_std_deg  = float(np.std(radii_deg))

    radii_km = [haversine_km(center_H, center_K, x, y) for (x, y) in coords_list]
    return radii_deg, radii_km, R_min_deg, R_min_km, R_max_deg, R_max_km, R_mean_deg, R_std_deg

def main():
    # --------- I/O SETUP ---------
    out_dir = ensure_output_dir(OUTPUT_DIR)
    pdf_filename  = os.path.join(out_dir, "epicenter_report.pdf")
    map_filename  = os.path.join(out_dir, "epicenter_map.html")
    fig_filename  = os.path.join(out_dir, "epicenter_figure.png")  # save the 3-panel plot

    print("CURRENT WORKING DIRECTORY:", os.getcwd())
    print("OUTPUT DIRECTORY:", out_dir)

    # --------- INPUTS ---------
    n = int(input("Enter the number of data points n: "))
    points = [f"P{i}" for i in range(1, n+1)]
    combinations = list(itertools.combinations(points, 3))

    coordinates = {}
    for i in range(1, n+1):
        x, y = map(float, input(f"Enter the coordinates for P{i} (x{i} y{i}): ").split())
        coordinates[f"P{i}"] = (x, y)

    Hmeasured, Kmeasured = map(float, input("Enter the measured epicenter (Hmeasured Kmeasured): ").split())

    # --------- (h,k) from all triplets ---------
    h_k_values = []
    for combo in combinations:
        P1, P2, P3 = combo
        x1, y1 = coordinates[P1]; x2, y2 = coordinates[P2]; x3, y3 = coordinates[P3]
        a = (y2 - y3) * (x2**2 - x1**2 + y2**2 - y1**2) - (y2 - y1) * (x2**2 - x3**2 + y2**2 - y3**2)
        b = (x2 - x1) * (x2**2 - x3**2 + y2**2 - y3**2) - (x2 - x3) * (x2**2 - x1**2 + y2**2 - y1**2)
        c = 2 * (x2 - x1) * (y2 - y3) - 2 * (x2 - x3) * (y2 - y1)
        if c != 0:
            h = a / c; k = b / c
            h_k_values.append((combo, h, k))
            print(f"The value of h, k of {P1}, {P2}, {P3} is h={h}, k={k}")

    # --------- Approximate epicenter (uses ALL triplets) ---------
    all_h = [hk[1] for hk in h_k_values]
    all_k = [hk[2] for hk in h_k_values]
    H = float(np.mean(all_h)); K = float(np.mean(all_k))
    h_std = float(np.std(all_h)); k_std = float(np.std(all_k))

    print(f"\nApproximate Epicenter (H, K) = ({format_lat(H)}, {format_lon(K)})")
    print(f"Estimated spread of epicenter center: H ± {h_std:.6f}°, K ± {k_std:.6f}°")

    # Per-point radii + stats for (H,K) — include ALL points
    (radii_deg_all, radii_km_all, R_min_deg, R_min_km, R_max_deg, R_max_km,
     R_mean_deg, R_std_deg) = build_radii_stats(H, K, coordinates.values())

    for i, r in enumerate(radii_deg_all, start=1):
        print(f"R_{i} (deg) from P{i} to (H,K) = {r}")

    print(f"\nMin R (deg) = {R_min_deg}  (~{R_min_km:.3f} km)")
    print(f"Max R (deg) = {R_max_deg}  (~{R_max_km:.3f} km)")
    print(f"\nApproximate mean radius R_prox (deg) = {R_mean_deg}")
    print(f"Radius spread (std, deg) = {R_std_deg}")
    print("We can consider the standard deviation of radius as the proximity coefficient.")

    # Distance measured <-> approximate (km)
    dist_measured_to_HK_km = haversine_km(Hmeasured, Kmeasured, H, K)
    print(f"\nDistance between (Hmeasured, Kmeasured) and (H, K): {dist_measured_to_HK_km:.3f} km")

    # Absolute D
    measured_radii = [np.sqrt((Hmeasured - x)**2 + (Kmeasured - y)**2) for (x, y) in coordinates.values()]
    measured_radius_std = np.std(measured_radii)
    Absolute_D = abs(R_std_deg - measured_radius_std)
    print(f"Absolute D (|std(H,K) - std(Hmeasured,Kmeasured)| in deg) = {Absolute_D}")

    # --------- Triplet outliers & union of outlier points ---------
    h_outliers = [hk for hk in h_k_values if abs(hk[1] - H) > 3 * h_std]
    k_outliers = [hk for hk in h_k_values if abs(hk[2] - K) > 3 * k_std]
    outlier_combos = set(h_outliers + k_outliers)

    outlier_points = set()
    for combo, *_ in outlier_combos:
        outlier_points.update(combo)

    # Coordinates excluding outlier points (for recalculated Section 2 tables)
    coordinates_filtered = {p: xy for p, xy in coordinates.items() if p not in outlier_points}

    # --------- Recalculated epicenter (from filtered triplets) ---------
    filtered_h_k_values = [hk for hk in h_k_values if hk not in h_outliers and hk not in k_outliers]
    have_recalc = len(filtered_h_k_values) > 0 and len(coordinates_filtered) > 0

    H_r = K_r = None
    H_r_std = K_r_std = None
    (radii_r_deg, radii_r_km, Rr_min_deg, Rr_min_km, Rr_max_deg, Rr_max_km, Rr_mean_deg, Rr_std_deg) = \
        ([], [], None, None, None, None, None, None)
    dist_measured_to_HrKr_km = None

    if have_recalc:
        filt_h = [hk[1] for hk in filtered_h_k_values]
        filt_k = [hk[2] for hk in filtered_h_k_values]
        H_r = float(np.mean(filt_h)); K_r = float(np.mean(filt_k))
        H_r_std = float(np.std(filt_h)); K_r_std = float(np.std(filt_k))
        print(f"\nRecalculated Approximate Epicenter (H_r, K_r) = ({format_lat(H_r)}, {format_lon(K_r)})")
        print(f"Estimated spread (recalculated): H_r ± {H_r_std:.6f}°, K_r ± {K_r_std:.6f}°")

        # stats using ONLY non-outlier points
        (radii_r_deg, radii_r_km, Rr_min_deg, Rr_min_km, Rr_max_deg, Rr_max_km,
         Rr_mean_deg, Rr_std_deg) = build_radii_stats(H_r, K_r, coordinates_filtered.values())

        for idx, (pname) in enumerate(coordinates_filtered.keys(), start=1):
            print(f"Rr_{idx} (deg) from {pname} to (H_r,K_r) = {radii_r_deg[idx-1]}")

        print(f"\n(Recalculated) Min R (deg) = {Rr_min_deg}  (~{Rr_min_km:.3f} km)")
        print(f"(Recalculated) Max R (deg) = {Rr_max_deg}  (~{Rr_max_km:.3f} km)")

        dist_measured_to_HrKr_km = haversine_km(Hmeasured, Kmeasured, H_r, K_r)
        print(f"\nDistance between (Hmeasured, Kmeasured) and (H_r, K_r): {dist_measured_to_HrKr_km:.3f} km")

    # --------- Plots ----------
    fig, axs = plt.subplots(3, 1, figsize=(12, 8))

    # Original points
    axs[0].scatter(*zip(*coordinates.values()))
    for i, (x, y) in enumerate(coordinates.values(), start=1):
        axs[0].text(x, y, f"P{i}", fontsize=10)
    axs[0].set_title("Original Points")

    # Points with epicenters and approximate radius circles
    axs[1].scatter(*zip(*coordinates.values()))
    axs[1].scatter([H], [K], color='red', label="Approximate Epicenter (H, K)")
    axs[1].scatter([Hmeasured], [Kmeasured], color='green', label="Measured Epicenter (Hmeasured, Kmeasured)")
    if have_recalc:
        axs[1].scatter([H_r], [K_r], color='blue', label="Recalculated Epicenter (H_r, K_r)")
    for (x, y) in coordinates.values():
        circle = plt.Circle((x, y), R_mean_deg if R_mean_deg is not None else 0.0, fill=False)
        axs[1].add_artist(circle)
    axs[1].legend()
    axs[1].set_title("Points with Epicenters and Approximate Radius Circles")

    # Points with individual radii circles
    axs[2].scatter(*zip(*coordinates.values()))
    for (x, y), r in zip(coordinates.values(), radii_deg_all):
        circle = plt.Circle((x, y), r, fill=False)
        axs[2].add_artist(circle)
    axs[2].set_title("Points with Individual Radii Circles")

    fig.tight_layout()
    # Save the figure (so it's available even if a GUI isn't)
    try:
        fig.savefig(fig_filename, dpi=150)
        print(f"📷 Matplotlib figure saved as: {fig_filename}")
    except Exception as e:
        print(f"[WARN] Could not save figure: {e}")

    # --------- PDF EXPORT (now includes the epicenter intervals) ---------
    styles = getSampleStyleSheet()
    story = []

    def add_section(title, center_H, center_K, sigma_H, sigma_K, dist_km,
                    per_deg, per_km, rmin_deg, rmin_km, rmax_deg, rmax_km, rmean_deg, rstd_deg,
                    point_labels):
        story.append(Paragraph(f"<b>{title}</b>", styles['Heading2']))
        story.append(Paragraph(
            f"Epicenter (H, K): {format_lat(center_H)}, {format_lon(center_K)}",
            styles['BodyText']
        ))
        if sigma_H is not None and sigma_K is not None:
            story.append(Paragraph(
                f"Epicenter 1σ interval: (H ± {sigma_H:.6f}°, K ± {sigma_K:.6f}°)",
                styles['BodyText']
            ))
        story.append(Paragraph(f"Distance to PHIVOLCS Measured Epicenter: {kmfmt(dist_km)}", styles['BodyText']))
        story.append(Spacer(1, 12))

        # radii table
        table_data = [["Point", "Radius (deg)", "Radius (km)"]]
        for lbl, rd, rk in zip(point_labels, per_deg, per_km):
            table_data.append([lbl, f"{rd:.6f}", f"{rk:,.3f}"])
        tbl = Table(table_data)
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONT', (0,0), (-1,-1), 'Helvetica')
        ]))
        story.append(Paragraph("<b>Radii to (H, K)</b>", styles['Heading3']))
        story.append(tbl)
        story.append(Spacer(1, 12))

        # summary line items
        story.append(Paragraph(f"Minimum R: {rmin_deg:.6f}° (~{rmin_km:,.3f} km)", styles['BodyText']))
        story.append(Paragraph(f"Maximum R: {rmax_deg:.6f}° (~{rmax_km:,.3f} km)", styles['BodyText']))
        story.append(Paragraph(f"Mean R_prox: {rmean_deg:.6f}°", styles['BodyText']))
        story.append(Paragraph(f"Radius std: {rstd_deg:.6f}°", styles['BodyText']))
        story.append(Spacer(1, 18))

    story.append(Paragraph("<b>Intensity-Based Epicenter Estimate Report</b>", styles['Title']))
    story.append(Spacer(1, 12))

    # Section 1: ALL points
    labels_all = [f"P{i}" for i in range(1, len(coordinates)+1)]
    add_section(
        "1) Initial (Unfiltered) Epicenter Estimate",
        H, K, h_std, k_std, dist_measured_to_HK_km,
        radii_deg_all, radii_km_all, R_min_deg, R_min_km, R_max_deg, R_max_km, R_mean_deg, R_std_deg,
        labels_all
    )

    # Section 2: EXCLUDE outlier points
    if have_recalc:
        labels_filtered = list(coordinates_filtered.keys())  # original point names minus outliers, in dict order
        add_section(
            "2) Recalculated Epicenter (After Outlier Removal)",
            H_r, K_r, H_r_std, K_r_std, dist_measured_to_HrKr_km,
            radii_r_deg, radii_r_km, Rr_min_deg, Rr_min_km, Rr_max_deg, Rr_max_km, Rr_mean_deg, Rr_std_deg,
            labels_filtered
        )

    # Include the saved matplotlib figure in the PDF (optional but useful)
    if os.path.exists(fig_filename):
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure:</b> Triplet Geometry and Radii", styles['Heading3']))
        story.append(Image(fig_filename, width=520, height=360))

    # Build PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=LETTER)
    doc.build(story)
    print(f"📄 PDF report saved as: {pdf_filename}")

    # --------- FOLIUM MAP (same directory; NO ellipse) ---------
    if FOLIUM_AVAILABLE:
        try:
            # choose center (recalc if available)
            use_H = H_r if have_recalc else H
            use_K = K_r if have_recalc else K

            # markers: all sites
            lats = [xy[0] for xy in coordinates.values()]
            lons = [xy[1] for xy in coordinates.values()]
            map_center = [float(np.mean(lats)), float(np.mean(lons))]

            fmap = folium.Map(location=map_center, zoom_start=12)
            mc = MarkerCluster().add_to(fmap)

            for i, (lat, lon) in enumerate(coordinates.values(), start=1):
                Marker([lat, lon], popup=f"P{i} ({lat:.5f}, {lon:.5f})",
                       icon=folium.Icon(color="blue")).add_to(mc)

            folium.Marker([Hmeasured, Kmeasured],
                          popup=f"Measured Epicenter: {format_lat(Hmeasured)}, {format_lon(Kmeasured)}",
                          icon=folium.Icon(color="green", icon="star")).add_to(fmap)
            folium.Marker([H, K],
                          popup=f"Approx Epicenter: {format_lat(H)}, {format_lon(K)}",
                          icon=folium.Icon(color="red", icon="star")).add_to(fmap)
            if have_recalc:
                folium.Marker([H_r, K_r],
                              popup=f"Recalculated Epicenter: {format_lat(H_r)}, {format_lon(K_r)}",
                              icon=folium.Icon(color="purple", icon="star")).add_to(fmap)

            # individual circles for chosen center:
            # if recalculated: exclude outlier points; else use all
            coords_for_circles = coordinates_filtered.values() if have_recalc else coordinates.values()
            radii_km_for_map = [haversine_km(x, y, use_H, use_K) for (x, y) in coords_for_circles]

            mean_radius_km = float(np.mean(radii_km_for_map)) if radii_km_for_map else 0.0
            Circle([use_H, use_K], radius=mean_radius_km*1000.0,
                   color="green", fill=True, fill_opacity=0.25, weight=2,
                   popup=f"Mean radius ~ {mean_radius_km:.2f} km").add_to(fmap)

            for (lat, lon), rkm in zip(coords_for_circles, radii_km_for_map):
                Circle([lat, lon], radius=rkm*1000.0, color="gray", fill=False, weight=1,
                       popup=f"r ≈ {rkm:.2f} km").add_to(fmap)

            fmap.save(map_filename)
            print(f"🗺️  Map saved as: {map_filename}")
        except Exception as e:
            print(f"[WARN] Folium map export skipped: {e}")
    else:
        print("[INFO] Folium not installed; map export skipped. Install with: pip install folium")

    # Keep last so files are written even if GUI blocks
    plt.show()

if __name__ == "__main__":
    main()
