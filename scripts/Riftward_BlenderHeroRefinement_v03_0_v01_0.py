"""
RIFTWARD — Consolidated Blender Hero Refinement
Package: v03_0_v01_0
Script version: 1.0.0
Target Blender: 5.2.2 LTS

PURPOSE
-------
Save-forward the completed automatic-finishing MASTER into a HEROREFINE master,
then perform one deterministic all-world hero-refinement assistance pass across
S01-S05.

This script deliberately does NOT claim to replace final manual art direction.
It is a structured refinement accelerator:

- preserves object names, pivots, transforms and collection placement;
- skips lower LODs / colliders / review helpers;
- processes S01-S05 together;
- adds removable/generated structural detail;
- applies targeted root taper/junction improvement with internal mesh backup;
- improves crystal hierarchy with core/secondary forms;
- adds glacier snow-cap source geometry;
- adds portal buttress/crown depth outside the existing aperture;
- adds tower/plinth/crown structure where appropriate;
- creates semantic Blender source-lookdev materials;
- creates spread-out review collection instances;
- checkpoints after each world;
- writes JSON evidence/report.

Unity still owns final URP materials, reflections, portal energy, atmosphere,
particles, motion, color grading and runtime lighting.
"""

import bpy
import bmesh
import os
import re
import json
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from mathutils import Vector

# =============================================================================
# CONFIG
# =============================================================================

SCRIPT_VERSION = "1.0.0"
PACKAGE_VERSION = "v03_0_v01_0"
REFINE_TAG = "RW_HEROREFINE_v01_0"

DRY_RUN = False

# Geometry behavior
ENABLE_COMMON_BEVELS = True
ENABLE_ROOT_TAPER = True
ENABLE_GENERATED_DETAILS = True
ENABLE_CRYSTAL_CORES = True
ENABLE_SNOW_CAPS = True
ENABLE_REVIEW_INSTANCES = True

# Save/evidence behavior
SAVE_FORWARD = True
CHECKPOINT_AFTER_EACH_WORLD = True
WRITE_JSON_REPORT = True

# Do NOT automatically export before visual/manual review.
EXPORT_AFTER_RUN = False

# Deterministic seed
GLOBAL_SEED = 41731

# Only work on these worlds
WORLD_ORDER = ["S01", "S02", "S03", "S04", "S05"]

# Lower LOD/helper tokens to skip.
SKIP_NAME_TOKENS = (
    "lod1", "lod2", "lod3", "lod4",
    "collider", "collision", "_col", "ucx_",
    "review", "preview", "camera", "light",
    "vfx", "particle", "fx_", "_high", "_cage",
)

# Hero tokens used for review instances and stronger assistance.
HERO_TOKENS = (
    "portal", "boss", "cliff", "glacier", "wreck", "hull",
    "root", "arch", "shrine", "spire", "monolith",
    "ring", "orbital", "fortress", "observatory", "dome",
    "dish", "reactor", "nest", "mirror", "crown",
)

# =============================================================================
# GLOBAL REPORT
# =============================================================================

REPORT = {
    "script": "Riftward_BlenderHeroRefinement_v03_0_v01_0.py",
    "script_version": SCRIPT_VERSION,
    "package_version": PACKAGE_VERSION,
    "generated_utc": None,
    "source_blend": None,
    "output_blend": None,
    "worlds": {},
    "class_counts": {},
    "actions": [],
    "warnings": [],
    "errors": [],
}

# =============================================================================
# UTILITY
# =============================================================================

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def log(msg):
    print(f"[RIFTWARD-HR] {msg}")

def warn(msg):
    REPORT["warnings"].append(msg)
    print(f"[RIFTWARD-HR][WARN] {msg}")

def error(msg):
    REPORT["errors"].append(msg)
    print(f"[RIFTWARD-HR][ERROR] {msg}")

def action(world, asset, obj, kind, detail=""):
    REPORT["actions"].append({
        "world": world,
        "asset": asset,
        "object": obj,
        "action": kind,
        "detail": detail,
    })

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def safe_name(s):
    return re.sub(r"[^A-Za-z0-9_\-]+", "_", s).strip("_")

def seeded_rng(key):
    seed = GLOBAL_SEED
    for ch in key:
        seed = (seed * 33 + ord(ch)) & 0xFFFFFFFF
    return random.Random(seed)

def object_bounds_local(obj):
    pts = [Vector(corner) for corner in obj.bound_box]
    mn = Vector((
        min(p.x for p in pts),
        min(p.y for p in pts),
        min(p.z for p in pts),
    ))
    mx = Vector((
        max(p.x for p in pts),
        max(p.y for p in pts),
        max(p.z for p in pts),
    ))
    return mn, mx, mx - mn, (mn + mx) * 0.5

def bounds_volume(obj):
    try:
        _, _, d, _ = object_bounds_local(obj)
        return max(d.x, 1e-6) * max(d.y, 1e-6) * max(d.z, 1e-6)
    except Exception:
        return 0.0

def max_dimension(obj):
    _, _, d, _ = object_bounds_local(obj)
    return max(d.x, d.y, d.z, 1e-4)

def name_has(text, tokens):
    t = text.lower()
    return any(tok in t for tok in tokens)

def is_eligible_mesh(obj):
    if obj.type != "MESH":
        return False
    n = obj.name.lower()
    if name_has(n, SKIP_NAME_TOKENS):
        return False
    if obj.get("rw_hr_generated", False):
        return False
    return True

def ensure_unique_mesh(obj):
    if obj.data and obj.data.users > 1:
        obj.data = obj.data.copy()

def backup_mesh_data(obj):
    if not obj.data or obj.get("rw_hr_mesh_backup", ""):
        return
    backup = obj.data.copy()
    backup.name = f"{obj.data.name}_PRE_HEROREFINE"
    backup.use_fake_user = True
    obj["rw_hr_mesh_backup"] = backup.name

def mark_processed(obj, profile):
    obj["rw_hr_version"] = SCRIPT_VERSION
    obj["rw_hr_profile"] = profile
    obj["rw_hr_tag"] = REFINE_TAG

