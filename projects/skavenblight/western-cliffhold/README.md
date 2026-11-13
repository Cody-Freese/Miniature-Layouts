# Skavenblight — Western Cliffhold

A schematic 96 × 96-inch tabletop concept at 32mm heroic scale, featuring a western cliff, northern ridge, ruined ring terraces, central bell tower, industrial voids and marshes.

## Source

- `scripts/generate_asset_plan.py` — **reconstructed** editable Matplotlib generator. The original Matplotlib session was not saved.
- `viewer/index.html` — **original** standalone HTML5 Canvas / JavaScript drag-to-rotate 3D viewer.

These two visualizations currently maintain independent geometry coordinates; editing one does not update the other.

## Run the 2D generator

From the repository root:

```powershell
.\.venv\Scripts\python.exe projects\skavenblight\western-cliffhold\scripts\generate_asset_plan.py --svg
```

Generated files are saved to `outputs/maps/` in this project, independent of working directory. Use `--output <path>` to choose an alternative destination.

## Run the 3D viewer

Open `viewer/index.html` in a desktop browser. No external packages or web server are required. Drag to rotate, wheel to zoom, and use the preset camera buttons.

## Materials and documentation

- `docs/build_checklist.md` — the terrain, lighting and conversion plan.
- `references/` — original asset plan and elevation drawings.
- `outputs/maps/` — reconstructed PNG and SVG output.
- `assets/` — notes on local assets; purchased third-party STLs should be kept in `assets/licensed/`, which Git ignores.

## Coordinate system

- West = x=0; east = x=96 inches.
- South = y=0; north = y=96 inches.
- Central tower near `(63.1, 56.1)`.
- Approximate industrial pit coordinates `(44.5, 37.3)` and `(82.0, 50.0)`.

These are modeling assumptions, not finalized construction measurements or licensed STL dimensions.
