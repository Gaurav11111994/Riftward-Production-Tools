---
name: riftward-master-blender-production
version: 1.0.0
description: >
  Master reference-driven Blender production and hero-refinement skill for
  Riftward S01-S05. Use for reference analysis, modeling, sculpting,
  hard-surface work, organic forms, architecture, rocks, ice, crystals,
  UVs, baking, PBR texturing, materials, lookdev lighting, LODs, export,
  validation, and reference-fidelity review.
---

# RIFTWARD MASTER BLENDER PRODUCTION SKILL

## 0. Purpose

Produce premium, readable, reference-specific Riftward environment and hero assets without reducing the art to procedural primitives, random noise, generic kitbash forms, or copied marketplace assets.

The operating principle is:

**Riftward references define WHAT to build.  
The supplied learning assets teach HOW to model, texture, shade, light, and polish it.**

Marketplace/source assets are primarily craft references. Extract principles from them. Do not let them replace Riftward art direction.

## 1. Authority order

When references disagree:

1. Current Riftward project authority / production matrix / AGENTS rules.
2. Approved Riftward stage, world, and portal references.
3. Existing approved Riftward assets.
4. User-supplied learning/reference assets.
5. General physically based art knowledge.
6. Procedural/default Blender solutions.

Technical completion is never equivalent to visual approval.

## 2. Reference-learning method

For every supplied reference, ask:

- What is the primary silhouette?
- How are primary, secondary, and tertiary forms distributed?
- How does thickness change?
- How are edges handled?
- How are large quiet areas balanced with detail?
- How are materials separated?
- What does roughness do?
- Where is dirt/moss/frost/oxidation placed?
- How is damage related to structure?
- How is the asset grounded?
- What survives at gameplay-camera distance?
- Which decisions are geometry, which are texture, and which are lighting?

Do not ask only “what Riftward object can this replace?”

## 3. Duplicate policy

Ignore duplicate uploads before learning analysis.

Deduplicate by:

1. exact hash when available;
2. identical normalized filename;
3. same package name and byte size;
4. clearly identical content.

Duplicate copies do not increase reference weight.

## 4. Non-negotiable production rules

- Work save-forward.
- Never overwrite protected Blender foundations or finished authorities.
- Preserve asset IDs, collection names, pivots, origins, and production transforms where required.
- Preserve semantic material-slot meaning.
- Vendor/reference packages remain untouched.
- Never join an entire world into one mesh.
- Export each approved production asset independently.
- Do not bake Unity-owned portal energy, fog, runtime motion, particles, or final VFX into static Blender geometry.
- Keep portal apertures physically open.
- Do not add gameplay colliders unless explicitly requested.
- Protect the gameplay corridor and runway rules.
- Do not solve weak art by merely increasing polygon count.
- Do not solve rocks with random noise.
- Do not solve roots with uniform tubes.
- Do not solve architecture with stacked boxes.
- Do not solve crystals with cloned spikes.
- Do not solve ruins with random Boolean holes.
- Do not solve ice by recoloring rock blue.
- Do not solve gold by making whole objects gold.
- Do not solve emissive art by making every edge glow.

## 5. Master asset workflow

Every important asset follows:

REFERENCE
→ DESIGN DECOMPOSITION
→ BLOCKOUT
→ PRIMARY FORMS
→ SECONDARY FORMS
→ STRUCTURAL LOGIC
→ TERTIARY DETAIL
→ TOPOLOGY CLEANUP
→ NORMAL / SHADING REVIEW
→ UV
→ BAKE
→ MATERIAL / TEXTURE
→ LOOKDEV
→ GAMEPLAY-CAMERA REVIEW
→ LOD
→ EXPORT VALIDATION
→ REFERENCE COMPARISON

Never texture a weak silhouette.

Never use microdetail to hide weak modeling.

## 6. Form hierarchy

### Primary forms

Visible from far away:

- cliff profile;
- tower silhouette;
- giant root direction;
- ring arc;
- portal outline;
- glacier mass;
- wreck hull;
- monumental ruin.

Target visual importance: roughly 60-75%.