def already_processed(obj):
    return obj.get("rw_hr_version", "") == SCRIPT_VERSION

# =============================================================================
# COLLECTION TREE / ASSET GROUPING
# =============================================================================

def build_collection_depths():
    depths = {}

    def walk(col, depth):
        depths[col.name] = max(depths.get(col.name, -1), depth)
        for child in col.children:
            walk(child, depth + 1)

    walk(bpy.context.scene.collection, 0)
    return depths

def choose_asset_collection(obj, depths):
    if not obj.users_collection:
        return bpy.context.scene.collection
    return max(
        obj.users_collection,
        key=lambda c: depths.get(c.name, 0)
    )

def discover_asset_groups():
    depths = build_collection_depths()
    groups = defaultdict(list)

    for obj in bpy.data.objects:
        if not is_eligible_mesh(obj):
            continue
        col = choose_asset_collection(obj, depths)
        groups[col].append(obj)

    # Remove clearly non-asset/global collections when they only contain helper content.
    cleaned = {}
    for col, objects in groups.items():
        name = col.name.lower()
        if name_has(name, ("review", "preview", "helper", "lighting", "camera")):
            continue
        cleaned[col] = objects
    return cleaned

def combined_group_name(col, objects):
    return " ".join([col.name] + [o.name for o in objects])

def detect_world(text):
    upper = text.upper()
    for world in WORLD_ORDER:
        if world in upper:
            return world
    # tolerate S1/S2 etc
    m = re.search(r"(?<![A-Z0-9])S([1-5])(?![0-9])", upper)
    if m:
        return f"S0{m.group(1)}"
    return "UNKNOWN"

def classify_asset(text):
    t = text.lower()

    if "portal" in t:
        return "portal"
    if any(k in t for k in ("crystal", "bloom", "gem")):
        return "crystal"
    if any(k in t for k in ("ice", "glacier", "frozen", "snow")):
        return "ice"
    if any(k in t for k in ("root", "trunk", "tree", "vine", "organic", "nest")):
        return "root"
    if any(k in t for k in ("mirror", "reflective")):
        return "mirror"
    if any(k in t for k in ("ring", "orbital", "arc", "gravity")):
        return "ring"
    if any(k in t for k in ("wreck", "hull", "ship", "station fragment")):
        return "wreck"
    if any(k in t for k in ("rock", "cliff", "boulder", "shelf", "debris", "massif")):
        return "rock"
    if any(k in t for k in (
        "tower", "pylon", "dome", "dish", "plinth", "gantry", "bridge",
        "support", "frame", "fortress", "monolith", "ruin", "structure",
        "spire", "platform", "architecture", "reactor"
    )):
        return "hard_surface"
    if any(k in t for k in ("foliage", "plant", "leaf", "bush", "grass")):
        return "foliage"
    return "support"

def is_hero_group(text):
    return name_has(text, HERO_TOKENS)

def choose_primary_mesh(objects):
    candidates = [o for o in objects if is_eligible_mesh(o)]
    if not candidates:
        return None
    # prefer explicit LOD0, otherwise largest visible mesh
    lod0 = [o for o in candidates if "lod0" in o.name.lower()]
    pool = lod0 if lod0 else candidates
    return max(pool, key=bounds_volume)

# =============================================================================
# MATERIALS
# =============================================================================

WORLD_PROFILES = {
    "S01": {
        "stone": (0.16, 0.17, 0.19, 1.0),
        "structure": (0.07, 0.09, 0.11, 1.0),
        "accent": (0.12, 0.48, 0.58, 1.0),
        "accent_emission": (0.05, 0.75, 1.00, 1.0),
        "gold": (0.48, 0.36, 0.16, 1.0),
    },
    "S02": {
        "stone": (0.28, 0.36, 0.42, 1.0),
        "structure": (0.18, 0.24, 0.29, 1.0),
        "accent": (0.28, 0.66, 0.88, 1.0),
        "accent_emission": (0.20, 0.62, 1.00, 1.0),
        "gold": (0.45, 0.34, 0.14, 1.0),
    },
    "S03": {
        "stone": (0.18, 0.20, 0.16, 1.0),
        "structure": (0.13, 0.09, 0.06, 1.0),
        "accent": (0.18, 0.64, 0.58, 1.0),
        "accent_emission": (0.10, 0.92, 0.76, 1.0),
        "gold": (0.55, 0.39, 0.14, 1.0),
    },
    "S04": {
        "stone": (0.025, 0.027, 0.035, 1.0),
        "structure": (0.045, 0.046, 0.055, 1.0),
        "accent": (0.42, 0.30, 0.09, 1.0),
        "accent_emission": (0.30, 0.12, 0.62, 1.0),
        "gold": (0.58, 0.42, 0.18, 1.0),
    },
    "S05": {
        "stone": (0.20, 0.18, 0.16, 1.0),
        "structure": (0.055, 0.052, 0.052, 1.0),
        "accent": (0.68, 0.58, 0.40, 1.0),
        "accent_emission": (1.00, 0.28, 0.04, 1.0),
        "gold": (0.66, 0.46, 0.15, 1.0),
    },
    "UNKNOWN": {
        "stone": (0.20, 0.20, 0.20, 1.0),
        "structure": (0.08, 0.08, 0.08, 1.0),
        "accent": (0.35, 0.35, 0.35, 1.0),
        "accent_emission": (0.45, 0.65, 0.90, 1.0),
        "gold": (0.55, 0.40, 0.16, 1.0),
    },
}

def bsdf_input(bsdf, candidates):
    for name in candidates:
        if name in bsdf.inputs:
            return bsdf.inputs[name]
    return None

def set_bsdf_value(bsdf, candidates, value):
    socket = bsdf_input(bsdf, candidates)
    if socket is not None:
        socket.default_value = value

def color_scaled(color, factor):
    return (
        clamp(color[0] * factor, 0.0, 1.0),
        clamp(color[1] * factor, 0.0, 1.0),
        clamp(color[2] * factor, 0.0, 1.0),
        color[3],
    )

