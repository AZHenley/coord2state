#!/usr/bin/env python3
"""
build_state_lookup.py

Load a TIGER/Line state shapefile, keep only the 50 states + DC,
simplify geometries, and inject the resulting GeoJSON into a JS template.
"""

import argparse
import geopandas as gpd
import json
from pathlib import Path

# List of USPS codes for the 50 states + DC
VALID_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"
}

def main():
    p = argparse.ArgumentParser(
        description="Build single-file JS state-lookup from a TIGER shapefile + JS template")
    p.add_argument("--shapefile", required=True,
                   help="Path to tl_2024_us_state.shp")
    p.add_argument("--template", required=True,
                   help="Path to state-lookup.template.js")
    p.add_argument("--tolerance", type=float, default=0.001,
                   help="Simplification tolerance in degrees (default 0.001)")
    p.add_argument("--out", default="state-lookup.js",
                   help="Output JS filename")
    args = p.parse_args()

    # 1) Load
    print(f"Loading shapefile {args.shapefile}…")
    gdf = gpd.read_file(args.shapefile).to_crs(epsg=4326)

    # 2) Filter to only the 50 states + DC
    before_count = len(gdf)
    gdf = gdf[gdf["STUSPS"].isin(VALID_CODES)]
    after_count = len(gdf)
    print(f"Filtered from {before_count} features down to {after_count} (50 states + DC)")

    # 3) Simplify
    print(f"Simplifying geometries with tol={args.tolerance}°…")
    gdf["geometry"] = gdf.geometry.simplify(
        tolerance=args.tolerance,
        preserve_topology=True
    )

    # 4) Convert to GeoJSON dict
    geojson = json.loads(gdf.to_json())

    # 5) Read template
    tpl = Path(args.template).read_text()

    # 6) Replace placeholder
    out_js = tpl.replace("{geojson}", json.dumps(geojson, indent=2))

    # 7) Write result
    Path(args.out).write_text(out_js)
    print(f"Wrote lookup library to {args.out}")

if __name__ == "__main__":
    main()