### Secondary forms

Readable at normal gameplay distance:

- shelves;
- braces;
- buttresses;
- branch forks;
- ribs;
- panel recesses;
- large fractures;
- trims;
- crystal subclusters;
- snow caps.

Target: roughly 20-30%.

### Tertiary detail

Close-review information:

- chips;
- scratches;
- bolts;
- pores;
- bark grooves;
- fine cracks;
- engraved lines;
- micro-normal detail.

Target: roughly 5-10%.

If tertiary detail competes with the silhouette, reduce it.

## 7. Silhouette test

Before detailed modeling:

- inspect as solid black;
- inspect front, side, and 3/4;
- inspect from gameplay camera;
- zoom out;
- evaluate negative space.

Questions:

- Is the asset recognizable without texture?
- Is it distinct from other assets in the same family?
- Is there a dominant gesture?
- Are asymmetries intentional?
- Does it look authored rather than averaged by a procedural generator?

If not, continue primary-form work.

## 8. Hard-surface modeling

Use the mechanical, antenna, coupling, tool, urban-kitbash, furniture, chest, vehicle, and weapon references for construction logic.

### Hierarchy

PRIMARY SHELL
→ STRUCTURAL FRAME
→ SUPPORT
→ RECESS
→ PANEL
→ TRIM
→ JOINT
→ FASTENER
→ SMALL FUNCTIONAL DETAIL

Every detail should imply a purpose.

Avoid greeble soup.

### Bevel logic

Perfectly sharp edges generally look unfinished.

Bevel width must scale with the object.

Practical visual starting points:

- tiny functional edge: ~0.2-0.5% of local form width;
- normal visible structural edge: ~0.5-1.5%;
- monumental stylized architecture can intentionally exceed that.

These are visual heuristics, not fixed dimensions.

### Hard-surface quality formula

large clean plane
+ controlled edge
+ selective recess
+ structural support
+ material break

usually reads better than:

flat object
+ hundreds of tiny panels.

## 9. Architecture

Architecture must imply support, weight, load, foundation, repetition, rhythm, access, and construction hierarchy.

For monumental structures:

BASE
→ BODY
→ MAJOR FRAME
→ SECONDARY FRAME
→ CROWN / TOP
→ ORNAMENT

Use repetition, then deliberately break it.

Avoid evenly distributed complexity.

Useful lessons from towers, castles, storefront frames, and skyscrapers:

- vertical rhythm;
- frame thickness;
- recess depth;
- foundation mass;
- roof/crown silhouette;
- modular repetition;
- structural exposure after damage;
- how large masses are visually subdivided.

Do not copy recognisable architecture; transfer principles.

## 10. Ruins and destruction

Damage must follow how the object was built.

Good destruction:

INTACT STRUCTURE
→ STRESS ZONE
→ FAILURE POINT
→ BROKEN STRUCTURAL MEMBER
→ EXPOSED INTERIOR
→ DEBRIS HIERARCHY
→ POST-FAILURE WEATHERING

Use three damage scales:

### Macro
missing section, collapse, broken ring segment.

### Meso
broken beams, fractured wall edges, large chips.

### Micro
scratches, fine cracks, erosion.

Do not damage every edge. Quiet intact surfaces make damage believable.

## 11. Rocks and cliffs

Premium geology is driven by planes and fracture hierarchy, not uniform noise.

### Construction

PRIMARY MASS
→ GEOLOGICAL DIRECTION
→ LARGE BREAK PLANES
→ SHELVES
→ SECONDARY FRACTURES
→ SMALL CHIPS
→ MICRO SURFACE

### Frequency layers

Large:
major cliff blocks.

Medium:
fractures and ledges.

Small:
surface erosion.

Random displacement is a finishing accent, not the foundation.

Strong cliffs need:

- directional geology;
- large readable planes;
- undercuts;
- shelf depth;
- asymmetry;
- intentional vertical rhythm.

## 12. Lunar terrain

Use lunar references for:

- impact craters;
- crater lips;
- compacted regolith;
- fine powder;
- exposed harder substrate;
- impact fracture;
- dusty cavity accumulation.