def ensure_material(name, base_color, metallic=0.0, roughness=0.55,
                    emission_color=None, emission_strength=0.0,
                    transmission=0.0, ior=1.45, noise_scale=4.0):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    out.location = (480, 0)
    bsdf.location = (180, 0)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    set_bsdf_value(bsdf, ("Metallic",), metallic)
    set_bsdf_value(bsdf, ("IOR",), ior)
    set_bsdf_value(bsdf, ("Transmission Weight", "Transmission"), transmission)

    # Broad color variation
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-620, 100)
    noise.inputs["Scale"].default_value = noise_scale
    if "Detail" in noise.inputs:
        noise.inputs["Detail"].default_value = 2.0
    if "Roughness" in noise.inputs:
        noise.inputs["Roughness"].default_value = 0.55

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-360, 120)
    ramp.color_ramp.elements[0].color = color_scaled(base_color, 0.82)
    ramp.color_ramp.elements[1].color = color_scaled(base_color, 1.12)
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])

    base_socket = bsdf_input(bsdf, ("Base Color",))
    if base_socket:
        links.new(ramp.outputs["Color"], base_socket)

    # Roughness variation
    mapr = nodes.new("ShaderNodeMapRange")
    mapr.location = (-80, -170)
    mapr.inputs["From Min"].default_value = 0.0
    mapr.inputs["From Max"].default_value = 1.0
    mapr.inputs["To Min"].default_value = clamp(roughness - 0.08, 0.0, 1.0)
    mapr.inputs["To Max"].default_value = clamp(roughness + 0.08, 0.0, 1.0)
    links.new(noise.outputs["Fac"], mapr.inputs["Value"])
    rough_socket = bsdf_input(bsdf, ("Roughness",))
    if rough_socket:
        links.new(mapr.outputs["Result"], rough_socket)

    if emission_color is not None and emission_strength > 0:
        set_bsdf_value(bsdf, ("Emission Color", "Emission"), emission_color)
        set_bsdf_value(bsdf, ("Emission Strength",), emission_strength)

    return mat

def ensure_world_materials(world):
    p = WORLD_PROFILES.get(world, WORLD_PROFILES["UNKNOWN"])
    mats = {}

    mats["stone"] = ensure_material(
        f"RW_HR_{world}_Stone",
        p["stone"], metallic=0.0, roughness=0.72, noise_scale=3.5
    )
    mats["structure"] = ensure_material(
        f"RW_HR_{world}_Structure",
        p["structure"], metallic=0.85, roughness=0.38, noise_scale=5.0
    )
    mats["accent"] = ensure_material(
        f"RW_HR_{world}_Accent",
        p["accent"], metallic=0.90, roughness=0.28, noise_scale=6.0
    )
    mats["gold"] = ensure_material(
        f"RW_HR_{world}_Gold",
        p["gold"], metallic=1.0, roughness=0.30, noise_scale=7.0
    )
    mats["emissive"] = ensure_material(
        f"RW_HR_{world}_Emissive",
        color_scaled(p["accent_emission"], 0.35),
        metallic=0.0,
        roughness=0.35,
        emission_color=p["accent_emission"],
        emission_strength=2.5,
        noise_scale=4.0
    )

    mats["bark"] = ensure_material(
        "RW_HR_Bark",
        (0.16, 0.09, 0.045, 1.0),
        metallic=0.0, roughness=0.78, noise_scale=7.0
    )
    mats["moss"] = ensure_material(
        "RW_HR_Moss",
        (0.11, 0.21, 0.09, 1.0),
        metallic=0.0, roughness=0.88, noise_scale=8.0
    )
    mats["snow"] = ensure_material(
        "RW_HR_Snow",
        (0.84, 0.90, 0.94, 1.0),
        metallic=0.0, roughness=0.82, noise_scale=10.0
    )
    mats["ice"] = ensure_material(
        "RW_HR_Ice",
        (0.34, 0.62, 0.78, 1.0),
        metallic=0.0, roughness=0.18, transmission=0.55, ior=1.31, noise_scale=4.0
    )
    mats["crystal_outer"] = ensure_material(
        f"RW_HR_{world}_CrystalOuter",
        p["accent"],
        metallic=0.0, roughness=0.12, transmission=0.38, ior=1.52, noise_scale=5.0
    )
    mats["crystal_core"] = ensure_material(
        f"RW_HR_{world}_CrystalCore",
        color_scaled(p["accent_emission"], 0.55),
        metallic=0.0,
        roughness=0.24,
        emission_color=p["accent_emission"],
        emission_strength=3.0,
        noise_scale=4.0
    )
    mats["mirror"] = ensure_material(
        "RW_HR_MirrorPreview",
        (0.035, 0.035, 0.04, 1.0),
        metallic=1.0, roughness=0.04, noise_scale=12.0
    )

    return mats

def assign_single_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

# =============================================================================
# GENERATED DETAIL HELPERS
# =============================================================================

def unique_object_name(base):
    if base not in bpy.data.objects:
        return base
    i = 1
    while f"{base}_{i:02d}" in bpy.data.objects:
        i += 1
    return f"{base}_{i:02d}"

def tag_generated(obj, source_obj, kind):
    obj["rw_hr_generated"] = True
    obj["rw_hr_version"] = SCRIPT_VERSION
    obj["rw_hr_kind"] = kind
    obj["rw_hr_source_object"] = source_obj.name if source_obj else ""

