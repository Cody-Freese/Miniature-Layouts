# Miniature Layouts

**Miniature Layouts** is a collection of tools and project workspaces for designing miniature-scale terrain, tabletop dioramas, and fictional environments. The goal is to plan complex scenes digitally—using measured 2D diagrams and interactive 3D blockouts—before committing to physical construction or 3D printing.

The repository is organized to support **multiple independent layouts**, each with its own design scripts, reference material, documentation, and generated outputs.

## Projects

### Skavenblight — Western Cliffhold

A work-in-progress **96 × 96 in (8 × 8 ft)** concept for a 32 mm heroic-scale Skavenblight diorama, inspired by the *Doom of Kavzar* and the visual language of the Warhammer settings.

The current design includes:

- A dominant **western mountain** and snowy ridges to the north, with the city to their east.
- A fortified outer wall, corrupted marshes, ruined siege roads, and outlying workshops.
- An outer ground district, fractured inner ground, and **two raised city terraces** leading to a central bell tower.
- Two large openings into the undercity, planned for ruined Dwarf halls and Clan Skryre machinery.
- Proposed green warpstone lighting, industrial furnaces, tunnels, bridges, and layered architectural ruins.

These are **design targets**, not a final, dimension-validated construction plan.

| Resource | Description |
| --- | --- |
| [Western Cliffhold project](projects/skavenblight/western-cliffhold/README.md) | Project-specific documentation and usage |
| [2D asset plan](projects/skavenblight/western-cliffhold/outputs/maps/asset_plan.png) | Generated top-down terrain-placement diagram |
| [Editable SVG plan](projects/skavenblight/western-cliffhold/outputs/maps/asset_plan.svg) | Vector version of the diagram |
| [3D viewer source](projects/skavenblight/western-cliffhold/viewer/index.html) | Standalone, draggable HTML5/JavaScript blockout |
| [Build checklist](projects/skavenblight/western-cliffhold/docs/build_checklist.md) | Terrain, materials, lighting, and conversion planning |

> **Current limitation:** The 2D Python generator and 3D JavaScript viewer store their layout coordinates separately. Editing one does **not** automatically update the other. A shared layout-data format is planned.

## Getting started

**Requirements:** Python 3.11 or newer, a modern desktop browser, and Git if you want version control. The 2D generator uses Matplotlib and NumPy; the 3D viewer has no Python or JavaScript package dependencies.

### Windows / PowerShell

Open a terminal in the **Miniature Layouts repository root**, then run:

```powershell
# Create a local virtual environment if you do not already have one
py -m venv .venv

# Install the Python dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Generate the 2D PNG and SVG plans
.\.venv\Scripts\python.exe "projects\skavenblight\western-cliffhold\scripts\generate_asset_plan.py" --svg

# Open the interactive 3D viewer in your default browser
Start-Process ".\projects\skavenblight\western-cliffhold\viewer\index.html"
```

If you already created `.venv` through PyCharm, reuse it; there is no need to create another one.

### Git Bash

From the repository root:

```bash
python -m venv .venv                       # Only if needed
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe projects/skavenblight/western-cliffhold/scripts/generate_asset_plan.py --svg
```

Open `projects/skavenblight/western-cliffhold/viewer/index.html` in Chrome, Edge, or another modern browser. The viewer can be rotated and zoomed without a web server.

### PyCharm

Open the **repository root** as the PyCharm project. Select the interpreter at `.venv\Scripts\python.exe`. Keep `.idea/` and `.venv/` in the root directory; both are local files excluded from version control.

## Repository layout

```text
Miniature-Layouts/
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/                        # Repository-wide maintenance tools
└── projects/
    └── skavenblight/
        └── western-cliffhold/
            ├── README.md
            ├── scripts/            # Project-specific generators
            ├── viewer/             # Interactive viewer source
            ├── references/         # Reference and historical design files
            ├── assets/             # Asset inventory; licensed files remain local
            ├── docs/               # Construction and procurement notes
            └── outputs/
                ├── maps/           # Generated 2D plans (selected samples tracked)
                ├── renders/        # Temporary images, ignored by Git
                └── exports/        # Large exports / 3D meshes, ignored by Git
```

New layouts should be created as separate directories under `projects/`, so their source code, references, and generated files remain isolated.

## Project status and roadmap

**Current:** Editable 2D map generator, a standalone interactive 3D blockout, a project-level source structure, and construction-planning notes.

**Planned directions:**

- Consolidate coordinates and elevations into a shared `layout.json` used by both viewers.
- Add placement and cataloging for modular buildings, walls, roads, and terrain assets.
- Improve 3D geometry, camera controls, and sunlight/shadow simulation.
- Model construction modules, vertical cutaways, and LED/power-distribution zones.
- Explore Blender, glTF, or other export formats for more detailed design workflows.

These are intentions rather than implemented features.

## Source and asset provenance

The Western Cliffhold **Python map generator was reconstructed** from an earlier schematic; it is not a verbatim recovery of the initial plotting session. The existing **HTML5 Canvas/JavaScript viewer** was preserved as a standalone source file. Neither currently uses commercial terrain STLs as embedded geometry.

This repository is for project-authored code, documentation, and distributable work. **Do not commit** purchased STL files, proprietary textures, third-party reference artwork without permission, passwords, credentials, or other restricted content. Keep licensed terrain files in the Git-ignored `assets/licensed/` directory, and reference vendor pages or asset manifests instead.

### Unofficial fan project

The Skavenblight layout is an unofficial fan project inspired by Warhammer settings. Warhammer, Skaven, Skavenblight, and related names and imagery are associated with Games Workshop and their respective rights holders. This project is **not affiliated with, sponsored by, or endorsed by Games Workshop**. Third-party models, trademarks, and artwork remain subject to their respective owners' terms.

## License

**No license has been selected yet.** Public visibility on GitHub does not, by itself, grant permission to reuse or redistribute the project's source code. If a software license is added later, it will apply only to the material the project owner is authorized to license, not to third-party intellectual property.

---

**Repository:** [Cody-Freese/Miniature-Layouts](https://github.com/Cody-Freese/Miniature-Layouts)