Recommended hierarchy:

bedrock
→ impact fracture
→ crater depression
→ powder accumulation
→ exposed sharper edge
→ fine granular breakup

Keep S01 low-saturation and distinct from Earth granite.

## 13. Stone materials

### Limestone

- pale;
- porous;
- softened weathering;
- chipped corners;
- sedimentary variation.

Preview roughness: ~0.55-0.85.  
Metallic: 0.

### Granite

- harder fracture;
- coarse mineral variation;
- sharper breaks;
- medium-high roughness.

Preview roughness: ~0.45-0.8.

### Marble / ceremonial stone

- cleaner planes;
- lower roughness;
- subtle veins/value variation;
- polished or worn response.

Preview roughness: ~0.20-0.55.

### Ancient weathered stone

Use:

- chipped silhouette;
- softened exposed edges;
- cavity dirt;
- restrained moss/lichen;
- streaks where gravity/weather supports them.

Never bake dramatic lighting into Base Color.

## 14. Roots, trunks, and wood

The root, stump, branch, antler, skull, and tree references are core structural-learning assets.

### Root construction

BASE MASS
→ MAIN ROOT
→ TAPER
→ FORK
→ KNUCKLE
→ SECONDARY ROOT
→ BROKEN END
→ BARK DETAIL

Roots must not maintain a constant radius.

At forks:

- widen before split;
- compress/flatten;
- change cross-section;
- introduce asymmetry;
- taper after split.

Ground-contact roots flatten under perceived weight.

Use irregular elliptical cross-sections, not circular tubes everywhere.

### Root silhouette

Good:
heavy base → directional extension → uneven forks → strong negative space.

Bad:
spaghetti → equal radius → random crossings.

### Wood

Surface detail follows grain.

Use:

- directional cracks;
- broken fibers;
- bark separation;
- exposed inner wood;
- localized moss;
- softer decayed zones.

Do not apply isotropic noise as a substitute for grain.

## 15. Organic curvature

Natural references teach:

- taper;
- continuous curvature;
- changing cross-section;
- growth direction;
- compression;
- asymmetry;
- junction behavior.

These principles can inform S03 roots, S04 crown shapes, and S05 curved supports without copying recognisable anatomy.

## 16. Foliage

Build hierarchy:

PLANT MASS
→ BRANCH / STEM GROUP
→ LEAF CLUSTER
→ INDIVIDUAL LEAF

Do not construct the whole plant as random individual leaves.

Variation should include:

- scale;
- bend;
- rotation;
- cluster density;
- health/decay;
- color;
- roughness.

For game assets:

- use cards where appropriate;
- preserve silhouette density;
- limit excessive alpha overlap;
- control overdraw;
- use geometry leaves only when needed.

Final wind is Unity-owned unless explicitly required in source art.

## 17. Ice

ICE IS NOT BLUE ROCK.

Ice needs:

- thickness variation;
- translucent zones;
- opaque frosted zones;
- internal cracks;
- fracture planes;
- sharp exposed edges;
- softened frosted regions;
- trapped value variation.

### Structure

PRIMARY ICE MASS
→ FRACTURE PLANE
→ INTERNAL CRACK
→ THIN EDGE
→ FROST LAYER
→ SNOW ACCUMULATION

Source-lookdev IOR: ~1.31.

Preview roughness can range from ~0.05 clear areas to ~0.65 frosted areas.

Final mobile Unity implementation may simplify transmission significantly.

## 18. Snow

Snow accumulates according to gravity, exposure, shelter, wind, and surface orientation.

Use:

base material
→ selective snow mask
→ thicker accumulation on horizontal shelves
→ less on vertical faces
→ wind-scoured exposed edges

Avoid uniform white coating.

Preview roughness: ~0.65-0.95.

## 19. Crystals

Use dominant / secondary / accent hierarchy.

DOMINANT CRYSTAL
→ SECONDARY CRYSTALS
→ SMALL ACCENTS

Vary:

- height;
- thickness;
- lean;
- facet count;
- orientation;
- embedded depth.