def create_box_detail(collection, source_obj, name, center, size, material, kind="trim"):
    name = unique_object_name(name)
    mesh = bpy.data.meshes.new(name + "_Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)

    sx, sy, sz = max(size[0], 1e-4), max(size[1], 1e-4), max(size[2], 1e-4)
    for v in bm.verts:
        v.co.x = v.co.x * sx + center[0]
        v.co.y = v.co.y * sy + center[1]
        v.co.z = v.co.z * sz + center[2]

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.matrix_world = source_obj.matrix_world.copy()
    tag_generated(obj, source_obj, kind)
    assign_single_material(obj, material)

    # Small bevel for authored edge response
    try:
        bev = obj.modifiers.new("RW_HR_DetailBevel", "BEVEL")
        bev.width = min(sx, sy, sz) * 0.08
        bev.segments = 2
        bev.limit_method = "ANGLE"
    except Exception:
        pass

    return obj

def create_ellipsoid_detail(collection, source_obj, name, center, size, material,
                            kind="secondary_mass", smooth=False):
    name = unique_object_name(name)
    mesh = bpy.data.meshes.new(name + "_Mesh")
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)

    sx, sy, sz = max(size[0], 1e-4), max(size[1], 1e-4), max(size[2], 1e-4)
    for v in bm.verts:
        v.co.x = v.co.x * sx * 0.5 + center[0]
        v.co.y = v.co.y * sy * 0.5 + center[1]
        v.co.z = v.co.z * sz * 0.5 + center[2]

    bm.to_mesh(mesh)
    bm.free()

    for p in mesh.polygons:
        p.use_smooth = smooth

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.matrix_world = source_obj.matrix_world.copy()
    tag_generated(obj, source_obj, kind)
    assign_single_material(obj, material)
    return obj

def create_crystal_prism(collection, source_obj, name, center, radius, height,
                         material, sides=6, lean=(0.0, 0.0)):
    name = unique_object_name(name)
    mesh = bpy.data.meshes.new(name + "_Mesh")

    verts = []
    faces = []

    z0 = center[2] - height * 0.5
    z1 = z0 + height * 0.72
    z2 = z0 + height

    # base and upper rings
    for ring_z, scale in ((z0, 1.0), (z1, 0.82)):
        for i in range(sides):
            a = (i / sides) * math.tau
            verts.append((
                center[0] + math.cos(a) * radius * scale + lean[0] * ((ring_z-z0)/height),
                center[1] + math.sin(a) * radius * scale + lean[1] * ((ring_z-z0)/height),
                ring_z,
            ))

    tip_index = len(verts)
    verts.append((
        center[0] + lean[0],
        center[1] + lean[1],
        z2,
    ))

    # base
    faces.append(tuple(range(sides - 1, -1, -1)))

    # sides between rings
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((i, j, sides + j, sides + i))

    # tip triangles
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((sides + i, sides + j, tip_index))

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    for p in mesh.polygons:
        p.use_smooth = False

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.matrix_world = source_obj.matrix_world.copy()
    tag_generated(obj, source_obj, "secondary_crystal")
    assign_single_material(obj, material)
    return obj

def create_top_face_overlay(collection, source_obj, name, material,
                            normal_threshold=0.55, offset_ratio=0.0025, max_faces=2500):
    mesh = source_obj.data
    if not mesh or len(mesh.polygons) == 0:
        return None

    maxdim = max_dimension(source_obj)
    offset = maxdim * offset_ratio

    verts = []
    faces = []
    face_count = 0

    for poly in mesh.polygons:
        if face_count >= max_faces:
            break
        if poly.normal.z < normal_threshold:
            continue

        face = []
        n = poly.normal.normalized()
        for vi in poly.vertices:
            co = mesh.vertices[vi].co + n * offset
            face.append(len(verts))
            verts.append(tuple(co))
        if len(face) >= 3:
            faces.append(tuple(face))
            face_count += 1

    if not faces:
        return None

    out_mesh = bpy.data.meshes.new(name + "_Mesh")
    out_mesh.from_pydata(verts, [], faces)
    out_mesh.update()

    obj = bpy.data.objects.new(unique_object_name(name), out_mesh)
    collection.objects.link(obj)
    obj.matrix_world = source_obj.matrix_world.copy()
    tag_generated(obj, source_obj, "surface_overlay")
    assign_single_material(obj, material)
    return obj

# =============================================================================
# COMMON POLISH
# =============================================================================

def add_bevel_modifier(obj, cls):
    if not ENABLE_COMMON_BEVELS:
        return False
    if obj.modifiers.get("RW_HR_Bevel"):
        return False

    maxdim = max_dimension(obj)

    ratios = {
        "portal": 0.006,
        "hard_surface": 0.0045,
        "ring": 0.0045,
        "wreck": 0.0035,
        "mirror": 0.0035,
        "crystal": 0.0020,
        "ice": 0.0020,
        "root": 0.0015,
        "rock": 0.0010,
        "support": 0.0020,
    }
    ratio = ratios.get(cls, 0.0020)

    try:
        bev = obj.modifiers.new("RW_HR_Bevel", "BEVEL")
        bev.width = maxdim * ratio
        bev.segments = 2 if cls in ("portal", "hard_surface", "ring", "mirror") else 1
        bev.limit_method = "ANGLE"
        if hasattr(bev, "angle_limit"):
            bev.angle_limit = math.radians(28.0)
        return True
    except Exception as exc:
        warn(f"Bevel failed on {obj.name}: {exc}")
        return False

def try_weighted_normal(obj):
    if obj.modifiers.get("RW_HR_WeightedNormal"):
        return False
    try:
        mod = obj.modifiers.new("RW_HR_WeightedNormal", "WEIGHTED_NORMAL")
        if hasattr(mod, "keep_sharp"):
            mod.keep_sharp = True
        return True
    except Exception:
        return False

def common_polish(obj, cls, world, asset_name):
    if already_processed(obj):
        return

    if add_bevel_modifier(obj, cls):
        action(world, asset_name, obj.name, "micro_bevel", cls)

    if cls in ("portal", "hard_surface", "ring", "wreck", "mirror"):
        if try_weighted_normal(obj):
            action(world, asset_name, obj.name, "weighted_normal", cls)

    if cls == "crystal":
        for p in obj.data.polygons:
            p.use_smooth = False
        action(world, asset_name, obj.name, "faceted_shading", "flat crystal facets")

    mark_processed(obj, cls)

# =============================================================================
# CLASS-SPECIFIC REFINEMENT
# =============================================================================

