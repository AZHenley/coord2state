#!/usr/bin/env python3
"""
plot_texas_simplification.py

Compare the full-detail vs. simplified Texas state boundary.
Generates and saves a PNG with both outlines overlaid.
"""

import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    # --- User parameters ---
    shapefile = "tl_2024_us_state.shp"  # path to your TIGER/Line .shp (with .dbf, .shx, .prj)
    state_code = "TX"                   # USPS code
    tolerance = 0.1                     # DP simplify tolerance in degrees (~100 m)
    output_png = "texas_compare.png"
    # ------------------------

    # 1) Load and reproject
    print(f"Loading shapefile {shapefile} …")
    states = gpd.read_file(shapefile).to_crs(epsg=4326)

    # 2) Extract Texas
    tx_full = states[states["STUSPS"] == state_code]
    if tx_full.empty:
        raise RuntimeError(f"No features found for state code '{state_code}'")

    # 3) Simplify geometry
    print(f"Simplifying Texas geometry with tol={tolerance}° …")
    tx_simp = tx_full.copy()
    tx_simp["geometry"] = tx_simp.geometry.simplify(
        tolerance=tolerance, preserve_topology=True
    )

    # 4) Plot both
    fig, ax = plt.subplots(figsize=(8, 8))
    tx_full.boundary.plot(ax=ax, linewidth=1, label="Original", color="C0")
    tx_simp.boundary.plot(ax=ax, linewidth=1, linestyle="--", label="Simplified", color="C1")
    ax.set_title("Texas State Boundary: Original vs. Simplified")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()

    # 5) Save to file
    plt.tight_layout()
    fig.savefig(output_png, dpi=150)
    print(f"Saved comparison plot to {output_png}")

if __name__ == "__main__":
    main()