Avoid radial clone arrangements.

Each important crystal should have:

- intentional facets;
- readable termination;
- width variation;
- grounded/embedded base;
- local asymmetry.

For premium crystals:

OUTER FACETED SHELL
+ OPTIONAL INNER CORE

Blender owns geometry and semantic materials.

Unity owns final transmission, Fresnel, glow, refraction-like behavior, and mobile simplification.

Preview IOR: roughly 1.45-1.60 depending on mineral intent.

## 20. Black materials

Do not collapse all dark materials into one shader.

### Rough black stone

Metallic: 0  
Roughness: ~0.55-0.90

Needs broad readable highlights.

### Polished obsidian-like stone

Metallic: 0  
Roughness: ~0.08-0.35

Black must not be RGB 0 everywhere.

### Black metal

Metallic: 1  
Roughness: ~0.15-0.55

Use controlled micro-scratches and edge response.

S04 depends on separating rough black stone, polished black stone, black metal, and mirror.

## 21. Gold and metallic ornament

Gold is a hierarchy accent.

Typical preview:

Metallic: 1  
Roughness: ~0.15-0.45

For aged gold:

cleaner protected recesses
+ micro-scratched exposed surfaces
+ subtle grime
+ darker cavities

Use roughness variation more than large random Base Color variation.

Do not make entire structures gold.

## 22. Aged metal

Layer logically:

BASE METAL
→ MANUFACTURING MARK
→ SCRATCH / ABRASION
→ OXIDATION
→ DIRT
→ EDGE EXPOSURE

For painted metal:

paint
→ chips
→ exposed metal
→ selective oxidation

Avoid uniform procedural rust.

## 23. Mirrors

A mirror is not an infinitely thin reflective plane.

Geometry should include:

- frame;
- backing;
- support;
- attachment;
- border/recess;
- thickness.

Blender can preview reflectivity.

Unity owns final reflection implementation.

## 24. Energized / burnt / lava-like surfaces

Use the lava, burnt, charred, and molten references as material-logic studies.

Recommended balance:

80-90% stable structural surface
+
10-20% energetic exposed zones

Pattern:

dark crust
→ medium exposed regions
→ fine connecting fissures
→ localized brightest points

Vary emission intensity.

Do not make all cracks equally bright.

Especially useful for S05.

## 25. Dirt, moss, weathering, and grounding

Dirt accumulates at:

- cavities;
- bottoms;
- contact zones;
- horizontal ledges;
- sheltered recesses.

Moss prefers:

- moisture;
- shade;
- crevices;
- sloped/upward surfaces;
- less disturbed zones.

Avoid global moss coverage.

Ground assets with:

- embedded bases;
- debris;
- root transitions;
- contact discoloration;
- dust;
- small transitional geometry.

No visibly floating props.

## 26. Texture-frequency hierarchy

Every texture should have:

### Macro
large color/material regions.

### Meso
wear zones, stains, fracture areas, medium breakup.

### Micro
pores, scratches, grain, fine cracks.

Gameplay readability depends mostly on macro and meso information.

Do not build a texture out of micro noise only.

## 27. PBR map rules

### Base Color

Contains material color.

Do NOT include:

- directional lighting;
- strong baked AO;
- painted specular highlights;
- fake shadows.

### Roughness

Critical for realism and material separation.

Use meaningful spatial variation.

Never derive it by simply converting Base Color to grayscale.

### Metallic

Dielectric: 0.  
Metal: 1.

Intermediate values are mainly for transition/antialias pixels, not arbitrary artistic gray.

### Normal

Use for:

- fine surface;
- shallow chips;
- grain;
- engraving;
- fine fracture.

Do not use normal maps to replace silhouette geometry.

### Height

Use for source detail and baking.

For mobile, prefer converting small height to normals unless silhouette/parallax requires more.

### AO

Keep separate where possible.

Do not crush Base Color with aggressive AO.

### Emission

Use a dedicated mask.

Keep non-emissive areas truly non-emissive.

### Opacity

Use only when necessary.

Excess alpha is expensive on mobile.

## 28. Color space