def dominant_axis_for_root(obj):
    _, _, d, _ = object_bounds_local(obj)
    dims = [d.x, d.y, d.z]
    return max(range(3), key=lambda i: dims[i])

def refine_root_mesh(obj, world, asset_name, collection, mats):
    if not ENABLE_ROOT_TAPER:
        return
    if obj.get("rw_hr_root_taper", False):
        return
    if not obj.data or len(obj.data.vertices) < 24:
        return
    if obj.data.shape_keys:
        warn(f"Skipped destructive root taper on {obj.name}: shape keys present.")
        return

    backup_mesh_data(obj)
    ensure_unique_mesh(obj)

    mesh = obj.data
    mn, mx, dims, _ = object_bounds_local(obj)
    axis = dominant_axis_for_root(obj)
    axis_min = (mn.x, mn.y, mn.z)[axis]
    axis_max = (mx.x, mx.y, mx.z)[axis]

    if abs(axis_max - axis_min) < 1e-5:
        return

    # Choose the endpoint closest to local origin as the base.
    if abs(axis_min) <= abs(axis_max):
        base = axis_min
        end = axis_max
    else:
        base = axis_max
        end = axis_min

    other = [0, 1, 2]
    other.remove(axis)
    a0, a1 = other
    length = abs(end - base)
    phase = seeded_rng(obj.name).random() * math.tau

    for v in mesh.vertices:
        co = v.co
        t = (co[axis] - base) / (end - base)
        t = clamp(t, 0.0, 1.0)

        taper = 1.18 - 0.38 * t
        knuckle = (
            0.12 * math.exp(-((t - 0.18) / 0.075) ** 2)
            + 0.08 * math.exp(-((t - 0.46) / 0.09) ** 2)
        )

        angle = math.atan2(co[a1], co[a0])
        asym = 1.0 + 0.055 * math.sin(angle * 3.0 + t * 7.0 + phase)

        scale = clamp((taper + knuckle) * asym, 0.74, 1.34)

        co[a0] *= scale
        co[a1] *= scale

        # Low-amplitude authored-looking lateral warp.
        warp = length * 0.010 * (1.0 - t)
        co[a0] += math.sin(t * 5.7 + phase) * warp
        co[a1] += math.cos(t * 4.9 + phase * 0.71) * warp

    mesh.update()
    obj["rw_hr_root_taper"] = True
    action(world, asset_name, obj.name, "root_taper", f"axis={axis}")

    if ENABLE_GENERATED_DETAILS:
        # Add a few broad junction masses, not micro-noise.
        positions = (0.16, 0.40)
        min_cross = min(
            (dims.x, dims.y, dims.z)[a0],
            (dims.x, dims.y, dims.z)[a1]
        )
        for idx, target_t in enumerate(positions):
            band = []
            for v in mesh.vertices:
                t = (v.co[axis] - base) / (end - base)
                if abs(t - target_t) < 0.045:
                    band.append(v.co.copy())
            if not band:
                continue
            center = sum(band, Vector()) / len(band)
            size = [min_cross * 0.28, min_cross * 0.28, min_cross * 0.28]
            size[axis] = length * 0.075
            create_ellipsoid_detail(
                collection, obj,
                f"{safe_name(asset_name)}_HR_RootKnuckle_{idx+1}",
                center, size, mats["bark"],
                kind="root_knuckle", smooth=True
            )
            action(world, asset_name, obj.name, "root_knuckle", f"t={target_t:.2f}")

def augment_rock(obj, world, asset_name, collection, mats, hero):
    if not ENABLE_GENERATED_DETAILS:
        return
    key = f"{asset_name}|rock"
    rng = seeded_rng(key)

    mn, mx, d, c = object_bounds_local(obj)
    if max(d.x, d.y, d.z) <= 0:
        return

    count = 2 if hero else 1
    horizontal_axis = 0 if d.x >= d.y else 1
    other_axis = 1 - horizontal_axis

    for i in range(count):
        center = c.copy()
        side = -1.0 if i % 2 == 0 else 1.0
        if horizontal_axis == 0:
            center.x = (mn.x if side < 0 else mx.x) + side * d.x * 0.03
            center.y += (rng.random() - 0.5) * d.y * 0.25
        else:
            center.y = (mn.y if side < 0 else mx.y) + side * d.y * 0.03
            center.x += (rng.random() - 0.5) * d.x * 0.25
        center.z = mn.z + d.z * (0.20 + 0.30 * rng.random())

        size = (
            max(d.x * (0.18 + 0.08 * rng.random()), 0.02),
            max(d.y * (0.18 + 0.08 * rng.random()), 0.02),
            max(d.z * (0.18 + 0.07 * rng.random()), 0.02),
        )

        create_ellipsoid_detail(
            collection, obj,
            f"{safe_name(asset_name)}_HR_SecondaryRock_{i+1}",
            center, size, mats["stone"],
            kind="secondary_rock", smooth=False
        )
        action(world, asset_name, obj.name, "secondary_rock", f"index={i+1}")

def augment_vertical_structure(obj, world, asset_name, collection, mats, text):
    if not ENABLE_GENERATED_DETAILS:
        return

    mn, mx, d, c = object_bounds_local(obj)
    if d.z <= 0:
        return

    lower = text.lower()
    vertical = d.z > max(d.x, d.y) * 1.15 or any(
        k in lower for k in ("tower", "pylon", "spire", "monolith")
    )

    if not vertical:
        return

    # Base and crown remain outside/at the extremities of the existing form.
    base_center = Vector((c.x, c.y, mn.z + d.z * 0.035))
    base_size = (d.x * 1.06, d.y * 1.06, d.z * 0.07)
    create_box_detail(
        collection, obj,
        f"{safe_name(asset_name)}_HR_BaseStep",
        base_center, base_size, mats["structure"], kind="base_step"
    )
    action(world, asset_name, obj.name, "base_step", "structural base hierarchy")

    crown_center = Vector((c.x, c.y, mx.z - d.z * 0.025))
    crown_size = (d.x * 1.04, d.y * 1.04, d.z * 0.05)
    crown_mat = mats["gold"] if world in ("S04", "S05") else mats["accent"]
    create_box_detail(
        collection, obj,
        f"{safe_name(asset_name)}_HR_CrownBand",
        crown_center, crown_size, crown_mat, kind="crown_band"
    )
    action(world, asset_name, obj.name, "crown_band", "top profile hierarchy")

