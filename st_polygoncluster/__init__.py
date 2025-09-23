# Package Initialization for ST-PolygonCluster

try:
    from importlib.metadata import version as _pkg_version, PackageNotFoundError as _PkgNotFound
    try:
        __version__ = _pkg_version("st_polygoncluster")
    except _PkgNotFound:
        __version__ = "0.0.0"
except Exception:
    __version__ = "0.0.0"

from .neighbors import find_overlapping_neighbors
from .clustering import cluster_polygons