In Blender:

sRGB:
- Base Color;
- colored emission.

Non-Color:
- roughness;
- metallic;
- AO;
- normal;
- height;
- masks.

Tangent normal maps must pass through a Normal Map node.

## 29. UV strategy

Choose based on asset role.

### Unique UV

Use when:

- hero asset;
- unique damage;
- asymmetric texture story;
- baked normal/AO required.

### Trim sheet

Use for:

- architecture;
- repeated beams;
- frames;
- edge profiles;
- panels;
- modular structures.

### Tiling material

Use for:

- large rocks;
- broad architecture;
- terrain-like surfaces.

Break repetition with:

- vertex masks;
- second UV;
- decals;
- macro variation;
- world-space masks.

### Atlas

Useful for:

- small props;
- foliage families;
- repeated modular details.

Avoid creating hard-to-maintain mega-atlases of unrelated content.

## 30. UV seams

Place seams:

- in hidden areas;
- at natural material boundaries;
- near hard edges when appropriate;
- along structural breaks.

Avoid cutting directly across major hero-facing surfaces unless needed.

## 31. Texel density

Maintain consistent density inside an asset family unless hero areas justify more.

Priority:

hero-facing
> standard visible
> underside / hidden.

Do not waste resolution on invisible bottoms.

Practical mobile-oriented starting classes:

- hero near asset: often 2K source/final class;
- mid support asset: often 1K;
- small/far: often 512-1K.

4K may be valid as source or exceptional hero data, but final engine resolution must be justified by screen coverage.

## 32. UV padding

Starting point:

- 2K: ~8 px or more;
- 4K: ~16 px or more.

Scale with resolution and mip requirements.

Always validate after engine import.

## 33. Overlapping / mirrored UVs

Allowed when:

- surfaces are truly repeated;
- no unique bake is needed;
- no unique dirt/damage is needed.

Avoid when:

- unique normal/AO is required;
- asymmetry matters;
- baked lightmap UV needs uniqueness.

## 34. Lightmap UV

If Unity uses baked lightmaps, maintain a separate UV channel with:

- no overlap;
- enough margin;
- clean packing;
- no zero-area islands.

Do not assume UV0 is suitable for lightmapping.

## 35. High-to-low baking

For hero assets:

HIGH POLY / SOURCE DETAIL
→ CLEAN LOW POLY
→ CAGE
→ BAKE
→ INSPECT
→ FIX
→ REBAKE

Useful bakes:

- tangent normal;
- AO;
- curvature;
- thickness;
- position;
- material ID.

Inspect for artifacts around:

- tight corners;
- intersections;
- mirrored seams;
- hard edges;
- thin geometry.

Use proper cages or exploded baking when required.

## 36. Topology

Static environment topology exists to support:

- silhouette;
- shading;
- UVs;
- LOD;
- export stability.

Perfect deformation topology is unnecessary unless deformation is planned.

N-gons are acceptable only when:

- planar;
- stable;
- non-deforming;
- predictable under triangulation;
- free of shading artifacts.

Avoid:

- zero-area faces;
- doubles;
- accidental internal faces;
- bad non-manifold regions;
- self-intersections causing visible artifacts;
- unexpected negative scale.

## 37. Normals and shading

Inspect under grazing light.

Use:

- bevels;
- intentional smooth/flat shading;
- weighted normals where useful;
- controlled hard edges;
- stable triangulation.

For hard-surface work, good bevels plus normals often create more perceived quality than large polygon increases.

## 38. Transforms and scale

Use metric scale.

For new assets:

- model at believable real size;
- aim for 1,1,1 object scale before final export;
- avoid hidden negative scale.

For existing Riftward production assets:

do not change approved pivot, origin, placement, collection transform, or asset name unless explicitly permitted.

Refine geometry locally.

## 39. Portal frames

Portal frames are Tier-A assets.

Check:

- front silhouette;
- side depth;
- top profile;
- base;
- crown;
- material-region separation;
- open aperture;
- VFX socket areas.

Normal and boss portals must belong to the same family, but boss portals must be more monumental through design, not simple uniform scaling.