def augment_portal(obj, world, asset_name, collection, mats, text):
    if not ENABLE_GENERATED_DETAILS:
        return

    mn, mx, d, c = object_bounds_local(obj)
    if d.z <= 0:
        return

    width_axis = 0 if d.x >= d.y else 1
    depth_axis = 1 - width_axis
    width = (d.x, d.y)[width_axis]
    depth = (d.x, d.y)[depth_axis]
    height = d.z

    if width <= 0 or depth <= 0:
        return

    structure_mat = mats["structure"]
    accent_mat = mats["gold"] if world in ("S04", "S05") else mats["accent"]

    # Side buttresses are placed OUTSIDE the current outer bounds so they cannot
    # close the existing aperture.
    for side_idx, side in enumerate((-1.0, 1.0), start=1):
        center = [c.x, c.y, mn.z + height * 0.30]
        size = [d.x * 0.12, d.y * 0.12, height * 0.52]

        if width_axis == 0:
            center[0] = (mn.x if side < 0 else mx.x) + side * width * 0.055
            size[0] = width * 0.11
            size[1] = max(depth * 1.25, width * 0.04)
        else:
            center[1] = (mn.y if side < 0 else mx.y) + side * width * 0.055
            size[1] = width * 0.11
            size[0] = max(depth * 1.25, width * 0.04)

        create_box_detail(
            collection, obj,
            f"{safe_name(asset_name)}_HR_PortalButtress_{side_idx}",
            center, size, structure_mat, kind="portal_buttress"
        )
        action(world, asset_name, obj.name, "portal_buttress", f"side={side_idx}")

    crown_center = [c.x, c.y, mx.z + height * 0.025]
    crown_size = [d.x * 0.10, d.y * 0.10, height * 0.075]
    if width_axis == 0:
        crown_size[0] = width * 0.72
        crown_size[1] = max(depth * 1.30, width * 0.045)
    else:
        crown_size[1] = width * 0.72
        crown_size[0] = max(depth * 1.30, width * 0.045)

    create_box_detail(
        collection, obj,
        f"{safe_name(asset_name)}_HR_PortalCrown",
        crown_center, crown_size, accent_mat, kind="portal_crown"
    )
    action(world, asset_name, obj.name, "portal_crown", "top profile")

    if "boss" in text.lower():
        crest_center = list(crown_center)
        crest_center[2] += height * 0.11
        crest_size = list(crown_size)
        if width_axis == 0:
            crest_size[0] = width * 0.28
        else:
            crest_size[1] = width * 0.28
        crest_size[2] = height * 0.18

        create_box_detail(
            collection, obj,
            f"{safe_name(asset_name)}_HR_BossCrest",
            crest_center, crest_size, accent_mat, kind="boss_crest"
        )
        action(world, asset_name, obj.name, "boss_crest", "boss structural escalation")

def augment_ring(obj, world, asset_name, collection, mats):
    if not ENABLE_GENERATED_DETAILS:
        return

    mn, mx, d, c = object_bounds_local(obj)
    width_axis = 0 if d.x >= d.y else 1
    depth_axis = 1 - width_axis
    width = (d.x, d.y)[width_axis]
    depth = (d.x, d.y)[depth_axis]
    if width <= 0 or d.z <= 0:
        return

    accent_mat = mats["gold"] if world in ("S04", "S05") else mats["accent"]

    # Three external clamps: left/right/top. They add structural rhythm without
    # changing the central opening.
    positions = [
        ("Left", -1.0, 0.45),
        ("Right", 1.0, 0.55),
    ]

    for label, side, zf in positions:
        center = [c.x, c.y, mn.z + d.z * zf]
        size = [d.x * 0.10, d.y * 0.10, d.z * 0.12]
        if width_axis == 0:
            center[0] = (mn.x if side < 0 else mx.x) + side * width * 0.025
            size[0] = width * 0.07
            size[1] = max(depth * 1.20, width * 0.035)
        else:
            center[1] = (mn.y if side < 0 else mx.y) + side * width * 0.025
            size[1] = width * 0.07
            size[0] = max(depth * 1.20, width * 0.035)

        create_box_detail(
            collection, obj,
            f"{safe_name(asset_name)}_HR_RingClamp_{label}",
            center, size, accent_mat, kind="ring_clamp"
        )
        action(world, asset_name, obj.name, "ring_clamp", label)

def augment_crystal(obj, world, asset_name, collection, mats):
    if not ENABLE_CRYSTAL_CORES:
        return

    # Inner core duplicates the same faceted topology at smaller scale in mesh
    # coordinates while preserving the source object transform.
    core_name = f"{obj.name}_HR_Core"
    if bpy.data.objects.get(core_name):
        return

    core_mesh = obj.data.copy()
    core_mesh.name = core_name + "_Mesh"
    for v in core_mesh.vertices:
        v.co *= 0.58

    core = bpy.data.objects.new(core_name, core_mesh)
    collection.objects.link(core)
    core.matrix_world = obj.matrix_world.copy()
    tag_generated(core, obj, "crystal_core")
    assign_single_material(core, mats["crystal_core"])
    for p in core.data.polygons:
        p.use_smooth = False

    action(world, asset_name, obj.name, "crystal_core", "scaled inner core")

    if ENABLE_GENERATED_DETAILS:
        mn, mx, d, c = object_bounds_local(obj)
        rng = seeded_rng(asset_name + "|crystal")
        base_z = mn.z

        for i in range(2):
            px = c.x + (rng.random() - 0.5) * d.x * 0.55
            py = c.y + (rng.random() - 0.5) * d.y * 0.55
            h = max(d.z * (0.24 + 0.10 * rng.random()), max(d.x, d.y) * 0.15)
            radius = max(min(d.x, d.y) * (0.07 + 0.03 * rng.random()), h * 0.06)
            lean = (
                (rng.random() - 0.5) * radius * 0.9,
                (rng.random() - 0.5) * radius * 0.9,
            )
            create_crystal_prism(
                collection, obj,
                f"{safe_name(asset_name)}_HR_SecondaryCrystal_{i+1}",
                (px, py, base_z + h * 0.5),
                radius, h, mats["crystal_outer"],
                sides=6, lean=lean
            )
            action(world, asset_name, obj.name, "secondary_crystal", f"index={i+1}")

