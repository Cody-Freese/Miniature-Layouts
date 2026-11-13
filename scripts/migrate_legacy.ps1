# Reorganize an existing Miniature Layouts checkout without touching .git, .idea or .venv.
# Usage in PowerShell (script may be in repo root or repo/scripts):
#   powershell -ExecutionPolicy Bypass -File .\migrate_legacy.ps1
# Or, if placed under scripts/: 
#   powershell -ExecutionPolicy Bypass -File .\scripts\migrate_legacy.ps1
$ErrorActionPreference = 'Stop'

$scriptFolder = Split-Path -Parent $MyInvocation.MyCommand.Path
if ((Split-Path -Leaf $scriptFolder) -eq 'scripts') {
    $repo = Split-Path -Parent $scriptFolder
} else {
    $repo = $scriptFolder
}
$legacy = Join-Path $repo 'skavenblight-western-cliff'
$project = Join-Path $repo 'projects\skavenblight\western-cliffhold'

if (-not (Test-Path -LiteralPath $legacy -PathType Container)) {
    throw "Could not find the legacy folder: $legacy`nNo files were moved."
}

Write-Host "Repository: $repo"
Write-Host "Migrating: $legacy"

# Stop before doing anything if target files are already present.
$files = @(
    @('src\generate_asset_plan.py', 'scripts\generate_asset_plan.py'),
    @('viewer\index.html', 'viewer\index.html'),
    @('reference\original_asset_plan.png', 'references\original_asset_plan.png'),
    @('reference\original_elevations.png', 'references\original_elevations.png'),
    @('output\asset_plan.png', 'outputs\maps\asset_plan.png'),
    @('output\asset_plan.svg', 'outputs\maps\asset_plan.svg'),
    @('docs\build_checklist.md', 'docs\build_checklist.md'),
    @('README.md', 'docs\legacy_README.md')
)
foreach ($pair in $files) {
    $src = Join-Path $legacy $pair[0]
    $dst = Join-Path $project $pair[1]
    if ((Test-Path -LiteralPath $src -PathType Leaf) -and (Test-Path -LiteralPath $dst)) {
        throw "Destination already exists, so migration stopped without overwriting it: $dst"
    }
}

foreach ($pair in $files) {
    $src = Join-Path $legacy $pair[0]
    $dst = Join-Path $project $pair[1]
    if (Test-Path -LiteralPath $src -PathType Leaf) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
        Move-Item -LiteralPath $src -Destination $dst
        Write-Host "Moved $($pair[0]) -> projects\skavenblight\western-cliffhold\$($pair[1])"
    } else {
        Write-Warning "Not present (skipped): $src"
    }
}

$oldRequirements = Join-Path $legacy 'requirements.txt'
$newRequirements = Join-Path $repo 'requirements.txt'
if (Test-Path -LiteralPath $oldRequirements) {
    if (-not (Test-Path -LiteralPath $newRequirements)) {
        Move-Item -LiteralPath $oldRequirements -Destination $newRequirements
    } else {
        $oldReqText = [System.IO.File]::ReadAllText($oldRequirements).Trim()
        $newReqText = [System.IO.File]::ReadAllText($newRequirements).Trim()
        if ($oldReqText -eq $newReqText) {
            Remove-Item -LiteralPath $oldRequirements
        } else {
            # Leave the original untouched for manual comparison if dependencies differ.
            Write-Warning 'requirements.txt differs between root and legacy folder; retained legacy copy for review.'
        }
    }
}

# Fix the Python generator's default output. The previous default was cwd-relative.
$generator = Join-Path $project 'scripts\generate_asset_plan.py'
if (Test-Path -LiteralPath $generator) {
    $raw = [System.IO.File]::ReadAllText($generator)
    $oldDefault = "default=Path('output/asset_plan.png')"
    $newDefault = "default=Path(__file__).resolve().parents[1] / 'outputs' / 'maps' / 'asset_plan.png'"
    if ($raw.Contains($oldDefault)) {
        $raw = $raw.Replace($oldDefault, $newDefault)
        [System.IO.File]::WriteAllText($generator, $raw, [System.Text.UTF8Encoding]::new($false))
        Write-Host 'Updated default map output to project outputs/maps/.'
    } elseif (-not $raw.Contains($newDefault)) {
        Write-Warning 'Generator output default differs from expected version; review it manually.'
    }
}