No permanent energy plane in Blender.

## 40. LOD strategy

LOD0:
hero silhouette + important secondary forms.

LOD1:
remove tertiary geometry.

LOD2:
simplify secondary forms but preserve silhouette.

Far LOD:
prioritize outline and broad material regions.

Never destroy:

- portal aperture;
- landmark silhouette;
- major root fork;
- major ring break;
- tower crown.

Remove invisible tertiary complexity first.

## 41. Optimization

Optimize what the gameplay camera cannot perceive.

Priority order:

1. hidden interior geometry;
2. invisible faces;
3. excessive backfaces;
4. tiny bevel segments;
5. redundant support loops;
6. invisible microgeometry;
7. excessive material slots;
8. excessive transparent layers;
9. unnecessary unique materials.

Do not sacrifice a hero silhouette for trivial triangle savings.

## 42. Material-slot discipline

Use semantic slots:

- MAT_Stone
- MAT_MetalDark
- MAT_MetalGold
- MAT_Wood
- MAT_Bark
- MAT_CrystalOuter
- MAT_CrystalCore
- MAT_Ice
- MAT_Snow
- MAT_EmissiveSocket
- MAT_MirrorSurface

Avoid generic names such as Material.001.

Minimize unnecessary slots to reduce draw calls.

## 43. Source-lookdev material starting values

These are preview starting points, not Unity specifications.

| Material | Metallic | Roughness | Notes |
|---|---:|---:|---|
| Lunar rock | 0 | 0.65-0.90 | low saturation |
| Limestone | 0 | 0.55-0.85 | porous |
| Granite | 0 | 0.45-0.80 | coarse |
| Marble | 0 | 0.20-0.55 | subtle veins |
| Dirt | 0 | 0.70-0.95 | cavity variation |
| Bark | 0 | 0.60-0.90 | directional |
| Dry wood | 0 | 0.45-0.80 | directional grain |
| Painted metal | masked | 0.25-0.70 | chips expose metal |
| Raw steel | 1 | 0.20-0.55 | subtle scratches |
| Aged gold | 1 | 0.18-0.45 | darkened cavities |
| Rough black stone | 0 | 0.55-0.90 | broad highlight |
| Polished obsidian-like stone | 0 | 0.08-0.35 | black ≠ zero RGB |
| Black metal | 1 | 0.15-0.55 | edge response |
| Ice | 0 | 0.05-0.65 | IOR ~1.31 |
| Crystal | 0 | 0.04-0.30 | IOR ~1.45-1.60 |
| Snow | 0 | 0.65-0.95 | soft normal |
| Mirror preview | 1 | 0.00-0.08 | Unity owns final reflection |

## 44. Lookdev lighting

Never judge a material only under dramatic mood lighting.

Use two review modes.

### A. Neutral material rig

Use:

- neutral world;
- large soft key;
- weaker fill;
- rim/back light;
- neutral white balance;
- restrained exposure.

Purpose:

- reveal roughness;
- reveal bevels;
- expose normal errors;
- reveal texture stretching;
- expose weak material breakup.

### B. World mood preview

Only after neutral validation.

Do not hide weak art with:

- fog;
- bloom;
- darkness;
- heavy color grading.

## 45. Color management

Use a consistent Blender color-management configuration.

AgX is preferred for modern Blender source lookdev because of its highlight handling.

Do not change exposure/look between comparison renders without recording it.

## 46. Lighting QA

Review under:

1. soft frontal light;
2. grazing side light;
3. backlight / silhouette;
4. world mood light.

Grazing light exposes:

- bad normals;
- faceting;
- stretched textures;
- weak bevels;
- flat roughness.

## 47. Camera review

Every hero asset should be inspected:

- front;
- side;
- 3/4;
- elevated;
- gameplay camera;
- close material view.

A strong close-up does not prove gameplay readability.

## 48. Texture review distances

Review at:

100%:
artifact detection.

50%:
normal detail.

25% or gameplay-equivalent:
macro/meso readability.

If all information disappears at gameplay scale, there is too much microdetail.

