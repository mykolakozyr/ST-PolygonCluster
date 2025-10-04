import numpy as np
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
from shapely.strtree import STRtree


def _normalize_candidate_indices(
    candidates, geometry_lookup
):
    """Return integer indices for STRtree query results across Shapely versions."""
    if candidates is None:
        return []

    if len(candidates) == 0:
        return []

    first = candidates[0]

    if isinstance(first, (int, np.integer)):
        # Shapely 2.0+ already returns numpy array of indices
        return list(candidates)

    # Shapely <2 returns geometry objects; map via identity lookup
    mapped = []
    for geom in candidates:
        idx = geometry_lookup.get(id(geom))
        if idx is None:
            continue
        mapped.append(idx)
    return mapped


def find_overlapping_neighbors(
    gdf: gpd.GeoDataFrame, overlap_threshold: float = 0.0
) -> dict:
    """
    Efficiently find neighbors whose polygon intersection exceeds a percentage of
    their combined footprint. Defaults to 0% (any positive IoU qualifies).
    """
    if not 0 <= overlap_threshold <= 100:
        raise ValueError("overlap_threshold must be between 0 and 100 inclusive")

    geometries = list(gdf.geometry)
    tree = STRtree(geometries)
    geometry_lookup = {id(geom): idx for idx, geom in enumerate(geometries)}
    threshold_ratio = overlap_threshold / 100.0

    neighbors = {i: set() for i in range(len(geometries))}
    areas = [geom.area for geom in geometries]

    for i, poly in enumerate(geometries):
        candidates = tree.query(poly)
        candidate_indices = _normalize_candidate_indices(candidates, geometry_lookup)

        for idx in candidate_indices:
            if idx <= i:
                continue

            other = geometries[idx]
            if not isinstance(other, BaseGeometry):
                continue

            intersection_area = poly.intersection(other).area
            if intersection_area == 0:
                continue

            union_area = areas[i] + areas[idx] - intersection_area
            overlap_ratio = 1.0 if union_area == 0 else intersection_area / union_area

            if overlap_ratio >= threshold_ratio:
                neighbors[i].add(idx)
                neighbors[idx].add(i)

    return {key: sorted(value) for key, value in neighbors.items()}