def augment_ice(obj, world, asset_name, collection, mats):
    if not ENABLE_SNOW_CAPS:
        return

    overlay_name = f"{safe_name(asset_name)}_HR_SnowCap"
    if any(o.name.startswith(overlay_name) for o in collection.objects):
        return

    overlay = create_top_face_overlay(
        collection, obj, overlay_name, mats["snow"],
        normal_threshold=0.60,
        offset_ratio=0.0025,
        max_faces=2200
    )
    if overlay:
        action(world, asset_name, obj.name, "snow_cap", "up-facing source overlay")

def augment_mirror(obj, world, asset_name, collection, mats):
    if not ENABLE_GENERATED_DETAILS:
        return

    mn, mx, d, c = object_bounds_local(obj)
    dims = [d.x, d.y, d.z]
    thin_axis = min(range(3), key=lambda i: dims[i])

    # Backing is slightly behind the existing mirror along its thinnest axis.
    center = [c.x, c.y, c.z]
    size = [d.x * 1.03, d.y * 1.03, d.z * 1.03]
    thickness = max(max(dims) * 0.018, dims[thin_axis] * 1.6)

    if thin_axis == 0:
        center[0] = mn.x - thickness * 0.45
        size[0] = thickness
    elif thin_axis == 1:
        center[1] = mn.y - thickness * 0.45
        size[1] = thickness
    else:
        center[2] = mn.z - thickness * 0.45
        size[2] = thickness

    create_box_detail(
        collection, obj,
        f"{safe_name(asset_name)}_HR_MirrorBacking",
        center, size, mats["structure"], kind="mirror_backing"
    )
    action(world, asset_name, obj.name, "mirror_backing", f"thin_axis={thin_axis}")

# =============================================================================
# REVIEW INSTANCES
# =============================================================================

def ensure_collection(name, parent):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
    if col.name not in [c.name for c in parent.children]:
        try:
            parent.children.link(col)
        except RuntimeError:
            pass
    return col

def clear_review_instances():
    for obj in list(bpy.data.objects):
        if obj.get("rw_hr_review_instance", False):
            bpy.data.objects.remove(obj, do_unlink=True)

def create_review_instances(group_records):
    if not ENABLE_REVIEW_INSTANCES:
        return

    root = ensure_collection("RW_HEROREFINE_REVIEW", bpy.context.scene.collection)
    clear_review_instances()

    by_world = defaultdict(list)
    for rec in group_records:
        if rec["hero"] and rec["world"] in WORLD_ORDER:
            by_world[rec["world"]].append(rec)

    world_spacing = 28.0
    asset_spacing = 16.0

    for wi, world in enumerate(WORLD_ORDER):
        sub = ensure_collection(f"RW_HEROREFINE_REVIEW_{world}", root)
        records = by_world.get(world, [])
        for ai, rec in enumerate(records):
            col = rec["collection"]
            inst = bpy.data.objects.new(
                unique_object_name(f"HR_REVIEW_{world}_{safe_name(col.name)}"),
                None
            )
            inst.instance_type = "COLLECTION"
            inst.instance_collection = col
            inst.location = (ai * asset_spacing, wi * world_spacing, 0.0)
            inst.empty_display_type = "PLAIN_AXES"
            inst["rw_hr_review_instance"] = True
            sub.objects.link(inst)

# =============================================================================
# SAVE / REPORT
# =============================================================================

def derive_output_path(source_path):
    if not source_path:
        raise RuntimeError("Current Blender file has never been saved.")

    source_path = os.path.abspath(source_path)

    if "HEROREFINE" in os.path.basename(source_path).upper():
        return source_path

    blend_dir = os.path.dirname(source_path)
    finishing_root = os.path.dirname(blend_dir)
    parent = os.path.dirname(finishing_root)

    out_root = os.path.join(
        parent,
        "Riftward_BlenderHeroRefinement_v03_0_v01_0"
    )
    out_blend_dir = os.path.join(out_root, "Blend")
    os.makedirs(out_blend_dir, exist_ok=True)

    filename = os.path.basename(source_path)
    if "FINISHED" in filename:
        filename = filename.replace("FINISHED", "HEROREFINE")
    elif filename.lower().endswith(".blend"):
        filename = filename[:-6] + "_HEROREFINE_v01_0.blend"
    else:
        filename += "_HEROREFINE_v01_0.blend"

    return os.path.join(out_blend_dir, filename)

def report_directory():
    blend_path = bpy.data.filepath
    blend_dir = os.path.dirname(blend_path)
    root = os.path.dirname(blend_dir)
    out = os.path.join(root, "Reports")
    os.makedirs(out, exist_ok=True)
    return out

def write_report_file():
    if not WRITE_JSON_REPORT:
        return None

    REPORT["generated_utc"] = utc_now()
    path = os.path.join(
        report_directory(),
        "RIFTWARD_HERO_REFINEMENT_REPORT_v01_0.json"
    )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(REPORT, f, indent=2)
    log(f"Report written: {path}")
    return path

def checkpoint(world):
    if not CHECKPOINT_AFTER_EACH_WORLD:
        return
    bpy.context.scene["rw_hr_last_completed_world"] = world
    bpy.context.scene["rw_hr_script_version"] = SCRIPT_VERSION
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    log(f"Checkpoint saved after {world}")

# =============================================================================
# MAIN GROUP PROCESSING
# =============================================================================

