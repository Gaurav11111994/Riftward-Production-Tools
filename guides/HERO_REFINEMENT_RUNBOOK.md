# Riftward Hero Refinement — Blender Runbook

## Current next step

Use the automatic-finished Blender MASTER as the source:

`RW_Riftward_v03_AllWorldAssets_FINISHED_v01_0.blend`

Do **not** reopen the foundation MASTER.

## Script

`scripts/Riftward_BlenderHeroRefinement_v03_0_v01_0.py`

## What the script does

It performs one consolidated S01–S05 refinement-assistance pass:

- save-forwards before editing;
- preserves names, pivots and transforms where possible;
- skips lower LODs, helpers and colliders;
- discovers asset collections automatically;
- classifies assets by family;
- adds controlled bevel/normal polish;
- improves root taper and broad junction mass;
- adds secondary rock silhouette masses;
- adds portal buttresses, crown and boss crest outside the existing aperture;
- adds base/crown hierarchy to tall towers, pylons and spires;
- adds ring clamps;
- creates crystal inner cores and secondary crystals;
- creates snow-cap source overlays on up-facing ice/glacier faces;
- adds mirror backing;
- creates semantic Blender source-lookdev materials;
- creates spread-out hero review collection instances;
- checkpoints after each world;
- writes a JSON report.

## What it deliberately does NOT do

It does not claim final reference fidelity.
It does not bake Unity-owned portal energy/VFX.
It does not build Unity stages.
It does not overwrite the foundation or automatic-finished MASTER.
It does not automatically export before manual visual review.

## Run procedure

1. Launch Blender 5.2.2 LTS.
2. Open:
   `RW_Riftward_v03_AllWorldAssets_FINISHED_v01_0.blend`
3. Open the **Scripting** workspace.
4. Text Editor → **Open**.
5. Select:
   `Riftward_BlenderHeroRefinement_v03_0_v01_0.py`
6. Review the CONFIG block at the top.
7. Keep `EXPORT_AFTER_RUN = False`.
8. Click **Run Script**.

The script should save forward to a new HEROREFINE package before editing.

## After the script

Inspect the generated review collections:

- `RW_HEROREFINE_REVIEW_S01`
- `RW_HEROREFINE_REVIEW_S02`
- `RW_HEROREFINE_REVIEW_S03`
- `RW_HEROREFINE_REVIEW_S04`
- `RW_HEROREFINE_REVIEW_S05`

Then perform the manual Tier-A hero pass.

### S01
- lunar cliffs/shelves;
- observatory/dish structures;
- orbital structures/rings;
- ion/relic towers;
- normal + boss portals.

### S02
- glacier readability;
- wreck silhouettes;
- reactor cages;
- alien nests;
- crystal hierarchy;
- portals.

### S03
- root junctions/forks;
- sacred arches;
- shrine structures;
- root/crystal integration;
- portals.

### S04
- imperial/crown hierarchy;
- mirrors;
- gravity structures;
- broken monoliths;
- portals.

### S05
- monumental rings;
- fused ruins;
- fortress fragments;
- boss-approach massing;
- ivory/gold/energy separation;
- portals.

## Visual approval rule

The script is an accelerator, not an approval mechanism.

Before Unity intake:

- compare against original stage and portal references;
- manually correct generic/procedural-looking geometry;
- regenerate final FBXs;
- regenerate previews/contact sheets;
- validate pivots, names, transforms and material slots;
- review all five worlds together.

## Failure / resume

If the script fails after save-forward:

- do not overwrite/restart the automatic-finished MASTER;
- open the HEROREFINE output;
- inspect the traceback;
- fix only the narrow cause;
- rerun.

The script tags processed source objects so repeated runs avoid reprocessing them for the same version.

## Production boundary

Blender owns:
- geometry;
- silhouette;
- source UVs/textures;
- structural detail;
- faceting/edge treatment;
- material-slot separation;
- source lookdev;
- LOD-ready source geometry.

Unity later owns:
- final URP materials;
- reflection implementation;
- portal energy;
- particles/VFX;
- fog/atmosphere;
- runtime motion;
- color grading;
- final lighting.
