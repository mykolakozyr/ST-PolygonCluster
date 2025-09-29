# Repository Guidelines

## Project Structure & Module Organization
Source modules live under `st_polygoncluster/`. `clustering.py` contains the spatio-temporal clustering pipeline, while `neighbors.py` wraps the STRtree neighbor search. Shared sample data sits in `data/` (GeoJSON fixtures mirrored by the tests), and runnable demonstrations belong in `examples/`. Test coverage is organized under `tests/` with files mirroring the package layout (`test_clustering.py`, `test_neighbors.py`).

## Build, Test, and Development Commands
Install dependencies in editable mode before iterating:
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```
Run the full suite with `pytest` (auto-discovering the unittest cases) and log verbose output when debugging:
```bash
pytest
pytest -k clustering -vv
```
Single-file checks remain available via the stdlib runner:
```bash
python -m unittest tests/test_neighbors.py
```

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation and descriptive snake_case for functions, variables, and GeoDataFrame columns. Match the existing docstring style (triple-quoted summaries with parameter bullets) and keep functions focused on geometry or graph responsibilities. Prefer explicit type hints as in `cluster_polygons` and avoid silent mutation outside return values. When adding utilities, co-locate them with the most related module rather than new top-level packages.

## Testing Guidelines
All new behavior must ship with tests in `tests/` whose names begin with `test_`. Mirror the module structure (`test_module.py`) and assert both spatial and temporal edge cases. Use the sample GeoJSON fixtures in `data/` or supply lightweight in-memory geometries in the test body. Aim to touch each new branch or failure path and run `pytest` locally before pushing.

## Commit & Pull Request Guidelines
History favors concise, imperative summaries (`Clean up data and examples`) with optional dash-separated details in the body. Organize commits around logical units (data prep, algorithm change, docs) to ease review. PRs should describe the motivating scenario, link any tracking issue, call out data files added or modified, and include screenshots or GeoJSON diffs when visual behavior shifts. Mention required follow-up tasks in a checklist so they are not forgotten.

## Project Context Notes
- Clustering builds a graph from polygon pairs whose intersection-over-union clears the configured overlap threshold (defaults to 50%), then labels connected components.
- Temporal filtering is optional: when `time_key` and `time_threshold` are provided, edges violating the time window are dropped before component analysis.
- The code relies on GeoPandas, Shapely (STRtree), NumPy, and SciPy; ensure these heavy GIS dependencies are installed locally before running tests.
- Unit tests use both fixture GeoJSON files and in-memory Shapely polygons to cover overlap thresholds; successful test runs require the Geo stack.