# WORLD-SPECIFIC RULES

## 49. S01 — Shardfall Moon

Core language:

LUNAR GEOLOGY
+ ENGINEERED GRAPHITE / SILVER TECHNOLOGY
+ CONTROLLED CYAN ENERGY

Use learning from:

- cratered lunar surfaces;
- charcoal/regolith-like powder;
- cliffs and boulders;
- weathered stone;
- antennas;
- mechanical props;
- fittings;
- towers and structural frames.

### S01 rocks

Need:

- low saturation;
- directional fracture;
- impact influence;
- dusty deposition;
- large planes;
- lunar identity.

### S01 machinery

Need:

- believable supports;
- joints;
- mounting hardware;
- structural braces;
- pivot logic;
- graphite body;
- restrained silver;
- reserved cyan socket regions.

### S01 architecture

Use tower/skyscraper references only for:

- vertical rhythm;
- frame hierarchy;
- support logic;
- recess depth;
- crown silhouette.

Do not copy recognisable urban architecture.

### S01 cyan

Use as accent, not as full-object glow.

## 50. S02 — Cryo Belt

Core language:

ICE
+ SNOW
+ FROSTED INDUSTRIAL STRUCTURE
+ CRYSTAL
+ WRECKAGE

The snowy peak, icy ground, ice cube, frozen-wall, frozen-cascade, and crystal references define the craft vocabulary.

### Glacier

Must include:

- layered mass;
- fracture planes;
- translucent thin edges;
- opaque frosted core;
- snow shelves;
- blue depth without blue-rock appearance.

### Frozen metal

Use:

metal
→ frost
→ partial ice accretion
→ snow

not:

entire machine painted blue/white.

### Wrecks

Use:

intact structural rhythm
→ structural failure
→ exposed interior
→ secondary fragments
→ post-destruction frost/snow.

## 51. S03 — Blight Expanse

Core language:

ROOT
+ BARK
+ STONE
+ MOSS / FOLIAGE
+ TURQUOISE CRYSTAL
+ SELECTIVE GOLD / TECH
+ VIOLET CORRUPTION

### Roots

Highest priority:

- weighted base;
- flatten at contact;
- taper;
- uneven forks;
- negative space;
- directional gesture.

### Sacred structures

Use ancient stone, altar, statue, and architectural construction principles without reproducing recognisable sacred real-world objects.

The structure should appear integrated with roots and crystal, not decorated after the fact.

### Corruption

Change:

- silhouette;
- growth direction;
- material behavior;
- local emissive accents.

Do not simply recolor healthy roots purple.

## 52. S04 — Black Crown Reach

Core language:

OBSIDIAN / BLACK STONE
+ DARK METAL
+ CHAMPAGNE GOLD
+ MIRROR
+ IMPERIAL HIERARCHY
+ INDIGO ENERGY

### Black separation

Distinguish:

- rough black stone;
- polished black stone;
- black metal;
- mirror.

Do not use one generic dark material for all.

### Gold

Reserve for:

- edge hierarchy;
- insignia;
- crown motifs;
- selective structural trims.

### Mirrors

Need:

- frame;
- backing;
- thickness;
- support;
- controlled damage.

Unity owns final reflection behavior.

### Imperial structures

Use repeated motifs and controlled asymmetry.

Avoid featureless stacks of dark cubes.

## 53. S05 — Eclipse Gate

Core language:

MONUMENTAL DARK STRUCTURE
+ IVORY / PALE STONE
+ AGED GOLD
+ FRACTURED RINGS
+ FUSED RUINS
+ WARM INTERNAL ENERGY
+ CRYSTAL INSERTION

### Energy

Preferred:

dark / ivory structure
+ localized warm internal damage.

Avoid universal orange edge glow.

### Rings

Need:

- believable thickness;
- major breaks;
- visible broken cross-section;
- secondary fragments;
- material separation;
- asymmetrical damage.

### Boss approach

Increase:

- mass;
- vertical dominance;
- depth;
- silhouette aggression;
- material contrast.

Do not equate “boss quality” with more greebles.

# VALIDATION