def process_group(col, objects):
    text = combined_group_name(col, objects)
    world = detect_world(text)
    cls = classify_asset(text)
    hero = is_hero_group(text)
    primary = choose_primary_mesh(objects)

    if world == "UNKNOWN":
        # Keep unknown support groups safe. Common polish is allowed, but no
        # world-specific generated hero detail.
        hero = False

    asset_name = col.name
    mats = ensure_world_materials(world)

    REPORT["class_counts"][cls] = REPORT["class_counts"].get(cls, 0) + 1

    # Common, non-destructive polish on eligible meshes.
    for obj in objects:
        if not is_eligible_mesh(obj):
            continue
        common_polish(obj, cls, world, asset_name)

    if not primary:
        return {
            "world": world,
            "class": cls,
            "hero": hero,
            "collection": col,
            "primary": None,
        }

    # Targeted primary-mesh assistance.
    if cls == "root":
        refine_root_mesh(primary, world, asset_name, col, mats)

    elif cls == "rock":
        augment_rock(primary, world, asset_name, col, mats, hero)

    elif cls == "portal":
        augment_portal(primary, world, asset_name, col, mats, text)

    elif cls == "ring":
        augment_ring(primary, world, asset_name, col, mats)

    elif cls == "hard_surface":
        augment_vertical_structure(primary, world, asset_name, col, mats, text)

    elif cls == "crystal":
        augment_crystal(primary, world, asset_name, col, mats)

    elif cls == "ice":
        augment_ice(primary, world, asset_name, col, mats)

    elif cls == "mirror":
        augment_mirror(primary, world, asset_name, col, mats)

    return {
        "world": world,
        "class": cls,
        "hero": hero,
        "collection": col,
        "primary": primary,
    }

def run():
    log("============================================================")
    log("Riftward Hero Refinement — START")
    log(f"Script version: {SCRIPT_VERSION}")
    log("============================================================")

    source = bpy.data.filepath
    if not source:
        raise RuntimeError(
            "Open the automatic-finished Riftward MASTER first. "
            "The current file is unsaved."
        )

    REPORT["source_blend"] = source

    # Safety: refuse obvious foundation source.
    base_upper = os.path.basename(source).upper()
    if "FOUNDATION" in base_upper and "FINISHED" not in base_upper:
        raise RuntimeError(
            "Refusing to refine a FOUNDATION file. "
            "Open RW_Riftward_v03_AllWorldAssets_FINISHED_v01_0.blend."
        )

    # Save-forward before editing.
    out_path = derive_output_path(source)
    REPORT["output_blend"] = out_path

    if SAVE_FORWARD and os.path.abspath(out_path) != os.path.abspath(source):
        if os.path.exists(out_path):
            raise RuntimeError(
                f"HEROREFINE output already exists:\n{out_path}\n"
                "Open that file directly to resume, or move/archive it first."
            )
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        if not DRY_RUN:
            bpy.ops.wm.save_as_mainfile(filepath=out_path)
        log(f"Save-forward HEROREFINE master: {out_path}")

    bpy.context.scene["rw_hr_script_version"] = SCRIPT_VERSION
    bpy.context.scene["rw_hr_source_blend"] = source
    bpy.context.scene["rw_hr_started_utc"] = utc_now()

    groups = discover_asset_groups()
    log(f"Discovered asset collections: {len(groups)}")

    # Prepare group metadata first so same-phase work remains consolidated.
    group_meta = []
    for col, objects in groups.items():
        combined = combined_group_name(col, objects)
        group_meta.append({
            "collection": col,
            "objects": objects,
            "world": detect_world(combined),
            "class": classify_asset(combined),
            "hero": is_hero_group(combined),
        })

    # Stable ordering: world then collection.
    world_rank = {w: i for i, w in enumerate(WORLD_ORDER)}
    group_meta.sort(
        key=lambda r: (
            world_rank.get(r["world"], 99),
            r["collection"].name.lower()
        )
    )

    processed_records = []
    current_world = None
    world_stats = defaultdict(lambda: {
        "groups": 0,
        "hero_groups": 0,
        "classes": defaultdict(int),
    })

    for meta in group_meta:
        world = meta["world"]

        if current_world is not None and world != current_world and current_world in WORLD_ORDER:
            if not DRY_RUN:
                checkpoint(current_world)

        current_world = world

        try:
            rec = process_group(meta["collection"], meta["objects"])
            processed_records.append(rec)

            stats = world_stats[world]
            stats["groups"] += 1
            if rec["hero"]:
                stats["hero_groups"] += 1
            stats["classes"][rec["class"]] += 1

            log(
                f"{world:7s} | {rec['class']:12s} | "
                f"{meta['collection'].name}"
            )
        except Exception as exc:
            error(f"{meta['collection'].name}: {type(exc).__name__}: {exc}")

    if current_world in WORLD_ORDER and not DRY_RUN:
        checkpoint(current_world)

    # Convert defaultdicts to plain dicts for JSON.
    for world, stats in world_stats.items():
        REPORT["worlds"][world] = {
            "groups": stats["groups"],
            "hero_groups": stats["hero_groups"],
            "classes": dict(stats["classes"]),
        }

    if ENABLE_REVIEW_INSTANCES and not DRY_RUN:
        create_review_instances(processed_records)
        action("ALL", "REVIEW", "RW_HEROREFINE_REVIEW", "review_instances",
               "spread-out collection instances for hero families")

    bpy.context.scene["rw_hr_completed_utc"] = utc_now()

    if not DRY_RUN:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

    write_report_file()

    log("============================================================")
    log(f"Actions: {len(REPORT['actions'])}")
    log(f"Warnings: {len(REPORT['warnings'])}")
    log(f"Errors: {len(REPORT['errors'])}")
    log("Riftward Hero Refinement — COMPLETE")
    log("Manual hero review is STILL REQUIRED before Unity intake.")
    log("============================================================")

    if EXPORT_AFTER_RUN:
        warn(
            "EXPORT_AFTER_RUN is intentionally unsupported in v01_0. "
            "Perform visual/manual signoff before export."
        )

if __name__ == "__main__":
    run()