# Retain existing .gitignore rules and append missing ones. Do not overwrite user's file.
$ignorePath = Join-Path $repo '.gitignore'
$legacyIgnore = Join-Path $legacy '.gitignore'
if ((-not (Test-Path -LiteralPath $ignorePath)) -and (Test-Path -LiteralPath $legacyIgnore)) {
    Move-Item -LiteralPath $legacyIgnore -Destination $ignorePath
}
$ignoreRules = @(
    '.idea/', '.venv/', 'venv/', '__pycache__/', '*.py[cod]',
    '.pytest_cache/', '.ruff_cache/', '.mypy_cache/',
    'Thumbs.db', '.DS_Store', '*.blend1', '*.blend2',
    '**/assets/licensed/', '**/assets/commercial/', '**/third_party_models/',
    '**/outputs/renders/*', '!**/outputs/renders/.gitkeep',
    '**/outputs/exports/*', '!**/outputs/exports/.gitkeep',
    '**/outputs/tmp/'
)
if (-not (Test-Path -LiteralPath $ignorePath)) {
    New-Item -Path $ignorePath -ItemType File | Out-Null
}
$present = @(Get-Content -LiteralPath $ignorePath)
if (Test-Path -LiteralPath $legacyIgnore) {
    foreach ($legacyRule in @(Get-Content -LiteralPath $legacyIgnore)) {
        if ($legacyRule.Trim() -and $present -notcontains $legacyRule) {
            Add-Content -LiteralPath $ignorePath -Value $legacyRule
            $present += $legacyRule
        }
    }
    Remove-Item -LiteralPath $legacyIgnore
}
foreach ($rule in $ignoreRules) {
    if ($present -notcontains $rule) {
        Add-Content -LiteralPath $ignorePath -Value $rule
    }
}

# Project directories to segregate outputs. Git tracks .gitkeep in otherwise empty directories.
foreach ($folder in @('outputs\renders', 'outputs\exports')) {
    $full = Join-Path $project $folder
    New-Item -ItemType Directory -Force -Path $full | Out-Null
    $marker = Join-Path $full '.gitkeep'
    if (-not (Test-Path -LiteralPath $marker)) {
        New-Item -ItemType File -Path $marker | Out-Null
    }
}
$assets = Join-Path $project 'assets'
New-Item -ItemType Directory -Force -Path $assets | Out-Null
$assetsReadme = Join-Path $assets 'README.md'
if (-not (Test-Path -LiteralPath $assetsReadme)) {
    Set-Content -LiteralPath $assetsReadme -Encoding UTF8 -Value 'Keep purchased STL models under assets/licensed/ (excluded by .gitignore). Do not redistribute commercial terrain meshes.'
}

$projectReadme = Join-Path $project 'README.md'
if (-not (Test-Path -LiteralPath $projectReadme)) {
    @'
# Skavenblight - Western Cliffhold

An 8x8-foot concept diorama with a western cliff, snow-capped northern mountains, stepped city, a central bell tower, industrial pits, and swamp outskirts.

## Run the 2D generator
From repository root, using the PyCharm virtual environment:

```powershell
.\.venv\Scripts\python.exe projects\skavenblight\western-cliffhold\scripts\generate_asset_plan.py --svg
```

Generated images are saved under `outputs/maps/` in this project.

## Open the 3D viewer
Open `viewer/index.html` in Chrome or Edge. No external server is required.

## Files
- `scripts/` - reconstructed Python source for the 2D map
- `viewer/` - original standalone 3D HTML/JavaScript viewer
- `references/` - preserved original images
- `outputs/maps/` - generated PNG/SVG plans
- `outputs/renders/` - optional large renders (Git ignored)
- `outputs/exports/` - optional STL/GLB/other exports (Git ignored)
- `docs/build_checklist.md` - terrain and construction notes
- `docs/legacy_README.md` - original source package README

The Python generator is a reconstruction of the original graphic; the 2D and 3D tools do not yet share one geometry configuration.
'@ | Set-Content -LiteralPath $projectReadme -Encoding UTF8
}

# If the GitHub repository already created a README, leave it intact.
$rootReadme = Join-Path $repo 'README.md'
if (-not (Test-Path -LiteralPath $rootReadme)) {
    @'
# Miniature Layouts

A multi-project terrain and diorama planning repository. Every project has separate source, references, viewers and outputs.

## Projects
- [Skavenblight - Western Cliffhold](projects/skavenblight/western-cliffhold/README.md)

## Windows / PyCharm
Keep `.idea/` and `.venv/` in the repository root. Both are Git-ignored.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe projects\skavenblight\western-cliffhold\scripts\generate_asset_plan.py --svg
```

The 2D generator saves PNG/SVG files to its own project's `outputs/maps/` folder.
'@ | Set-Content -LiteralPath $rootReadme -Encoding UTF8
}

# Remove rebuildable Python bytecode caches from the legacy folder only.
Get-ChildItem -LiteralPath $legacy -Directory -Recurse -Filter '__pycache__' | ForEach-Object {
    Remove-Item -LiteralPath $_.FullName -Recurse -Force
}

# Remove only empty legacy subdirectories; retain any custom files or user changes.
Get-ChildItem -LiteralPath $legacy -Directory -Recurse | Sort-Object FullName -Descending | ForEach-Object {
    if (@(Get-ChildItem -LiteralPath $_.FullName -Force).Count -eq 0) {
        Remove-Item -LiteralPath $_.FullName
    }
}
if (@(Get-ChildItem -LiteralPath $legacy -Force).Count -eq 0) {
    Remove-Item -LiteralPath $legacy
    Write-Host 'Removed empty legacy source directory.'
} else {
    Write-Warning "The old directory still has files (e.g. caches or extra work): $legacy. Review and remove it manually if appropriate."
}
Write-Host ''
Write-Host 'Migration complete. .git, .idea, and .venv were not changed.' -ForegroundColor Green
Write-Host 'Next: run the generator, inspect the new project folder, then git add -A; git status; git commit.'