## 54. Common failure modes

Reject an asset if it shows:

- primitive/blockout silhouette;
- same bevel width at all scales;
- random noise everywhere;
- stretched textures;
- repeated procedural patterns;
- cloned crystals;
- tube-like roots;
- floating rocks;
- overused gold;
- unreadable black surfaces;
- blue rock pretending to be ice;
- destruction with no structural logic;
- emission everywhere;
- microdetail invisible from gameplay view;
- too many material slots;
- unneeded transparency;
- broken scale;
- broken pivot;
- unintended transform changes;
- blocked portal aperture;
- duplicated terminal portal ownership;
- runtime VFX modeled into static geometry.

## 55. Hero-asset checklist

### Design
- reference intent preserved;
- world identity obvious;
- silhouette unique;
- hierarchy clear.

### Geometry
- primary form strong;
- secondary structure purposeful;
- tertiary detail controlled;
- no accidental intersections;
- believable thickness;
- clean grounding.

### Topology
- no useless geometry;
- no zero-area faces;
- stable triangulation;
- clean shading.

### UV
- no unintended overlap;
- consistent texel density;
- sufficient padding;
- no obvious stretching;
- correct UV-channel strategy.

### Texture
- macro variation;
- meso variation;
- restrained micro detail;
- meaningful roughness;
- clean normals;
- correct metal/nonmetal logic;
- no lighting baked into Base Color.

### Material
- semantic regions;
- world palette;
- physically distinct surfaces;
- selective emission;
- justified transparency/reflection.

### Lighting
- neutral-rig pass;
- grazing-light pass;
- silhouette pass;
- mood-preview pass.

### Gameplay
- readable at gameplay distance;
- not dependent on close-up detail;
- no protected-corridor intrusion.

### Production
- required names unchanged;
- pivot preserved;
- transforms preserved;
- semantic material slots valid;
- export succeeds;
- previews regenerated.

## 56. All-world review

Review S01-S05 together.

Check:

- each world has unique identity;
- shared quality bar;
- no world remains blockout-like;
- no one world is over-detailed;
- portals share game-family logic;
- boss portals escalate consistently;
- crystal/gold/emission are not overused;
- surface-frequency distribution is coherent.

## 57. Evidence package

Final Blender refinement evidence should include:

- hero-family previews;
- front / 3/4 / gameplay-camera comparisons;
- neutral-material renders;
- world-mood renders;
- wireframe samples where useful;
- contact sheets;
- export validation;
- material-slot validation;
- transform/pivot validation;
- failure report;
- reference-comparison notes.

Never claim “reference match” from automation logs alone.

## 58. Core diagnostic rule

When quality is weak, diagnose the correct layer.

If silhouette is weak:
MODEL.

If structural logic is weak:
REBUILD SECONDARY FORMS.

If shading is weak:
FIX NORMALS / BEVEL / TOPOLOGY.

If material is flat:
FIX ROUGHNESS / MATERIAL BREAKUP.

If texture is noisy:
REDUCE MICRODETAIL; STRENGTHEN MACRO / MESO.

If asset looks pasted in:
FIX GROUNDING / TRANSITIONS / WEATHERING.

If world identity is weak:
FIX PALETTE / MOTIF / MATERIAL HIERARCHY.

If close-up is good but gameplay is weak:
FIX LARGE-SCALE READABILITY.

Never use one layer to hide a problem from another.

## 59. Completion standard

A Riftward Blender asset is complete only when:

- design matches Riftward intent;
- silhouette works without texture;
- geometry feels authored;
- secondary detail follows construction logic;
- tertiary detail is restrained;
- UVs are clean;
- texture frequency is balanced;
- PBR channels are technically correct;
- material regions are meaningful;
- neutral lighting confirms quality;
- gameplay camera confirms readability;
- LOD preserves identity;
- export preserves production contracts;
- final runtime-owned effects remain outside Blender;
- visual comparison shows no obvious blockout-level gap.

Premium finish comes from coherent decisions at every layer.

It does not come from maximum polygons, maximum resolution, maximum noise, or maximum detail.
