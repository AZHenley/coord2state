#!/usr/bin/env python3
"""
vertex_compare.py

Compare vertex counts before and after simplification
for each U.S. state in the TIGER/Line shapefile.
"""

import geopandas as gpd

def count_vertices(geom):
    total = 0
    def count_poly(poly):
        cnt = len(poly.exterior.coords)
        for interior in poly.interiors:
            cnt += len(interior.coords)
        return cnt

    if geom.geom_type == "Polygon":
        return count_poly(geom)
    elif geom.geom_type == "MultiPolygon":
        return sum(count_poly(p) for p in geom.geoms)
    return 0

def main():
    # 1) Load and reproject
    shp = "tl_2024_us_state.shp"
    states = gpd.read_file(shp).to_crs(epsg=4326)

    # 2) Compute original vertex counts
    states["orig_vertices"] = states.geometry.apply(count_vertices)

    # 3) Simplify geometries 
    tol = 0.01
    states_simp = states.copy()
    states_simp["geometry"] = states_simp.geometry.simplify(
        tolerance=tol, preserve_topology=True
    )
    states["simp_vertices"] = states_simp.geometry.apply(count_vertices)

    # 4) Show comparison
    report = states[["NAME", "STUSPS", "orig_vertices", "simp_vertices"]]
    report["reduction_%"] = (
        (report.orig_vertices - report.simp_vertices) / report.orig_vertices * 100
    ).round(1)

    print(report.sort_values("reduction_%", ascending=False).to_string(index=False))

if __name__ == "__main__":
    main()
